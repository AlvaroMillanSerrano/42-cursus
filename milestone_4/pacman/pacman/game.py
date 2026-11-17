"""Game rules, independent of any graphics or input code."""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import Callable

from .ai import choose_direction
from .config import Config
from .entities import ACTIVE, EATEN, WAITING, Ghost, Mover, Player
from .maze import NONE, Cell, Maze, generate_with_retry

LOGGER = logging.getLogger("pacman.game")

# events returned by Game.update
EV_PACGUM = "pacgum"
EV_SUPER = "super"
EV_GHOST_EATEN = "ghost_eaten"
EV_PLAYER_DIED = "player_died"
EV_TIME_UP = "time_up"
EV_LEVEL_COMPLETE = "level_complete"

MAX_STEP = 1.0 / 60.0
HIT_DISTANCE = 0.55
EATEN_SPEED_FACTOR = 2.0
FRIGHTENED_SPEED_FACTOR = 0.6
CHEAT_SPEED_FACTOR = 1.6

MazeFactory = Callable[[int, int, int, random.Random], Maze]


@dataclass
class Cheats:
    """State of the cheat mode used during peer review."""

    enabled: bool = False
    invincible: bool = False
    freeze: bool = False
    fast: bool = False

    def active(self) -> list[str]:
        """Names of the cheats currently switched on."""
        if not self.enabled:
            return []
        names = []
        if self.invincible:
            names.append("INVINCIBLE")
        if self.freeze:
            names.append("FREEZE")
        if self.fast:
            names.append("FAST")
        return names


@dataclass
class Event:
    """Something that happened during an update."""

    kind: str
    cell: Cell = (0, 0)
    points: int = 0


