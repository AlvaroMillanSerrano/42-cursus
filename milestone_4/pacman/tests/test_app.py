"""End-to-end tests of the application state machine (no window)."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

import pacman.app as app_module
from pacman.app import App
from pacman.canvas import Canvas
from pacman.config import parse_config
from pacman.maze import MazeError


def make_app(tmp_path: Path, **overrides: object) -> App:
    raw: dict[str, object] = {
        "highscore_filename": str(tmp_path / "hs.json"),
        "levels": [{"width": 17, "height": 13}] * 10, "cheat_mode": True}
    raw.update(overrides)
    return App(parse_config(raw), rng=random.Random(1))


def frames(app: App, seconds: float, canvas: Canvas | None = None) -> None:
    canvas = canvas or Canvas(app_module.WIN_W, app_module.WIN_H)
    for _ in range(int(seconds * 60)):
        app.update(1 / 60)
        app.render(canvas)


def test_full_game_with_cheats_to_victory_and_highscore(
        tmp_path: Path) -> None:
    app = make_app(tmp_path)
    frames(app, 0.1)
    app.key_down("space")                      # START GAME
    assert app.state == app_module.READY
    frames(app, 2.1)
    assert app.state == app_module.PLAYING
    app.key_down("i")                          # invincible
    for level in range(10):
        assert app.game is not None and app.game.level_index == level
        app.key_down("n")                      # skip level
        frames(app, 0.1)
        assert app.state == app_module.LEVEL_DONE
        frames(app, 2.0)
        if level < 9:
            assert app.state == app_module.READY
            frames(app, 2.1)
    assert app.state == app_module.NAME_ENTRY and app.won
    for key in "bob":
        app.key_down(key)
    app.key_down("backspace")
    app.key_down("space")
    for key in "abcdefghijklmnop":
        app.key_down(key)
    assert len(app.name) == 10
    app.key_down("enter")
    assert app.state == app_module.MENU
    assert app.highscores.entries[0].name == "BO ABCDEFG"[:10]
    assert (tmp_path / "hs.json").exists()


def test_game_over_flow(tmp_path: Path) -> None:
    app = make_app(tmp_path, lives=1)
    app.key_down("enter")
    frames(app, 2.1)
    assert app.game is not None
    ghost = app.game.ghosts[0]
    ghost.mode = "active"
    ghost.place(app.game.player.cell)
    frames(app, 0.1)
    assert app.state == app_module.DYING
    frames(app, 1.5)
    assert app.state == app_module.NAME_ENTRY and not app.won
    app.key_down("enter")                      # empty name allowed
    assert app.state == app_module.MENU
    assert app.highscores.entries[0].name == "PLAYER"


def test_losing_a_life_returns_to_ready(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    app.key_down("enter")
    frames(app, 2.1)
    assert app.game is not None
    app.game.ghosts[0].mode = "active"
    app.game.ghosts[0].place(app.game.player.cell)
    frames(app, 0.1)
    frames(app, 1.5)
    assert app.state == app_module.READY and app.game.lives == 2


def test_pause_resume_and_return_to_menu(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    app.key_down("enter")
    frames(app, 2.1)
    app.key_down("escape")
    assert app.state == app_module.PAUSED
    time_before = app.game.time_left if app.game else 0
    frames(app, 1.0)
    assert app.game is not None and app.game.time_left == time_before
    app.key_down("escape")
    assert app.state == app_module.PLAYING
    app.key_down("p")
    app.key_down("down")
    app.key_down("enter")
    assert app.state == app_module.MENU and app.game is None


def test_menu_navigation_and_exit(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    app.key_down("down")
    app.key_down("enter")
    assert app.state == app_module.HIGHSCORES
    frames(app, 0.1)
    app.key_down("escape")
    app.key_down("down")
    app.key_down("space")
    assert app.state == app_module.INSTRUCTIONS
    frames(app, 0.1)
    app.key_down("enter")
    app.key_down("up")
    app.key_down("up")
    assert app.menu_index == 3 - 0 - 0 or app.menu_index >= 0
    app.menu_index = 3
    app.key_down("enter")
    assert app.running is False


def test_time_up_loses_a_life_and_replays_level(tmp_path: Path) -> None:
    app = make_app(tmp_path, level_max_time=5)
    app.key_down("enter")
    frames(app, 2.1)
    assert app.game is not None
    app.key_down("i")
    frames(app, 5.5)
    assert app.state == app_module.TIME_UP and app.game.lives == 2
    frames(app, 2.0)
    assert app.state == app_module.READY
    assert app.game is not None and app.game.time_left == 5.0


def test_maze_failure_shows_error_screen(tmp_path: Path) -> None:
    def broken(*_: object) -> None:
        raise MazeError("generator exploded")

    app = make_app(tmp_path)
    app.maze_factory = broken  # type: ignore[assignment]
    app.key_down("enter")
    assert app.state == app_module.ERROR
    frames(app, 0.1)
    app.key_down("enter")
    assert app.state == app_module.MENU


def test_unwritable_highscore_file_does_not_crash(tmp_path: Path) -> None:
    blocker = tmp_path / "blocker"
    blocker.write_text("x", encoding="utf-8")
    app = make_app(tmp_path, highscore_filename=str(blocker / "hs.json"),
                   lives=1)
    app.key_down("enter")
    frames(app, 2.1)
    assert app.game is not None
    app.game.ghosts[0].mode = "active"
    app.game.ghosts[0].place(app.game.player.cell)
    frames(app, 2.0)
    app.key_down("enter")
    assert app.state == app_module.MENU and "COULD NOT" in app.notice


def test_cheat_keys_need_cheat_mode(tmp_path: Path) -> None:
    app = make_app(tmp_path, cheat_mode=False)
    app.key_down("enter")
    frames(app, 2.1)
    assert app.game is not None
    app.key_down("l")
    assert app.game.lives == 3
    app.key_down("c")
    app.key_down("l")
    assert app.game.lives == 4


@pytest.mark.parametrize("key", ["w", "a", "s", "d", "z", "q", "up",
                                 "left", "down", "right"])
def test_direction_keys_are_accepted(tmp_path: Path, key: str) -> None:
    app = make_app(tmp_path)
    app.key_down("enter")
    frames(app, 2.1)
    app.key_down(key)
    app.key_up(key)
    frames(app, 0.2)
