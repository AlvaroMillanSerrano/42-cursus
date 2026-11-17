"""Common interface of the graphics backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from ..canvas import Canvas

TARGET_FPS = 60


class BackendError(Exception):
    """A graphics backend could not be started."""


class Application(Protocol):
    """What a backend needs from the game application."""

    running: bool

    def key_down(self, key: str) -> None:
        """A key was pressed."""

    def key_up(self, key: str) -> None:
        """A key was released."""

    def update(self, dt: float) -> None:
        """Advance the application by ``dt`` seconds."""

    def render(self, canvas: Canvas) -> None:
        """Draw the current frame into ``canvas``."""


class Backend(ABC):
    """A window that shows a :class:`Canvas` and reports key events."""

    name = "base"

    @abstractmethod
    def run(self, app: Application, canvas: Canvas) -> None:
        """Run the main loop until ``app.running`` becomes false."""

    @abstractmethod
    def close(self) -> None:
        """Release every window and resource."""
