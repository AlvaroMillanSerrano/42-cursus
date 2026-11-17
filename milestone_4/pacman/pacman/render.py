"""Drawing of the game scene, HUD and menu screens onto a Canvas."""

from __future__ import annotations

import math
from typing import Callable

from .canvas import Canvas, Color
from .entities import EATEN, Ghost
from .game import Game
from .highscores import Entry
from .maze import DX, DY, NONE, Maze

HUD_H = 56
MARGIN = 10

BLACK = 0x000000
WHITE = 0xFFFFFF
YELLOW = 0xFFFF00
WALL = 0x2121DE
SOLID = 0x0B0B55
DOT = 0xFFB8AE
BLUE = 0x2121FF
CYAN = 0x00FFFF
RED = 0xFF3030
GREY = 0x9090A0
GREEN = 0x40FF40
GHOST_COLORS = {"blinky": 0xFF0000, "pinky": 0xFFB8FF,
                "inky": 0x00FFFF, "clyde": 0xFFB852}

Painter = Callable[[Canvas], None]


class Renderer:
    """Knows how to draw every screen of the game."""

    def __init__(self, width: int, height: int) -> None:
        """Create the renderer for a ``width`` x ``height`` window."""
        self.width = width
        self.height = height
        self.static = Canvas(width, height)
        self.level = Canvas(width, height)
        self.hud = Canvas(width, HUD_H)
        self.cell = 20
        self.ox = 0
        self.oy = HUD_H
        self._hud_key: tuple[object, ...] | None = None
        self._drawn_pacgums: set[tuple[int, int]] = set()
        self._cache = Canvas(width, height)
        self._cache_key: tuple[object, ...] | None = None

    # -- level preparation --------

    def prepare_level(self, game: Game) -> None:
        """Pre-render walls and pacgums of the current level."""
        maze = game.current_maze
        area_w = self.width - 2 * MARGIN
        area_h = self.height - HUD_H - 2 * MARGIN
        self.cell = max(6, min(area_w // maze.width,
                               area_h // maze.height, 48))
        self.ox = (self.width - self.cell * maze.width) // 2
        free_h = self.height - HUD_H
        self.oy = HUD_H + (free_h - self.cell * maze.height) // 2
        self.static.clear(BLACK)
        self._draw_walls(self.static, maze)
        self.level.copy_from(self.static)
        self._drawn_pacgums = set(game.pacgums)
        radius = max(2, self.cell // 10)
        for cell in self._drawn_pacgums:
            px, py = self._centre(cell[0], cell[1])
            self.level.fill_circle(px, py, radius, DOT)
        self._hud_key = None

    def _centre(self, x: float, y: float) -> tuple[int, int]:
        """Pixel position of the centre of cell coordinates ``(x, y)``."""
        return (int(self.ox + (x + 0.5) * self.cell),
                int(self.oy + (y + 0.5) * self.cell))

    def _draw_walls(self, canvas: Canvas, maze: Maze) -> None:
        cs = self.cell
        thick = max(2, cs // 10)
        half = thick // 2
        for y in range(maze.height):
            for x in range(maze.width):
                px, py = self.ox + x * cs, self.oy + y * cs
                if not maze.free[y][x] and maze.walls[y][x] == 15:
                    canvas.fill_rect(px, py, cs, cs, SOLID)
        for y in range(maze.height):
            for x in range(maze.width):
                px, py = self.ox + x * cs, self.oy + y * cs
                bits = maze.walls[y][x]
                if bits & 1:
                    canvas.fill_rect(px - half, py - half, cs + thick,
                                     thick, WALL)
                if bits & 8:
                    canvas.fill_rect(px - half, py - half, thick,
                                     cs + thick, WALL)
                if bits & 4 and y == maze.height - 1:
                    canvas.fill_rect(px - half, py + cs - half, cs + thick,
                                     thick, WALL)
                if bits & 2 and x == maze.width - 1:
                    canvas.fill_rect(px + cs - half, py - half, thick,
                                     cs + thick, WALL)

    # -- game scene --------

    def draw_game(self, canvas: Canvas, game: Game, t: float,
                  dying: float | None = None) -> None:
        """Draw maze, entities and HUD.

        ``dying`` (0..1) animates the player's death; ``None`` is normal.
        """
        erased = self._drawn_pacgums - game.pacgums
        for cell in erased:
            px, py = self._centre(cell[0], cell[1])
            half = self.cell // 2 + 1
            self.level.copy_rect_from(self.static, px - half, py - half,
                                      2 * half + 1, 2 * half + 1)
        self._drawn_pacgums -= erased
        canvas.copy_from(self.level)
        if int(t * 4) % 2 == 0:
            for cell in game.supers:
                px, py = self._centre(cell[0], cell[1])
                canvas.fill_circle(px, py, max(4, self.cell // 4), DOT)
        if dying is None:
            for ghost in game.ghosts:
                self._draw_ghost(canvas, ghost, game, t)
        self._draw_player(canvas, game, t, dying)
        self._draw_hud(canvas, game)

    def _draw_player(self, canvas: Canvas, game: Game, t: float,
                     dying: float | None) -> None:
        player = game.player
        px, py = self._centre(*player.position)
        radius = int(self.cell * 0.42)
        if dying is not None:
            radius = int(radius * max(0.0, 1.0 - dying))
            if radius > 0:
                canvas.fill_pacman(px, py, radius, player.facing, 0.0,
                                   YELLOW)
            return
        if player.direction == NONE:
            mouth = 22.0
        else:
            mouth = 4.0 + 40.0 * abs(math.sin(player.anim))
        canvas.fill_pacman(px, py, radius, player.facing, mouth, YELLOW)

    def _draw_ghost(self, canvas: Canvas, ghost: Ghost, game: Game,
                    t: float) -> None:
        px, py = self._centre(*ghost.position)
        r = int(self.cell * 0.42)
        direction = ghost.direction if ghost.direction != NONE else 3
        if ghost.mode == EATEN:
            self._draw_eyes(canvas, px, py, r, direction)
            return
        if ghost.edible:
            flash = game.power_time_left < 2.0 and int(t * 6) % 2 == 0
            color = WHITE if flash else BLUE
            self._ghost_body(canvas, px, py, r, color, int(t * 8) % 2)
            eye = max(1, r // 5)
            face = 0xFFB8AE if not flash else RED
            canvas.fill_rect(px - r // 3 - eye // 2, py - r // 4, eye + 1,
                             eye + 1, face)
            canvas.fill_rect(px + r // 3 - eye // 2, py - r // 4, eye + 1,
                             eye + 1, face)
            for i in range(5):
                canvas.fill_rect(px - r // 2 + i * (r // 4 + 1),
                                 py + r // 4 + (i % 2) * 2, max(1, r // 5),
                                 max(1, r // 6), face)
            return
        self._ghost_body(canvas, px, py, r, GHOST_COLORS[ghost.kind],
                         int(t * 8) % 2)
        self._draw_eyes(canvas, px, py, r, direction)

    @staticmethod
    def _ghost_body(canvas: Canvas, px: int, py: int, r: int,
                    color: Color, phase: int) -> None:
        limit = (r + 0.5) ** 2
        for dy in range(-r, 1):
            half = int(math.sqrt(max(limit - dy * dy, 0.0)))
            canvas.fill_rect(px - half, py + dy, 2 * half + 1, 1, color)
        canvas.fill_rect(px - r, py + 1, 2 * r + 1, max(1, r - 2), color)
        seg = (2 * r + 1) / 5.0
        for i in range(5):
            if (i + phase) % 2 == 0:
                x0 = px - r + int(i * seg)
                x1 = px - r + int((i + 1) * seg)
                canvas.fill_rect(x0, py + r - 1, x1 - x0, 2, color)

    @staticmethod
    def _draw_eyes(canvas: Canvas, px: int, py: int, r: int,
                   direction: int) -> None:
        eye = max(2, r // 3)
        pupil = max(1, eye // 2)
        for side in (-1, 1):
            ex = px + side * int(r * 0.42)
            ey = py - int(r * 0.2)
            canvas.fill_circle(ex, ey, eye, WHITE)
            canvas.fill_circle(ex + DX[direction] * (eye - pupil),
                               ey + DY[direction] * (eye - pupil),
                               pupil, BLUE)

    # -- HUD ------------------------------------------------------------------

    def _draw_hud(self, canvas: Canvas, game: Game) -> None:
        cheats = game.cheats.active()
        key = (game.score, game.lives, game.level_index,
               math.ceil(game.time_left), tuple(cheats),
               game.cheats.enabled)
        if key != self._hud_key:
            self._hud_key = key
            self._render_hud(game, cheats)
        canvas.blit_top(self.hud)

    def _render_hud(self, game: Game, cheats: list[str]) -> None:
        hud = self.hud
        hud.clear(BLACK)
        hud.fill_rect(0, HUD_H - 2, self.width, 2, WALL)
        hud.draw_text(16, 8, "SCORE", WHITE, 2)
        hud.draw_text(16 + 6 * 12 + 4, 8, f"{game.score:07d}", YELLOW, 2)
        level = f"LEVEL {game.level_index + 1}/{game.level_count}"
        hud.draw_text_centered(self.width // 2, 8, level, WHITE, 2)
        seconds = max(0, math.ceil(game.time_left))
        colour = RED if seconds <= 10 else WHITE
        text = f"TIME {seconds:03d}"
        hud.draw_text(self.width - 16 - hud.text_width(text, 2), 8, text,
                      colour, 2)
        hud.draw_text(16, 34, "LIVES", WHITE, 1)
        if game.lives <= 8:
            for i in range(max(0, game.lives)):
                hud.fill_pacman(66 + i * 22, 38, 8, 1, 35.0, YELLOW)
        else:
            hud.fill_pacman(70, 38, 8, 1, 35.0, YELLOW)
            hud.draw_text(84, 34, f"X{game.lives}", YELLOW, 1)
        if game.cheats.enabled:
            label = "CHEAT " + (" ".join(cheats) if cheats else "ON")
            hud.draw_text_centered(self.width // 2, 34, label, GREEN, 1)

    # -- overlays --------

    def draw_banner(self, canvas: Canvas,
                    lines: list[tuple[str, Color, int]]) -> None:
        """Draw a framed box with centred lines ``(text, colour, scale)``."""
        width = max(canvas.text_width(t, s) for t, _, s in lines) + 48
        height = sum(canvas.text_height(s) + 10 for _, _, s in lines) + 30
        x = (self.width - width) // 2
        y = HUD_H + (self.height - HUD_H - height) // 2
        canvas.fill_rect(x - 4, y - 4, width + 8, height + 8, YELLOW)
        canvas.fill_rect(x, y, width, height, BLACK)
        cursor = y + 20
        for text, colour, scale in lines:
            canvas.draw_text_centered(self.width // 2, cursor, text, colour,
                                      scale)
            cursor += canvas.text_height(scale) + 10

    def draw_popup(self, canvas: Canvas, cell: tuple[int, int],
                   text: str) -> None:
        """Draw a short floating score text at a maze cell."""
        px, py = self._centre(cell[0], cell[1])
        canvas.draw_text_centered(px, py - 6, text, CYAN, 2)

    # -- full screens (cached: they only change on input) ---------------------

    def _cached(self, canvas: Canvas, key: tuple[object, ...],
                painter: Painter) -> None:
        if key != self._cache_key:
            self._cache.clear(BLACK)
            painter(self._cache)
            self._cache_key = key
        canvas.copy_from(self._cache)

    def draw_menu(self, canvas: Canvas, items: list[str], index: int,
                  entries: list[Entry], notice: str, t: float) -> None:
        """Main menu with the highscore table underneath."""
        key = ("menu", index, tuple(entries), notice)

        def paint(c: Canvas) -> None:
            c.draw_text_centered(self.width // 2, 34, "PAC-MAN", YELLOW, 9)
            c.draw_text_centered(self.width // 2, 110,
                                 "GHOSTS! MORE GHOSTS!", GREY, 2)
            y = 190
            for i, item in enumerate(items):
                colour = YELLOW if i == index else WHITE
                label = ("> " if i == index else "  ") + item
                c.draw_text(self.width // 2 - 150, y, label, colour, 3)
                y += 38
            c.draw_text_centered(self.width // 2, y + 6,
                                 "UP/DOWN + ENTER (OR SPACE)", GREY, 1)
            c.draw_text_centered(self.width // 2, y + 28, "HIGHSCORES:",
                                 CYAN, 2)
            y += 54
            if not entries:
                c.draw_text_centered(self.width // 2, y, "NO SCORES YET",
                                     GREY, 2)
            for rank, entry in enumerate(entries, start=1):
                line = f"{rank}. {entry.name} - {entry.score} PTS"
                c.draw_text(self.width // 2 - 150, y, line, WHITE, 2)
                y += 18
            if notice:
                c.draw_text_centered(self.width // 2, self.height - 24,
                                     notice, GREEN, 2)

        self._cached(canvas, key, paint)
        self._draw_parade(canvas, t)

    def _draw_parade(self, canvas: Canvas, t: float) -> None:
        """Pac-Man chasing the four ghosts along the top of the menu."""
        span = self.width + 400
        x = int((t * 140) % span) - 300
        y = 162
        canvas.fill_pacman(x, y, 14, 1, 4.0 + 40.0 * abs(math.sin(t * 12)),
                           YELLOW)
        for i, kind in enumerate(("blinky", "pinky", "inky", "clyde")):
            self._ghost_body(canvas, x - 50 - i * 40, y, 13,
                             GHOST_COLORS[kind], int(t * 8) % 2)
            self._draw_eyes(canvas, x - 50 - i * 40, y, 13, 1)

    def draw_highscores(self, canvas: Canvas,
                        entries: list[Entry]) -> None:
        """Full top-10 screen."""
        def paint(c: Canvas) -> None:
            c.draw_text_centered(self.width // 2, 50, "HIGHSCORES", YELLOW,
                                 6)
            y = 150
            if not entries:
                c.draw_text_centered(self.width // 2, y + 40,
                                     "NO SCORES YET", GREY, 3)
            for rank, entry in enumerate(entries, start=1):
                line = f"{rank}. {entry.name} - {entry.score} PTS"
                c.draw_text(self.width // 2 - 220, y, line, WHITE, 3)
                y += 40
            c.draw_text_centered(self.width // 2, self.height - 40,
                                 "PRESS ENTER OR ESC TO GO BACK", GREY, 2)

        self._cached(canvas, ("scores", tuple(entries)), paint)

    def draw_instructions(self, canvas: Canvas) -> None:
        """Controls and rules."""
        def paint(c: Canvas) -> None:
            cx = self.width // 2
            c.draw_text_centered(cx, 24, "INSTRUCTIONS", YELLOW, 5)
            rows = [
                ("CONTROLS", CYAN),
                ("ARROWS OR WASD (ZQSD): MOVE", WHITE),
                ("P OR ESC: PAUSE / RESUME", WHITE),
                ("", WHITE),
                ("RULES", CYAN),
                ("EAT ALL THE PACGUMS TO WIN THE LEVEL", WHITE),
                ("SUPER PACGUMS (CORNERS) MAKE GHOSTS EDIBLE", WHITE),
                ("TOUCHING A GHOST COSTS A LIFE", WHITE),
                ("BEAT THE CLOCK AND ALL LEVELS TO WIN", WHITE),
                ("", WHITE),
                ("CHEAT MODE (FOR REVIEWERS)", GREEN),
                ("C: TOGGLE CHEAT MODE   I: INVINCIBLE", WHITE),
                ("F: FREEZE GHOSTS   H: FAST PLAYER", WHITE),
                ("N: SKIP LEVEL   L: EXTRA LIFE", WHITE),
            ]
            y = 100
            for text, colour in rows:
                c.draw_text_centered(cx, y, text, colour, 2)
                y += 26
            c.draw_text_centered(cx, self.height - 40,
                                 "PRESS ENTER OR ESC TO GO BACK", GREY, 2)

        self._cached(canvas, ("instructions",), paint)

    def draw_pause_menu(self, canvas: Canvas, items: list[str],
                        index: int) -> None:
        """Pause menu drawn over the (frozen) game scene."""
        lines: list[tuple[str, Color, int]] = [("PAUSED", YELLOW, 4)]
        for i, item in enumerate(items):
            label = ("> " if i == index else "  ") + item
            lines.append((label, YELLOW if i == index else WHITE, 2))
        self.draw_banner(canvas, lines)

    def draw_name_entry(self, canvas: Canvas, title: str, score: int,
                        name: str, blink: bool, rank_note: str) -> None:
        """Game over / victory screen with name prompt."""
        key = ("name", title, score, name, blink, rank_note)

        def paint(c: Canvas) -> None:
            cx = self.width // 2
            colour = GREEN if title == "YOU WIN!" else RED
            c.draw_text_centered(cx, 90, title, colour, 8)
            if title == "YOU WIN!":
                c.draw_text_centered(cx, 170, "CONGRATULATIONS! ALL LEVELS "
                                     "CLEARED", YELLOW, 2)
            c.draw_text_centered(cx, 230, f"FINAL SCORE: {score}", WHITE, 4)
            c.draw_text_centered(cx, 330, "ENTER YOUR NAME:", CYAN, 3)
            shown = name + ("_" if blink else " ")
            c.draw_text_centered(cx, 390, shown, YELLOW, 5)
            c.draw_text_centered(cx, 480, "LETTERS, DIGITS AND SPACES - "
                                 "MAX 10", GREY, 2)
            c.draw_text_centered(cx, 510, "ENTER TO SAVE", GREY, 2)
            if rank_note:
                c.draw_text_centered(cx, 560, rank_note, GREEN, 2)

        self._cached(canvas, key, paint)

    def draw_error(self, canvas: Canvas, message: str) -> None:
        """Error screen (for example when the maze generator fails)."""
        def paint(c: Canvas) -> None:
            cx = self.width // 2
            c.draw_text_centered(cx, 120, "SOMETHING WENT WRONG", RED, 4)
            y = 220
            for line in _wrap(message, 60):
                c.draw_text_centered(cx, y, line, WHITE, 2)
                y += 26
            c.draw_text_centered(cx, self.height - 60,
                                 "PRESS ENTER TO GO BACK TO THE MENU",
                                 GREY, 2)

        self._cached(canvas, ("error", message), paint)


def _wrap(text: str, width: int) -> list[str]:
    """Greedy word wrap."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        if current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return lines or [""]
