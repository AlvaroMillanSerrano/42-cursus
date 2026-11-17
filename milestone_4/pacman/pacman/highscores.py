"""Persistent top-10 highscore table stored as JSON."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger("pacman.highscores")

MAX_ENTRIES = 10
NAME_MAX = 10
DEFAULT_NAME = "PLAYER"
MAX_SCORE = 10 ** 12


@dataclass(frozen=True)
class Entry:
    """One line of the highscore table."""

    name: str
    score: int


def sanitize_name(raw: str) -> str:
    """Keep ASCII letters, digits and spaces; trim to ``NAME_MAX``.

    An empty result falls back to ``DEFAULT_NAME``.
    """
    kept = "".join(c for c in str(raw)
                   if (c.isascii() and c.isalnum()) or c == " ")
    kept = kept.strip()[:NAME_MAX].strip()
    return kept or DEFAULT_NAME


class HighScores:
    """Load, update and save the top ``MAX_ENTRIES`` scores."""

    def __init__(self, path: str) -> None:
        """Create an empty table bound to the file ``path``."""
        self.path = Path(path)
        self.entries: list[Entry] = []

    # -- persistence --------------------------------------------------------

    def load(self) -> None:
        """Read the file; any problem results in an empty/partial table."""
        self.entries = []
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return
        except (OSError, UnicodeDecodeError) as exc:
            LOGGER.warning("cannot read highscores (%s): %s",
                           self.path, exc)
            return
        try:
            raw: Any = json.loads(text)
        except json.JSONDecodeError as exc:
            LOGGER.warning("highscore file %s is corrupted (%s); "
                           "starting with an empty table", self.path, exc)
            return
        items = raw.get("scores") if isinstance(raw, dict) else raw
        if not isinstance(items, list):
            LOGGER.warning("highscore file %s has an unknown format; "
                           "ignoring it", self.path)
            return
        for item in items:
            entry = self._parse_entry(item)
            if entry is not None:
                self.entries.append(entry)
        self.entries.sort(key=lambda e: -e.score)
        del self.entries[MAX_ENTRIES:]

    @staticmethod
    def _parse_entry(item: Any) -> Entry | None:
        if not isinstance(item, dict):
            return None
        name, score = item.get("name"), item.get("score")
        if not isinstance(name, str):
            return None
        if isinstance(score, bool) or not isinstance(score, int):
            return None
        if score < 0 or score > MAX_SCORE:
            return None
        return Entry(sanitize_name(name), score)

    def save(self) -> bool:
        """Write the table atomically. Return ``False`` on failure."""
        payload = {"scores": [{"name": e.name, "score": e.score}
                              for e in self.entries]}
        tmp_name = ""
        try:
            directory = self.path.parent
            directory.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                    "w", encoding="utf-8", dir=directory,
                    prefix=".highscores-", suffix=".tmp",
                    delete=False) as tmp:
                tmp_name = tmp.name
                json.dump(payload, tmp, indent=2)
            os.replace(tmp_name, self.path)
            return True
        except OSError as exc:
            LOGGER.warning("cannot save highscores to %s: %s",
                           self.path, exc)
            if tmp_name:
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass
            return False

    # -- table logic --------------------------------------------------------

    def qualifies(self, score: int) -> bool:
        """Would ``score`` enter the table?"""
        if score < 0:
            return False
        if len(self.entries) < MAX_ENTRIES:
            return True
        return score > self.entries[-1].score

    def add(self, name: str, score: int) -> int:
        """Insert a score and return its 1-based rank (0 if not kept).

        Ties keep the older entry ahead.
        """
        score = max(0, int(score))
        entry = Entry(sanitize_name(name), score)
        position = len(self.entries)
        for index, existing in enumerate(self.entries):
            if score > existing.score:
                position = index
                break
        self.entries.insert(position, entry)
        del self.entries[MAX_ENTRIES:]
        return position + 1 if position < MAX_ENTRIES else 0
