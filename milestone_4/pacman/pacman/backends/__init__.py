"""Graphics backends and the factory that picks one."""

from __future__ import annotations

import logging
import os

from .base import Application, Backend, BackendError

LOGGER = logging.getLogger("pacman.backends")

__all__ = ["Application", "Backend", "BackendError", "create_backend"]


def create_backend(preferred: str, width: int, height: int,
                   title: str) -> Backend:
    """Open a window with the requested backend.

    ``preferred`` is ``"mlx"``, ``"pygame"`` or ``"auto"`` (MLX first,
    pygame as a fallback). The environment variable ``PACMAN_BACKEND``
    overrides the configuration.
    """
    choice = os.environ.get("PACMAN_BACKEND", preferred).strip().lower()
    order = {"mlx": ["mlx"], "pygame": ["pygame"]}.get(choice,
                                                       ["mlx", "pygame"])
    errors: list[str] = []
    for name in order:
        try:
            if name == "mlx":
                from .mlx_backend import MlxBackend
                return MlxBackend(width, height, title)
            from .pygame_backend import PygameBackend
            return PygameBackend(width, height, title)
        except BackendError as exc:
            LOGGER.info("backend %s unavailable: %s", name, exc)
            errors.append(f"{name}: {exc}")
    raise BackendError("no graphics backend could be started ("
                       + "; ".join(errors) + ")")
