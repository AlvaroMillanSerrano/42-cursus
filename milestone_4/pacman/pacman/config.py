"""Configuration loading.

The configuration file is JSON that additionally accepts comments:

* lines whose first non-blank character is ``#``;
* ``// line`` comments;
* ``/* block */`` comments.

Problems with the *file* (missing, unreadable, not a JSON object) raise
:class:`ConfigError`. Problems with individual *values* never stop the
game: the value is clamped or replaced by its default and a warning is
logged.
"""

from __future__ import annotations

import json
import logging
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger("pacman.config")

MIN_LEVELS = 10
MIN_WIDTH, MAX_WIDTH = 14, 61  # 14x10 is the smallest size holding the "42"
MIN_HEIGHT, MAX_HEIGHT = 10, 41
MAX_SEED = 2 ** 31 - 1
BACKENDS = ("auto", "mlx", "pygame")

_DEFAULT_SIZES = [(17, 13), (19, 13), (19, 15), (21, 15), (21, 15),
                  (23, 15), (23, 17), (25, 17), (25, 19), (27, 19)]


class ConfigError(Exception):
    """The configuration file cannot be used at all."""


@dataclass(frozen=True)
class LevelConfig:
    """Parameters of one level."""

    width: int
    height: int
    seed: int = 0  # 0 means "random"
    time: int = 0  # 0 means "use level_max_time"


@dataclass
class Config:
    """Validated game configuration."""

    highscore_filename: str = "highscores.json"
    lives: int = 3
    pacgum: int = 0  # 0 means "a pacgum in every free corridor cell"
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
    power_time: float = 8.0
    ghost_respawn_time: float = 5.0
    player_speed: float = 7.0
    ghost_speed: float = 5.5
    cheat_mode: bool = False
    backend: str = "auto"
    levels: list[LevelConfig] = field(default_factory=list)

    def level_time(self, index: int) -> int:
        """Time limit in seconds of level ``index``."""
        level = self.levels[index]
        return level.time if level.time > 0 else self.level_max_time

    def level_seed(self, index: int) -> int:
        """Seed of level ``index`` (0 = random)."""
        level = self.levels[index]
        if level.seed > 0:
            return level.seed
        return self.seed if index == 0 else 0


def default_levels() -> list[LevelConfig]:
    """Return the built-in list of ten levels."""
    return [LevelConfig(w, h) for w, h in _DEFAULT_SIZES]


# -- comment stripping ------------------------------------------------------

def strip_comments(text: str) -> str:
    """Remove ``#``, ``//`` and ``/* */`` comments from JSON text.

    String literals are respected, and newlines are preserved so error
    messages keep the original line numbers.
    """
    out: list[str] = []
    i, n = 0, len(text)
    in_string = False
    line_blank = True  # only whitespace seen so far on this line
    while i < n:
        c = text[i]
        if in_string:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 1
            elif c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
            line_blank = False
        elif c == "#" and line_blank:
            while i < n and text[i] != "\n":
                i += 1
            continue
        elif c == "/" and text[i:i + 2] == "//":
            while i < n and text[i] != "\n":
                i += 1
            continue
        elif c == "/" and text[i:i + 2] == "/*":
            end = text.find("*/", i + 2)
            end = n if end == -1 else end + 2
            out.append("\n" * text.count("\n", i, end))
            i = end
            continue
        if c == "\n":
            line_blank = True
        elif not c.isspace():
            line_blank = False
        out.append(c)
        i += 1
    return "".join(out)


# -- value helpers ----------------------------------------------------------

def _warn(message: str) -> None:
    LOGGER.warning(message)


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value) \
            and value.is_integer():
        return int(value)
    return None


