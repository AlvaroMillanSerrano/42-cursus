"""Tests for the maze generator adapter."""

from __future__ import annotations

import random

import pytest

import pacman.maze as maze_module
from pacman.maze import (E, N, NONE, S, W, MazeError, build_maze,
                         generate_maze, generate_with_retry, opposite)


def test_generated_maze_is_playable() -> None:
    maze = generate_maze(21, 15, 42)
    assert (maze.width, maze.height) == (21, 15)
    assert maze.is_free(*maze.start)
    assert len(maze.corners) == 4
    for corner in maze.corners:
        assert maze.is_free(*corner)
    dist = maze.distances_from(maze.start)
    for x, y in maze.free_cells():
        assert dist[y][x] < maze_module.UNREACHABLE


def test_fixed_seed_is_reproducible_and_random_differs() -> None:
    a, b = generate_maze(21, 15, 42), generate_maze(21, 15, 42)
    assert a.walls == b.walls
    assert generate_maze(21, 15, 43).walls != a.walls


def test_dead_ends_only_touch_the_42_block() -> None:
    """perfect=False removes dead ends, except next to the '42' cells.

    That is a property of the assigned package (it cannot open walls
    towards the closed '42' cells), so the game must cope with them.
    """
    for seed in (1, 5, 42, 99):
        maze = generate_maze(25, 17, seed)
        for x, y in maze.free_cells():
            if len(maze.open_directions(x, y)) < 2:
                near = [(x + maze_module.DX[d], y + maze_module.DY[d])
                        for d in range(4)]
                assert any(maze.in_bounds(a, b) and not maze.free[b][a]
                           for a, b in near)


def test_moves_are_symmetric() -> None:
    maze = generate_maze(19, 13, 3)
    for x, y in maze.free_cells():
        for d in maze.open_directions(x, y):
            nx, ny = x + maze_module.DX[d], y + maze_module.DY[d]
            assert maze.can_move(nx, ny, opposite(d))


def test_border_is_closed() -> None:
    maze = generate_maze(17, 13, 9)
    assert not maze.can_move(0, 0, N) and not maze.can_move(0, 0, W)
    assert not maze.can_move(16, 12, S) and not maze.can_move(16, 12, E)
    assert not maze.can_move(0, 0, NONE)


def test_bad_grids_raise_maze_error() -> None:
    with pytest.raises(MazeError):
        build_maze([[0, 0]], 3, 3)
    with pytest.raises(MazeError):
        build_maze([[15] * 4 for _ in range(4)], 4, 4)
    with pytest.raises(MazeError):
        build_maze([["x"] * 3 for _ in range(3)], 3, 3)  # type: ignore


def test_generator_crash_is_wrapped(monkeypatch: pytest.MonkeyPatch) -> None:
    import mazegenerator

    def boom(*_: object, **__: object) -> None:
        raise RuntimeError("kaboom")

    monkeypatch.setattr(mazegenerator, "MazeGenerator", boom)
    with pytest.raises(MazeError, match="kaboom"):
        generate_maze(21, 15, 1)


def test_retry_recovers_from_a_flaky_generator(
        monkeypatch: pytest.MonkeyPatch) -> None:
    real = maze_module.generate_maze
    calls = {"n": 0}

    def flaky(w: int, h: int, seed: int = 0) -> maze_module.Maze:
        calls["n"] += 1
        if calls["n"] < 3:
            raise MazeError("nope")
        return real(w, h, seed)

    monkeypatch.setattr(maze_module, "generate_maze", flaky)
    maze = generate_with_retry(21, 15, 0, random.Random(1))
    assert calls["n"] == 3 and maze.width == 21
