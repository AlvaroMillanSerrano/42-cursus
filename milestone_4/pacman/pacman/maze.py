"""Adapter between the assigned ``mazegenerator`` package and the game.

The generator is used *as is*; this module adapts to its interface.

Cell encoding used by the generator: each cell is an int whose low four
bits are walls (bit set = wall): N=1, E=2, S=4, W=8. A value of 15 is a
fully closed cell (the "42" pattern). The grid is indexed ``[y][x]``.
Here directions are the integers 0=N, 1=E, 2=S, 3=W, so the wall bit of
direction ``d`` is ``1 << d``.
"""

from __future__ import annotations

import contextlib
import io
import logging
import random
from collections import deque
from dataclasses import dataclass, field

LOGGER = logging.getLogger("pacman.maze")

NONE = -1
N, E, S, W = 0, 1, 2, 3
DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)
UNREACHABLE = 10 ** 6

Cell = tuple[int, int]
DistMap = list[list[int]]


def opposite(direction: int) -> int:
    """Return the opposite direction (``NONE`` stays ``NONE``)."""
    return NONE if direction == NONE else (direction + 2) % 4


class MazeError(Exception):
    """The maze generator failed or produced an unusable maze."""


@dataclass
class Maze:
    """A playable maze: walls, free cells, spawn points."""

    width: int
    height: int
    walls: list[list[int]]
    free: list[list[bool]]
    start: Cell
    corners: list[Cell]
    seed: int = 0
    _dist_cache: dict[Cell, DistMap] = field(
        default_factory=dict, repr=False)

    def in_bounds(self, x: int, y: int) -> bool:
        """Is ``(x, y)`` inside the grid?"""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, x: int, y: int) -> bool:
        """Can entities stand in cell ``(x, y)``?"""
        return self.in_bounds(x, y) and self.free[y][x]

    def can_move(self, x: int, y: int, direction: int) -> bool:
        """Is there an open passage from ``(x, y)`` in ``direction``?"""
        if direction == NONE or not self.is_free(x, y):
            return False
        nx, ny = x + DX[direction], y + DY[direction]
        if not self.is_free(nx, ny):
            return False
        bit = 1 << direction
        back = 1 << opposite(direction)
        return not (self.walls[y][x] & bit) and not (self.walls[ny][nx] & back)

    def open_directions(self, x: int, y: int) -> list[int]:
        """All directions leaving ``(x, y)`` through an open passage."""
        return [d for d in range(4) if self.can_move(x, y, d)]

    def free_cells(self) -> list[Cell]:
        """Every walkable cell, row by row."""
        return [(x, y) for y in range(self.height)
                for x in range(self.width) if self.free[y][x]]

    def distances_from(self, cell: Cell) -> DistMap:
        """BFS distance (in cells) from ``cell`` to every cell (cached)."""
        cached = self._dist_cache.get(cell)
        if cached is not None:
            return cached
        dist = [[UNREACHABLE] * self.width for _ in range(self.height)]
        if self.is_free(*cell):
            dist[cell[1]][cell[0]] = 0
            queue: deque[Cell] = deque([cell])
            while queue:
                x, y = queue.popleft()
                base = dist[y][x] + 1
                for d in range(4):
                    if self.can_move(x, y, d):
                        nx, ny = x + DX[d], y + DY[d]
                        if dist[ny][nx] > base:
                            dist[ny][nx] = base
                            queue.append((nx, ny))
        if len(self._dist_cache) > 400:
            self._dist_cache.clear()
        self._dist_cache[cell] = dist
        return dist


def _nearest_free(free: list[list[bool]], width: int, height: int,
                  target: tuple[float, float]) -> Cell | None:
    best: Cell | None = None
    best_d = float("inf")
    for y in range(height):
        for x in range(width):
            if free[y][x]:
                d = (x - target[0]) ** 2 + (y - target[1]) ** 2
                if d < best_d:
                    best, best_d = (x, y), d
    return best


def build_maze(grid: list[list[int]], width: int, height: int,
               seed: int = 0) -> Maze:
    """Turn a raw generator grid into a :class:`Maze`.

    Raises :class:`MazeError` if the grid is malformed or too small.
    """
    if (len(grid) != height
            or any(len(row) != width for row in grid)):
        raise MazeError("the generator returned a grid of unexpected size")
    for row in grid:
        for value in row:
            if not isinstance(value, int):
                raise MazeError("the generator returned non integer cells")
    free = [[(value & 0xF) != 15 for value in row] for row in grid]
    walls = [[value & 0xF for value in row] for row in grid]
    centre = ((width - 1) / 2.0, (height - 1) / 2.0)
    start = _nearest_free(free, width, height, centre)
    if start is None:
        raise MazeError("the generated maze has no free cells")
    maze = Maze(width, height, walls, free, start, [], seed)
    # keep only the cells connected to the start
    reach = maze.distances_from(start)
    for y in range(height):
        for x in range(width):
            if free[y][x] and reach[y][x] >= UNREACHABLE:
                free[y][x] = False
    maze._dist_cache.clear()
    cells = maze.free_cells()
    if len(cells) < 8:
        raise MazeError("the generated maze is too small to play")
    corner_targets = [(0, 0), (width - 1, 0), (0, height - 1),
                      (width - 1, height - 1)]
    for cx, cy in corner_targets:
        if free[cy][cx]:
            maze.corners.append((cx, cy))
        else:
            best = min(cells, key=lambda c: (c[0] - cx) ** 2
                       + (c[1] - cy) ** 2)
            maze.corners.append(best)
    return maze


def generate_maze(width: int, height: int, seed: int = 0) -> Maze:
    """Generate a Pac-Man compatible maze with the assigned package.

    ``seed`` > 0 gives a reproducible maze, 0 a random one. The generator
    is called with ``perfect=False`` as required by the subject.
    """
    try:
        from mazegenerator import MazeGenerator
    except ImportError as exc:
        raise MazeError(
            "the 'mazegenerator' package is not installed; run "
            "'make install' (it installs the provided .whl)") from exc
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            generator = MazeGenerator(
                size=(width, height), perfect=False, entry_cell=(0, 0),
                exit_cell=(width - 1, height - 1), seed=seed)
            grid = [list(row) for row in generator.maze]
    except Exception as exc:  # the package is third party: never trust it
        raise MazeError(f"the maze generator failed: {exc}") from exc
    noise = buffer.getvalue().strip()
    if noise:
        LOGGER.warning("maze generator says: %s", noise)
    return build_maze(grid, width, height, seed)


def generate_with_retry(width: int, height: int, seed: int,
                        rng: random.Random, attempts: int = 3) -> Maze:
    """Like :func:`generate_maze` but retries random mazes on failure."""
    last: MazeError | None = None
    for attempt in range(attempts):
        try_seed = seed
        if seed <= 0:
            try_seed = rng.randint(1, 2 ** 31 - 1)
        try:
            return generate_maze(width, height, try_seed)
        except MazeError as exc:
            last = exc
            LOGGER.warning("maze generation attempt %d failed: %s",
                           attempt + 1, exc)
            if seed > 0:
                break
    assert last is not None
    raise last