def _as_float(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    result = float(value)
    return result if math.isfinite(result) else None


def _int_option(data: dict[str, Any], key: str, default: int,
                low: int, high: int, label: str = "") -> int:
    """Read an integer, clamping it into ``[low, high]``."""
    if key not in data:
        return default
    name = label or key
    value = _as_int(data[key])
    if value is None:
        _warn(f"'{name}': expected an integer, got {data[key]!r}; "
              f"using default {default}")
        return default
    if value < low or value > high:
        clamped = min(max(value, low), high)
        _warn(f"'{name}': {value} is out of range [{low}, {high}]; "
              f"using {clamped}")
        return clamped
    return value


def _float_option(data: dict[str, Any], key: str, default: float,
                  low: float, high: float) -> float:
    """Read a number, clamping it into ``[low, high]``."""
    if key not in data:
        return default
    value = _as_float(data[key])
    if value is None:
        _warn(f"'{key}': expected a number, got {data[key]!r}; "
              f"using default {default}")
        return default
    if value < low or value > high:
        clamped = min(max(value, low), high)
        _warn(f"'{key}': {value} is out of range [{low}, {high}]; "
              f"using {clamped}")
        return clamped
    return value


def _bool_option(data: dict[str, Any], key: str, default: bool) -> bool:
    if key not in data:
        return default
    value = data[key]
    if isinstance(value, bool):
        return value
    _warn(f"'{key}': expected true or false, got {value!r}; "
          f"using default {default}")
    return default


def _str_option(data: dict[str, Any], key: str, default: str) -> str:
    if key not in data:
        return default
    value = data[key]
    if isinstance(value, str) and value.strip() and "\0" not in value:
        return value.strip()
    _warn(f"'{key}': expected a non-empty string, got {value!r}; "
          f"using default {default!r}")
    return default


def _parse_levels(raw: Any) -> list[LevelConfig]:
    """Validate the ``levels`` array and pad it to ``MIN_LEVELS``."""
    defaults = default_levels()
    if raw is None:
        return defaults
    if not isinstance(raw, list) or not raw:
        _warn("'levels': expected a non-empty array; using defaults")
        return defaults
    levels: list[LevelConfig] = []
    for index, entry in enumerate(raw):
        fallback = defaults[min(index, len(defaults) - 1)]
        if not isinstance(entry, dict):
            _warn(f"'levels[{index}]': expected an object; "
                  f"using the default level")
            levels.append(fallback)
            continue
        label = f"levels[{index}]."
        width = _int_option(entry, "width", fallback.width,
                            MIN_WIDTH, MAX_WIDTH, label + "width")
        height = _int_option(entry, "height", fallback.height,
                             MIN_HEIGHT, MAX_HEIGHT, label + "height")
        seed = _int_option(entry, "seed", 0, 0, MAX_SEED, label + "seed")
        time = _int_option(entry, "time", 0, 0, 3600, label + "time")
        levels.append(LevelConfig(width, height, seed, time))
    if len(levels) < MIN_LEVELS:
        _warn(f"'levels': {len(levels)} given but the game needs at least "
              f"{MIN_LEVELS}; adding default levels")
        for index in range(len(levels), MIN_LEVELS):
            levels.append(defaults[index])
    return levels


def parse_config(raw: Any) -> Config:
    """Build a :class:`Config` from decoded JSON, fixing bad values."""
    if not isinstance(raw, dict):
        raise ConfigError("the configuration must be a JSON object "
                          "(e.g. { \"lives\": 3 })")
    backend = _str_option(raw, "backend", "auto").lower()
    if backend not in BACKENDS:
        _warn(f"'backend': {backend!r} is not one of {BACKENDS}; "
              f"using 'auto'")
        backend = "auto"
    return Config(
        highscore_filename=_str_option(raw, "highscore_filename",
                                       "highscores.json"),
        lives=_int_option(raw, "lives", 3, 1, 99),
        pacgum=_int_option(raw, "pacgum", 0, 0, 5000),
        points_per_pacgum=_int_option(raw, "points_per_pacgum", 10,
                                      0, 100000),
        points_per_super_pacgum=_int_option(raw, "points_per_super_pacgum",
                                            50, 0, 100000),
        points_per_ghost=_int_option(raw, "points_per_ghost", 200,
                                     0, 100000),
        seed=_int_option(raw, "seed", 42, 0, MAX_SEED),
        level_max_time=_int_option(raw, "level_max_time", 90, 5, 3600),
        power_time=_float_option(raw, "power_time", 8.0, 1.0, 60.0),
        ghost_respawn_time=_float_option(raw, "ghost_respawn_time", 5.0,
                                         1.0, 60.0),
        player_speed=_float_option(raw, "player_speed", 7.0, 2.0, 15.0),
        ghost_speed=_float_option(raw, "ghost_speed", 5.5, 1.0, 15.0),
        cheat_mode=_bool_option(raw, "cheat_mode", False),
        backend=backend,
        levels=_parse_levels(raw.get("levels")),
    )


def load_config(path: str) -> Config:
    """Read, decode and validate the configuration file at ``path``."""
    file = Path(path)
    try:
        text = file.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ConfigError(f"configuration file not found: {path}") from None
    except IsADirectoryError:
        raise ConfigError(f"{path} is a directory, not a file") from None
    except PermissionError:
        raise ConfigError(f"no permission to read {path}") from None
    except (OSError, UnicodeDecodeError) as exc:
        raise ConfigError(f"cannot read {path}: {exc}") from None
    try:
        raw = json.loads(strip_comments(text))
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"{path} is not valid JSON (line {exc.lineno}, column "
            f"{exc.colno}): {exc.msg}") from None
    return parse_config(raw)
