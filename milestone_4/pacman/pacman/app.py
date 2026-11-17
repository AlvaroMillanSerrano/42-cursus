"""Application: screens, input handling and the game state machine.

Flow: Main menu > game > win or lose > enter name > main menu.
"""

from __future__ import annotations

import logging
import random

from . import keys
from .canvas import Canvas
from .config import Config
from .game import (EV_GHOST_EATEN, EV_LEVEL_COMPLETE, EV_PLAYER_DIED,
                   EV_TIME_UP, Game, MazeFactory)
from .highscores import NAME_MAX, HighScores
from .maze import E, N, NONE, S, W, MazeError, generate_with_retry
from .render import WHITE, YELLOW, Renderer

LOGGER = logging.getLogger("pacman.app")

WIN_W = 900
WIN_H = 700
TITLE = "Pac-Man"

# states
MENU = "menu"
HIGHSCORES = "highscores"
INSTRUCTIONS = "instructions"
READY = "ready"
PLAYING = "playing"
PAUSED = "paused"
DYING = "dying"
TIME_UP = "time_up"
LEVEL_DONE = "level_done"
NAME_ENTRY = "name_entry"
ERROR = "error"

READY_TIME = 2.0
DYING_TIME = 1.3
BANNER_TIME = 1.8
POPUP_TIME = 0.9

MENU_ITEMS = ["START GAME", "VIEW HIGHSCORES", "INSTRUCTIONS", "EXIT"]
PAUSE_ITEMS = ["RESUME THE GAME", "RETURN TO THE MAIN MENU"]

DIRECTION_KEYS = {
    keys.UP: N, "w": N, "z": N,
    keys.RIGHT: E, "d": E,
    keys.DOWN: S, "s": S,
    keys.LEFT: W, "a": W, "q": W,
}


