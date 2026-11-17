"""Ghost behaviour.

Each ghost has its own personality (as in the original game):

* blinky: chases the player directly;
* pinky: ambushes, aiming a few cells ahead of the player;
* inky: unpredictable, mixes chasing with random turns;
* clyde: chases from afar but retreats to its corner when close.

Every decision is taken at a cell centre and uses breadth first search
distances on the maze graph, so ghosts always follow real corridors.
"""

from __future__ import annotations

import random

from .entities import EATEN, Ghost, Player
from .maze import DX, DY, NONE, Cell, Maze, opposite

AMBUSH_DISTANCE = 4
CLYDE_SHY_DISTANCE = 8
INKY_CHASE_PROBABILITY = 0.6
FRIGHTENED_FLEE_PROBABILITY = 0.75


def _best(options: list[int], ghost: Ghost, maze: Maze, target: Cell,
          rng: random.Random, maximize: bool = False) -> int:
    """Pick the option whose next cell is nearest (or farthest) to target."""
    dist = maze.distances_from(target)
    scored: list[tuple[int, int]] = []
    for d in options:
        nx, ny = ghost.x + DX[d], ghost.y + DY[d]
        value = dist[ny][nx]
        scored.append((-value if maximize else value, d))
    best = min(score for score, _ in scored)
    ties = [d for score, d in scored if score == best]
    return rng.choice(ties)


def _ahead(maze: Maze, player: Player, steps: int) -> Cell:
    """The cell ``steps`` cells ahead of the player (stops at walls)."""
    x, y = player.nearest_cell
    direction = player.direction if player.direction != NONE \
        else player.facing
    for _ in range(steps):
        if not maze.can_move(x, y, direction):
            break
        x, y = x + DX[direction], y + DY[direction]
    return (x, y)


def choose_direction(ghost: Ghost, maze: Maze, player: Player,
                     rng: random.Random) -> int:
    """Decide where ``ghost`` goes next from its current cell centre."""
    dirs = maze.open_directions(ghost.x, ghost.y)
    if not dirs:
        return NONE
    if ghost.mode == EATEN:  # eyes may turn around to reach home
        return _best(dirs, ghost, maze, ghost.home, rng)
    back = opposite(ghost.direction)
    options = [d for d in dirs if d != back] or dirs
    if len(options) == 1:
        return options[0]
    target = player.nearest_cell
    if ghost.edible:
        if rng.random() < FRIGHTENED_FLEE_PROBABILITY:
            return _best(options, ghost, maze, target, rng, maximize=True)
        return rng.choice(options)
    kind = ghost.kind
    if kind == "pinky":
        return _best(options, ghost, maze,
                     _ahead(maze, player, AMBUSH_DISTANCE), rng)
    if kind == "inky" and rng.random() > INKY_CHASE_PROBABILITY:
        return rng.choice(options)
    if kind == "clyde":
        here = maze.distances_from(target)[ghost.y][ghost.x]
        if here <= CLYDE_SHY_DISTANCE:
            return _best(options, ghost, maze, ghost.home, rng)
    return _best(options, ghost, maze, target, rng)
