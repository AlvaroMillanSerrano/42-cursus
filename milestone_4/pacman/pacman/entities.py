"""Moving entities: the player and the four ghosts.

Entities live on the maze graph. ``(x, y)`` is the cell an entity is
leaving and ``progress`` (0..1) how far it is towards the next cell, so
movement is smooth and speeds are expressed in cells per second.
"""

from __future__ import annotations

from typing import Callable

from .maze import DX, DY, NONE, Cell, Maze, opposite

# ghost modes
WAITING = "waiting"  # standing at the corner until released
ACTIVE = "active"    # roaming the maze
EATEN = "eaten"      # eyes returning home / waiting to respawn

PERSONALITIES = ("blinky", "pinky", "inky", "clyde")

Chooser = Callable[["Mover"], int]


class Mover:
    """Something that walks along corridors at a given speed."""

    def __init__(self, cell: Cell) -> None:
        """Place the mover exactly on ``cell``, standing still."""
        self.x, self.y = cell
        self.direction = NONE
        self.progress = 0.0

    @property
    def cell(self) -> Cell:
        """The cell the mover is leaving (or standing on)."""
        return (self.x, self.y)

    @property
    def position(self) -> tuple[float, float]:
        """Exact position in cell units."""
        if self.direction == NONE:
            return (float(self.x), float(self.y))
        return (self.x + DX[self.direction] * self.progress,
                self.y + DY[self.direction] * self.progress)

    @property
    def nearest_cell(self) -> Cell:
        """The cell whose centre is closest to the mover."""
        px, py = self.position
        return (int(px + 0.5), int(py + 0.5))

    def place(self, cell: Cell) -> None:
        """Teleport to ``cell`` and stop."""
        self.x, self.y = cell
        self.direction = NONE
        self.progress = 0.0

    def reverse(self) -> None:
        """Turn around, even in the middle of a corridor."""
        if self.direction == NONE:
            return
        if self.progress > 1e-9:
            self.x += DX[self.direction]
            self.y += DY[self.direction]
            self.progress = 1.0 - self.progress
        self.direction = opposite(self.direction)

    def advance(self, distance: float, choose: Chooser) -> None:
        """Move ``distance`` cells, asking ``choose`` at every cell centre."""
        guard = 0
        while distance > 1e-9 and guard < 16:
            guard += 1
            if self.progress <= 1e-9:
                self.progress = 0.0
                self.direction = choose(self)
                if self.direction == NONE:
                    return
            step = min(distance, 1.0 - self.progress)
            self.progress += step
            distance -= step
            if self.progress >= 1.0 - 1e-9:
                self.x += DX[self.direction]
                self.y += DY[self.direction]
                self.progress = 0.0


class Player(Mover):
    """Pac-Man. Direction requests are buffered until they are possible."""

    def __init__(self, cell: Cell) -> None:
        """Create the player on ``cell``."""
        super().__init__(cell)
        self.desired = NONE
        self.facing = 1
        self.anim = 0.0
        self.held: list[int] = []

    def press(self, direction: int) -> None:
        """A direction key went down: remember it and react at once."""
        if direction in self.held:
            self.held.remove(direction)
        self.held.append(direction)
        self.desired = direction
        if (self.progress > 1e-9 and self.direction != NONE
                and direction == opposite(self.direction)):
            self.reverse()  # reversing never has to wait for a junction

    def release(self, direction: int) -> None:
        """A direction key went up."""
        if direction in self.held:
            self.held.remove(direction)
        if self.desired == direction and self.direction == direction \
                and self.held:
            self.desired = self.held[-1]

    def reset(self, cell: Cell) -> None:
        """Back to the start cell; keys still held keep steering."""
        self.place(cell)
        self.facing = 1
        self.desired = self.held[-1] if self.held else NONE

    def choose(self, maze: Maze) -> Chooser:
        """Return the junction decision function for this player."""
        def decide(_: Mover) -> int:
            if self.desired != NONE and maze.can_move(self.x, self.y,
                                                      self.desired):
                self.facing = self.desired
                return self.desired
            if self.direction != NONE and maze.can_move(self.x, self.y,
                                                        self.direction):
                self.facing = self.direction
                return self.direction
            return NONE
        return decide


class Ghost(Mover):
    """One of the four ghosts."""

    def __init__(self, index: int, home: Cell) -> None:
        """Create ghost number ``index`` standing on its ``home`` corner."""
        super().__init__(home)
        self.index = index
        self.kind = PERSONALITIES[index % len(PERSONALITIES)]
        self.home = home
        self.mode = WAITING
        self.edible = False
        self.wait = 0.0
        self.respawn = 0.0

    def send_home(self, wait: float) -> None:
        """Put the ghost back on its corner, released after ``wait`` s."""
        self.place(self.home)
        self.mode = WAITING
        self.edible = False
        self.wait = wait
        self.respawn = 0.0
