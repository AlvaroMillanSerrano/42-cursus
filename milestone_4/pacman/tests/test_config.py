"""Tests for the configuration loader."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from pacman.config import (ConfigError, load_config, parse_config,
                           strip_comments)


def test_hash_slash_and_block_comments_are_removed() -> None:
    text = '# comment\n{"a": 1, // note\n /* x\n y */ "b": "#kept // too"}'
    assert json.loads(strip_comments(text)) == {"a": 1, "b": "#kept // too"}


def test_comment_stripping_keeps_line_numbers() -> None:
    text = "# one\n/* two\nthree */\n{oops}"
    assert strip_comments(text).count("\n") == text.count("\n")


def test_defaults_when_empty() -> None:
    cfg = parse_config({})
    assert cfg.lives == 3 and cfg.points_per_pacgum == 10
    assert len(cfg.levels) == 10 and cfg.seed == 42


def test_invalid_values_are_fixed_and_logged(
        caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        cfg = parse_config({"lives": "three", "points_per_ghost": -5,
                            "level_max_time": 10 ** 9, "cheat_mode": 1,
                            "backend": "sdl", "unknown_key": 1})
    assert cfg.lives == 3
    assert cfg.points_per_ghost == 0
    assert cfg.level_max_time == 3600
    assert cfg.cheat_mode is False
    assert cfg.backend == "auto"
    assert "lives" in caplog.text and "unknown_key" not in caplog.text


def test_bool_is_not_an_int() -> None:
    assert parse_config({"lives": True}).lives == 3


def test_levels_are_clamped_and_padded() -> None:
    cfg = parse_config({"levels": [{"width": 3, "height": 999}, "x"]})
    assert len(cfg.levels) == 10
    assert cfg.levels[0].width == 14 and cfg.levels[0].height == 41


def test_seed_rules() -> None:
    cfg = parse_config({"seed": 7, "levels": [{"width": 15, "height": 11,
                                               "seed": 9}]})
    assert cfg.level_seed(0) == 9
    assert cfg.level_seed(1) == 0
    assert parse_config({"seed": 7}).level_seed(0) == 7


def test_not_an_object_is_an_error() -> None:
    with pytest.raises(ConfigError):
        parse_config([1, 2])


def test_load_errors_are_clean(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not found"):
        load_config(str(tmp_path / "missing.json"))
    with pytest.raises(ConfigError, match="directory"):
        load_config(str(tmp_path))
    bad = tmp_path / "bad.json"
    bad.write_text("{ not json", encoding="utf-8")
    with pytest.raises(ConfigError, match="line 1"):
        load_config(str(bad))
    binary = tmp_path / "bin.json"
    binary.write_bytes(b"\xff\xfe\x00")
    with pytest.raises(ConfigError):
        load_config(str(binary))


def test_load_valid_file_with_comments(tmp_path: Path) -> None:
    file = tmp_path / "c.json"
    file.write_text('# hi\n{"lives": 5 // five\n}', encoding="utf-8")
    assert load_config(str(file)).lives == 5
