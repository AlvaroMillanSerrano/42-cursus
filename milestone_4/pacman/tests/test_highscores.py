"""Tests for the highscore table."""

from __future__ import annotations

import json
from pathlib import Path

from pacman.highscores import MAX_ENTRIES, HighScores, sanitize_name


def test_sanitize_name() -> None:
    assert sanitize_name("  Bob!!  ") == "Bob"
    assert sanitize_name("a" * 30) == "a" * 10
    assert sanitize_name("") == "PLAYER"
    assert sanitize_name("é$%") == "PLAYER"
    assert sanitize_name("A B") == "A B"


def test_add_sorts_and_keeps_top_ten(tmp_path: Path) -> None:
    table = HighScores(str(tmp_path / "hs.json"))
    for score in range(0, 150, 10):
        table.add(f"P{score}", score)
    assert len(table.entries) == MAX_ENTRIES
    assert table.entries[0].score == 140
    assert table.entries[-1].score == 50
    assert table.add("LOW", 1) == 0
    assert not table.qualifies(50)
    assert table.qualifies(51)


def test_ties_keep_older_first(tmp_path: Path) -> None:
    table = HighScores(str(tmp_path / "hs.json"))
    table.add("OLD", 100)
    assert table.add("NEW", 100) == 2
    assert [e.name for e in table.entries] == ["OLD", "NEW"]


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "sub" / "hs.json"
    table = HighScores(str(path))
    table.add("ANA", 500)
    assert table.save()
    other = HighScores(str(path))
    other.load()
    assert other.entries == table.entries
    assert not list(path.parent.glob("*.tmp"))


def test_missing_file_is_fine(tmp_path: Path) -> None:
    table = HighScores(str(tmp_path / "nope.json"))
    table.load()
    assert table.entries == []


def test_corrupt_files_do_not_crash(tmp_path: Path) -> None:
    path = tmp_path / "hs.json"
    for content in ("{ broken", "42", '{"scores": 3}', ""):
        path.write_text(content, encoding="utf-8")
        table = HighScores(str(path))
        table.load()
        assert table.entries == []


def test_invalid_entries_are_dropped(tmp_path: Path) -> None:
    path = tmp_path / "hs.json"
    payload = {"scores": [
        {"name": "OK", "score": 10}, {"name": "NEG", "score": -1},
        {"name": 5, "score": 3}, {"name": "BOOL", "score": True},
        {"name": "FLOAT", "score": 1.5}, "junk",
        {"name": "x" * 40, "score": 7}]}
    path.write_text(json.dumps(payload), encoding="utf-8")
    table = HighScores(str(path))
    table.load()
    assert [(e.name, e.score) for e in table.entries] == [
        ("OK", 10), ("x" * 10, 7)]


def test_save_failure_returns_false(tmp_path: Path) -> None:
    blocker = tmp_path / "file"
    blocker.write_text("x", encoding="utf-8")
    table = HighScores(str(blocker / "hs.json"))
    table.add("A", 1)
    assert table.save() is False
