"""Optional development backend based on pygame.

It only uses features with a direct MLX equivalent: open a window,
receive key events, and show one finished image per frame (the same as
``mlx_put_image_to_window``). Everything else is drawn by the game's own
software canvas.
"""

from __future__ import annotations

from typing import Any

from ..canvas import Canvas
from .base import TARGET_FPS, Application, Backend, BackendError

_NAMES = {
    "K_ESCAPE": "escape", "K_RETURN": "enter", "K_KP_ENTER": "enter",
    "K_SPACE": "space", "K_BACKSPACE": "backspace", "K_TAB": "tab",
    "K_LEFT": "left", "K_RIGHT": "right", "K_UP": "up", "K_DOWN": "down",
}


class PygameBackend(Backend):
    """pygame window."""

    name = "pygame"

    def __init__(self, width: int, height: int, title: str) -> None:
        """Open a pygame window of the given size."""
        try:
            import pygame
        except ImportError as exc:
            raise BackendError("pygame is not installed") from exc
        self._pg: Any = pygame
        try:
            pygame.display.init()
            self._screen = pygame.display.set_mode((width, height))
        except pygame.error as exc:
            raise BackendError(f"cannot open a pygame window: {exc}") \
                from exc
        pygame.display.set_caption(title)
        self.width, self.height = width, height
        self._keymap: dict[int, str] = {
            getattr(pygame, name): key for name, key in _NAMES.items()}

    def _translate(self, code: int) -> str | None:
        if code in self._keymap:
            return self._keymap[code]
        if 97 <= code <= 122 or 48 <= code <= 57:
            return chr(code)
        return None

    def run(self, app: Application, canvas: Canvas) -> None:
        """Main loop: events, update, draw, show."""
        pg = self._pg
        clock = pg.time.Clock()
        size = (canvas.width, canvas.height)
        while app.running:
            dt = min(clock.tick(TARGET_FPS) / 1000.0, 0.1)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    app.running = False
                elif event.type == pg.KEYDOWN:
                    key = self._translate(event.key)
                    if key is not None:
                        app.key_down(key)
                elif event.type == pg.KEYUP:
                    key = self._translate(event.key)
                    if key is not None:
                        app.key_up(key)
            app.update(dt)
            if not app.running:
                break
            app.render(canvas)
            image = pg.image.frombuffer(canvas.buf, size, "BGRA")
            self._screen.blit(image, (0, 0))
            pg.display.flip()

    def close(self) -> None:
        """Shut pygame down."""
        try:
            self._pg.display.quit()
        except Exception:  # noqa: BLE001
            pass