@dataclass
class Game:
    """One play session: lives, score, current level and entities."""

    config: Config
    rng: random.Random = field(default_factory=random.Random)
    maze_factory: MazeFactory = generate_with_retry

    def __post_init__(self) -> None:
        """Initialise a fresh session (call :meth:`start_level` next)."""
        self.lives = self.config.lives
        self.score = 0
        self.level_index = 0
        self.cheats = Cheats(enabled=self.config.cheat_mode)
        self.maze: Maze | None = None
        self.player = Player((0, 0))
        self.ghosts: list[Ghost] = []
        self.pacgums: set[Cell] = set()
        self.supers: set[Cell] = set()
        self.time_left = 0.0
        self.power_time_left = 0.0
        self.clock = 0.0

    # -- level handling -----------------------------------------------------

    @property
    def level_count(self) -> int:
        """Number of levels in the game."""
        return len(self.config.levels)

    @property
    def current_maze(self) -> Maze:
        """The maze of the current level (a level must be loaded)."""
        if self.maze is None:
            raise RuntimeError("no level loaded")
        return self.maze

    def start_level(self, index: int) -> None:
        """Generate and enter level ``index``.

        Raises :class:`pacman.maze.MazeError` if no maze can be built.
        """
        level = self.config.levels[index]
        maze = self.maze_factory(level.width, level.height,
                                 self.config.level_seed(index), self.rng)
        self.maze = maze
        self.level_index = index
        self._fill_level()

    def restart_level(self) -> None:
        """Replay the current level on the same maze (time ran out)."""
        self._fill_level()

    def _fill_level(self) -> None:
        maze = self.current_maze
        self.pacgums = self._place_pacgums(maze)
        self.supers = set(maze.corners)
        self.pacgums -= self.supers
        self.time_left = float(self.config.level_time(self.level_index))
        self.ghosts = [Ghost(i, corner)
                       for i, corner in enumerate(maze.corners)]
        self.reset_positions()

    def _place_pacgums(self, maze: Maze) -> set[Cell]:
        cells = [c for c in maze.free_cells()
                 if c != maze.start and c not in maze.corners]
        wanted = self.config.pacgum
        if 0 < wanted < len(cells):
            return set(self.rng.sample(cells, wanted))
        return set(cells)

    def reset_positions(self) -> None:
        """Player to the middle, ghosts to their corners (after a death)."""
        maze = self.current_maze
        self.player.reset(maze.start)
        self.power_time_left = 0.0
        for ghost in self.ghosts:
            ghost.send_home(self.release_delay(ghost.index))

    def release_delay(self, index: int) -> float:
        """Seconds a ghost waits in its corner before leaving."""
        return 1.0 + 1.5 * index

    # -- level parameters ---------------------------------------------------

    def ghost_speed(self) -> float:
        """Base ghost speed of the current level (cells per second)."""
        speed = self.config.ghost_speed + 0.12 * self.level_index
        return min(speed, self.config.player_speed * 0.97)

    def power_duration(self) -> float:
        """How long ghosts stay edible in the current level."""
        return max(3.0, self.config.power_time - 0.4 * self.level_index)

    # -- cheats -------------------------------------------------------------

    def cheat_extra_life(self) -> None:
        """Cheat: +1 life."""
        if self.cheats.enabled:
            self.lives += 1

    def cheat_skip_level(self) -> None:
        """Cheat: win the level immediately."""
        if self.cheats.enabled:
            self.pacgums.clear()
            self.supers.clear()

    # -- main update --------------------------------------------------------

    def update(self, dt: float) -> list[Event]:
        """Advance the simulation by ``dt`` seconds; return the events."""
        events: list[Event] = []
        remaining = dt
        while remaining > 1e-9:
            step = min(remaining, MAX_STEP)
            remaining -= step
            self._step(step, events)
            if any(e.kind in (EV_PLAYER_DIED, EV_TIME_UP,
                              EV_LEVEL_COMPLETE) for e in events):
                break
        return events

    def _step(self, dt: float, events: list[Event]) -> None:
        maze = self.current_maze
        self.clock += dt
        self.time_left -= dt
        if self.time_left <= 0.0:
            self.time_left = 0.0
            self.lives -= 1
            events.append(Event(EV_TIME_UP))
            return
        speed = self.config.player_speed
        if self.cheats.enabled and self.cheats.fast:
            speed *= CHEAT_SPEED_FACTOR
        self.player.advance(speed * dt, self.player.choose(maze))
        if self.player.direction != NONE:
            self.player.anim += dt * 12.0
        if self.power_time_left > 0.0:
            self.power_time_left -= dt
            if self.power_time_left <= 0.0:
                self.power_time_left = 0.0
                for ghost in self.ghosts:
                    ghost.edible = False
        if not (self.cheats.enabled and self.cheats.freeze):
            for ghost in self.ghosts:
                self._update_ghost(ghost, dt)
        self._collect(events)
        self._collide(events)
        if (not self.pacgums and not self.supers
                and not any(e.kind == EV_PLAYER_DIED for e in events)):
            events.append(Event(EV_LEVEL_COMPLETE))

    def _update_ghost(self, ghost: Ghost, dt: float) -> None:
        maze = self.current_maze
        if ghost.mode == EATEN:
            ghost.respawn = max(0.0, ghost.respawn - dt)
            at_home = ghost.cell == ghost.home and ghost.progress == 0.0
            if at_home:
                ghost.direction = NONE
                if ghost.respawn <= 0.0:
                    ghost.mode = ACTIVE
                return
            speed = self.ghost_speed() * EATEN_SPEED_FACTOR
        elif ghost.mode == WAITING:
            ghost.wait -= dt
            if ghost.wait <= 0.0:
                ghost.mode = ACTIVE
            return
        else:
            speed = self.ghost_speed()
            if ghost.edible:
                speed *= FRIGHTENED_SPEED_FACTOR

        def decide(_: Mover) -> int:
            return choose_direction(ghost, maze, self.player, self.rng)

        ghost.advance(speed * dt, decide)

    def _collect(self, events: list[Event]) -> None:
        cell = self.player.nearest_cell
        if cell in self.pacgums:
            self.pacgums.discard(cell)
            self.score += self.config.points_per_pacgum
            events.append(Event(EV_PACGUM, cell,
                                self.config.points_per_pacgum))
        elif cell in self.supers:
            self.supers.discard(cell)
            self.score += self.config.points_per_super_pacgum
            self.power_time_left = self.power_duration()
            for ghost in self.ghosts:
                if ghost.mode != EATEN:
                    if not ghost.edible:
                        ghost.reverse()
                    ghost.edible = True
            events.append(Event(EV_SUPER, cell,
                                self.config.points_per_super_pacgum))

    def _collide(self, events: list[Event]) -> None:
        px, py = self.player.position
        for ghost in self.ghosts:
            if ghost.mode == EATEN:
                continue
            gx, gy = ghost.position
            if (gx - px) ** 2 + (gy - py) ** 2 > HIT_DISTANCE ** 2:
                continue
            if ghost.edible:
                ghost.mode = EATEN
                ghost.edible = False
                ghost.respawn = self.config.ghost_respawn_time
                self.score += self.config.points_per_ghost
                events.append(Event(EV_GHOST_EATEN, ghost.nearest_cell,
                                    self.config.points_per_ghost))
            elif not (self.cheats.enabled and self.cheats.invincible):
                self.lives -= 1
                events.append(Event(EV_PLAYER_DIED))
                return
