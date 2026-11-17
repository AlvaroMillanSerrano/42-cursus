"""Backend for the 42 ``mlx`` Python wrapper (MiniLibX).

Only calls that exist in MLX are used: window, image, key hooks, loop
hook. The whole frame is written into one MLX image and shown with a
single ``mlx_put_image_to_window``.
"""

from __future__ import annotations

import time
from typing import Any

from ..canvas import Canvas
from .base import TARGET_FPS, Application, Backend, BackendError

# X11 key symbols (what MiniLibX reports on Linux)
_SPECIAL = {
    65307: "escape", 65293: "enter", 65421: "enter", 32: "space",
    65288: "backspace", 65289: "tab", 65361: "left", 65362: "up",
    65363: "right", 65364: "down",
}
_KEY_PRESS = 2
_KEY_RELEASE = 3
_DESTROY = 17


def translate_key(code: int) -> str | None:
    """Map an X11 key symbol to a backend independent key name."""
    if code in _SPECIAL:
        return _SPECIAL[code]
    if 97 <= code <= 122 or 48 <= code <= 57:
        return chr(code)
    if 65 <= code <= 90:
        return chr(code + 32)
    return None


class MlxBackend(Backend):
    """MiniLibX window."""

    name = "mlx"

    def __init__(self, width: int, height: int, title: str) -> None:
        """Open the MLX connection and a window of the given size."""
        try:
            from mlx import Mlx  # type: ignore[import-not-found,unused-ignore]
        except ImportError as exc:
            raise BackendError("the 'mlx' package is not installed") from exc
        self.width, self.height = width, height
        self._mlx: Any = Mlx()
        self._ptr: Any = self._mlx.mlx_init()
        if not self._ptr:
            raise BackendError(
                "mlx_init failed: is a display (X server) available?")
        self._win: Any = self._mlx.mlx_new_window(self._ptr, width, height,
                                                  title)
        if not self._win:
            raise BackendError("mlx_new_window failed")
        self._img: Any = self._mlx.mlx_new_image(self._ptr, width, height)
        info = self._mlx.mlx_get_data_addr(self._img)
        data, bpp, line = info[0], info[1], info[2]
        if bpp != 32:
            raise BackendError(f"unsupported MLX pixel depth: {bpp} bpp")
        view = memoryview(data)
        self._data = view if view.format == "B" else view.cast("B")
        self._line = line
        self._app: Application | None = None
        self._canvas: Canvas | None = None
        self._last = time.perf_counter()
        self._error: BaseException | None = None
        self._closed = False

    # -- frame --------------------------------------------------------------

    def _present(self, canvas: Canvas) -> None:
        if self._line == canvas.stride:
            self._data[0:len(canvas.buf)] = canvas.buf
        else:
            for y in range(canvas.height):
                src = y * canvas.stride
                dst = y * self._line
                self._data[dst:dst + canvas.stride] = \
                    canvas.buf[src:src + canvas.stride]
        self._mlx.mlx_put_image_to_window(self._ptr, self._win, self._img,
                                          0, 0)

    def _guard(self, error: BaseException) -> None:
        """Remember an exception raised inside a C callback and stop."""
        if self._error is None:
            self._error = error
        self._mlx.mlx_loop_exit(self._ptr)

    def _on_key_down(self, code: int, _param: Any) -> int:
        try:
            key = translate_key(code)
            if key is not None and self._app is not None:
                self._app.key_down(key)
        except Exception as exc:  # noqa: BLE001
            self._guard(exc)
        return 0

    def _on_key_up(self, code: int, _param: Any) -> int:
        try:
            key = translate_key(code)
            if key is not None and self._app is not None:
                self._app.key_up(key)
        except Exception as exc:  # noqa: BLE001
            self._guard(exc)
        return 0

    def _on_close(self, _param: Any) -> int:
        if self._app is not None:
            self._app.running = False
        self._mlx.mlx_loop_exit(self._ptr)
        return 0

    def _on_loop(self, _param: Any) -> int:
        app, canvas = self._app, self._canvas
        if app is None or canvas is None:
            return 0
        try:
            frame = 1.0 / TARGET_FPS
            now = time.perf_counter()
            if now - self._last < frame:
                time.sleep(frame - (now - self._last))
                now = time.perf_counter()
            dt = min(now - self._last, 0.1)
            self._last = now
            app.update(dt)
            if not app.running:
                self._mlx.mlx_loop_exit(self._ptr)
                return 0
            app.render(canvas)
            self._present(canvas)
        except Exception as exc:  # noqa: BLE001
            self._guard(exc)
        return 0

    def run(self, app: Application, canvas: Canvas) -> None:
        """Hook the callbacks and enter ``mlx_loop``."""
        self._app, self._canvas = app, canvas
        self._last = time.perf_counter()
        self._mlx.mlx_hook(self._win, _KEY_PRESS, 1, self._on_key_down,
                           None)
        self._mlx.mlx_hook(self._win, _KEY_RELEASE, 2, self._on_key_up,
                           None)
        self._mlx.mlx_hook(self._win, _DESTROY, 0, self._on_close, None)
        self._mlx.mlx_loop_hook(self._ptr, self._on_loop, None)
        self._mlx.mlx_loop(self._ptr)
        if self._error is not None:
            raise self._error

    def close(self) -> None:
        """Destroy image and window."""
        if self._closed:
            return
        self._closed = True
        for call, arg in (("mlx_destroy_image", self._img),
                          ("mlx_destroy_window", self._win)):
            try:
                getattr(self._mlx, call)(self._ptr, arg)
            except Exception:  # noqa: BLE001
                pass
        try:
            self._mlx.mlx_release(self._ptr)
        except Exception:  # noqa: BLE001
            pass