class App:
    """The whole game application, driven by a graphics backend."""

    def __init__(self, config: Config, width: int = WIN_W,
                 height: int = WIN_H, rng: random.Random | None = None,
                 maze_factory: MazeFactory = generate_with_retry) -> None:
        """Build the application; highscores are loaded immediately."""
        self.config = config
        self.running = True
        self.rng = rng or random.Random()
        self.maze_factory = maze_factory
        self.renderer = Renderer(width, height)
        self.highscores = HighScores(config.highscore_filename)
        self.highscores.load()
        self.state = MENU
        self.time = 0.0
        self.state_timer = 0.0
        self.menu_index = 0
        self.pause_index = 0
        self.notice = ""
        self.error_message = ""
        self.game: Game | None = None
        self.name = ""
        self.won = False
        self.final_score = 0
        self.rank_note = ""
        self.popups: list[tuple[tuple[int, int], str, float]] = []

    # -- input --------

    def key_down(self, key: str) -> None:
        """Handle a key press according to the current state."""
        direction = DIRECTION_KEYS.get(key, NONE)
        game = self.game
        if (direction != NONE and game is not None
                and self.state in (READY, PLAYING, DYING, TIME_UP,
                                   LEVEL_DONE)):
            game.player.press(direction)
        handler = {
            MENU: self._key_menu, HIGHSCORES: self._key_back,
            INSTRUCTIONS: self._key_back, PLAYING: self._key_playing,
            PAUSED: self._key_paused, NAME_ENTRY: self._key_name,
            ERROR: self._key_back,
        }.get(self.state)
        if handler is not None:
            handler(key)

    def key_up(self, key: str) -> None:
        """Handle a key release (only direction keys matter)."""
        direction = DIRECTION_KEYS.get(key, NONE)
        if direction != NONE and self.game is not None:
            self.game.player.release(direction)

    def _key_menu(self, key: str) -> None:
        self.notice = ""
        if key in (keys.UP, "w"):
            self.menu_index = (self.menu_index - 1) % len(MENU_ITEMS)
        elif key in (keys.DOWN, "s"):
            self.menu_index = (self.menu_index + 1) % len(MENU_ITEMS)
        elif key in (keys.ENTER, keys.SPACE):
            if self.menu_index == 0:
                self._start_game()
            elif self.menu_index == 1:
                self.state = HIGHSCORES
            elif self.menu_index == 2:
                self.state = INSTRUCTIONS
            else:
                self.running = False

    def _key_back(self, key: str) -> None:
        if key in (keys.ENTER, keys.ESCAPE, keys.SPACE):
            self.state = MENU
            self.error_message = ""

    def _key_playing(self, key: str) -> None:
        game = self.game
        if game is None:
            return
        if key in (keys.ESCAPE, "p"):
            self.state = PAUSED
            self.pause_index = 0
            return
        if key == "c":
            game.cheats.enabled = not game.cheats.enabled
            return
        if not game.cheats.enabled:
            return
        if key == "i":
            game.cheats.invincible = not game.cheats.invincible
        elif key == "f":
            game.cheats.freeze = not game.cheats.freeze
        elif key == "h":
            game.cheats.fast = not game.cheats.fast
        elif key == "n":
            game.cheat_skip_level()
        elif key == "l":
            game.cheat_extra_life()

    def _key_paused(self, key: str) -> None:
        if key in (keys.ESCAPE, "p"):
            self.state = PLAYING
        elif key in (keys.UP, "w"):
            self.pause_index = (self.pause_index - 1) % len(PAUSE_ITEMS)
        elif key in (keys.DOWN, "s"):
            self.pause_index = (self.pause_index + 1) % len(PAUSE_ITEMS)
        elif key in (keys.ENTER, keys.SPACE):
            if self.pause_index == 0:
                self.state = PLAYING
            else:
                self.game = None
                self.state = MENU

    def _key_name(self, key: str) -> None:
        if key == keys.ENTER:
            self._save_score()
        elif key == keys.BACKSPACE:
            self.name = self.name[:-1]
        elif len(self.name) < NAME_MAX:
            if key == keys.SPACE:
                self.name += " "
            elif len(key) == 1 and key.isalnum():
                self.name += key.upper()

    # -- game flow --------

    def _fail(self, message: str) -> None:
        LOGGER.error("%s", message)
        self.error_message = message
        self.game = None
        self.state = ERROR

    def _start_game(self) -> None:
        game = Game(self.config, random.Random(self.rng.random()),
                    self.maze_factory)
        try:
            game.start_level(0)
        except MazeError as exc:
            self._fail(f"Could not create the maze: {exc}")
            return
        self.game = game
        self._enter_level()

    def _enter_level(self) -> None:
        if self.game is None:
            return
        self.renderer.prepare_level(self.game)
        self.popups = []
        self.state = READY
        self.state_timer = READY_TIME

    def _finish_game(self, won: bool) -> None:
        if self.game is None:
            return
        self.won = won
        self.final_score = self.game.score
        self.name = ""
        self.rank_note = ("A TOP 10 SCORE!"
                          if self.highscores.qualifies(self.final_score)
                          else "")
        self.game = None
        self.state = NAME_ENTRY

    def _save_score(self) -> None:
        rank = self.highscores.add(self.name, self.final_score)
        saved = self.highscores.save()
        if rank:
            self.notice = f"SCORE SAVED - RANK {rank}"
        else:
            self.notice = "SCORE NOT IN THE TOP 10"
        if not saved:
            self.notice = "COULD NOT WRITE THE HIGHSCORE FILE"
        self.state = MENU
        self.menu_index = 0

    def _next_level(self) -> None:
        game = self.game
        if game is None:
            return
        following = game.level_index + 1
        if following >= game.level_count:
            self._finish_game(True)
            return
        try:
            game.start_level(following)
        except MazeError as exc:
            self._fail(f"Could not create the maze: {exc}")
            return
        self._enter_level()

    # -- update --------

    def update(self, dt: float) -> None:
        """Advance timers and the game by ``dt`` seconds."""
        self.time += dt
        self.popups = [(c, t, left - dt) for c, t, left in self.popups
                       if left - dt > 0.0]
        game = self.game
        if game is None:
            return
        if self.state == PLAYING:
            self._update_playing(game, dt)
        elif self.state in (READY, DYING, TIME_UP, LEVEL_DONE):
            self.state_timer -= dt
            if self.state_timer <= 0.0:
                self._timer_expired(game)

    def _update_playing(self, game: Game, dt: float) -> None:
        for event in game.update(dt):
            if event.kind == EV_GHOST_EATEN:
                self.popups.append((event.cell, str(event.points),
                                    POPUP_TIME))
            elif event.kind == EV_PLAYER_DIED:
                self.state, self.state_timer = DYING, DYING_TIME
            elif event.kind == EV_TIME_UP:
                self.state, self.state_timer = TIME_UP, BANNER_TIME
            elif event.kind == EV_LEVEL_COMPLETE:
                self.state, self.state_timer = LEVEL_DONE, BANNER_TIME

    def _timer_expired(self, game: Game) -> None:
        if self.state == READY:
            self.state = PLAYING
        elif self.state == DYING:
            if game.lives <= 0:
                self._finish_game(False)
            else:
                game.reset_positions()
                self.state, self.state_timer = READY, READY_TIME
        elif self.state == TIME_UP:
            if game.lives <= 0:
                self._finish_game(False)
            else:
                game.restart_level()
                self._enter_level()
        elif self.state == LEVEL_DONE:
            self._next_level()

    # -- drawing --------

    def render(self, canvas: Canvas) -> None:
        """Draw the current frame."""
        r = self.renderer
        state = self.state
        if state == MENU:
            r.draw_menu(canvas, MENU_ITEMS, self.menu_index,
                        self.highscores.entries, self.notice, self.time)
        elif state == HIGHSCORES:
            r.draw_highscores(canvas, self.highscores.entries)
        elif state == INSTRUCTIONS:
            r.draw_instructions(canvas)
        elif state == NAME_ENTRY:
            title = "YOU WIN!" if self.won else "GAME OVER"
            r.draw_name_entry(canvas, title, self.final_score, self.name,
                              int(self.time * 2) % 2 == 0, self.rank_note)
        elif state == ERROR:
            r.draw_error(canvas, self.error_message)
        elif self.game is not None:
            self._render_game(canvas, self.game)

    def _render_game(self, canvas: Canvas, game: Game) -> None:
        r = self.renderer
        dying = None
        if self.state == DYING:
            dying = 1.0 - max(self.state_timer, 0.0) / DYING_TIME
        r.draw_game(canvas, game, self.time, dying)
        for cell, text, _ in self.popups:
            r.draw_popup(canvas, cell, text)
        if self.state == READY:
            r.draw_banner(canvas, [
                (f"LEVEL {game.level_index + 1}", WHITE, 3),
                ("READY!", YELLOW, 5)])
        elif self.state == TIME_UP:
            r.draw_banner(canvas, [("TIME UP!", YELLOW, 5)])
        elif self.state == LEVEL_DONE:
            r.draw_banner(canvas, [
                (f"LEVEL {game.level_index + 1} COMPLETE!", YELLOW, 4)])
        elif self.state == PAUSED:
            r.draw_pause_menu(canvas, PAUSE_ITEMS, self.pause_index)
