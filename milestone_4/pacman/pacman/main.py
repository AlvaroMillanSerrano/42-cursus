"""Command line entry point."""

from __future__ import annotations

import logging
import os
import sys
import traceback

from .app import TITLE, WIN_H, WIN_W, App
from .backends import BackendError, create_backend
from .canvas import Canvas
from .config import ConfigError, load_config

USAGE = "usage: python3 pac-man.py <config.json>"


def main(argv: list[str]) -> int:
    """Run the game. Return the process exit code."""
    logging.basicConfig(level=logging.WARNING,
                        format="%(levelname)s: %(message)s",
                        stream=sys.stderr)
    if len(argv) != 2:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        config = load_config(argv[1])
    except ConfigError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    try:
        backend = create_backend(config.backend, WIN_W, WIN_H, TITLE)
    except BackendError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("Hint: install the MLX wheel (make install) and make sure a "
              "display is available (X11/WSLg).", file=sys.stderr)
        return 1
    try:
        backend.run(App(config), Canvas(WIN_W, WIN_H))
    except KeyboardInterrupt:
        pass
    except Exception as exc:  # last line of defence: never show a traceback
        print(f"Fatal error: {exc}", file=sys.stderr)
        if os.environ.get("PACMAN_DEBUG"):
            traceback.print_exc()
        return 1
    finally:
        backend.close()
    return 0
