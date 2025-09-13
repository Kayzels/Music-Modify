"""Tests for Song."""

# pyright: reportUnusedParameter = false

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from music_modify.custom_types import Song
from music_modify.custom_types.songtag import SongTag

logger = logging.getLogger(__name__)


def test_Song_init_with_None(table_tags: list[SongTag]) -> None:
    """Test that a Song object is created correctly when not passed a file."""
    song = Song(table_tags, table_tags, "")
    assert song.file is None
    info: list[str] = ["" for _ in range(len(table_tags))]
    assert song.display_info == info


def test_Song_init_with_file(song_path: Path) -> None:
    """Test that a Song object is created correctly when passed a file."""
    song = Song([], [], "", file=song_path)
    assert song.file == song_path
    assert hasattr(song, "display_info")
    assert isinstance(song.display_info, list)


def test_Song_columns_setTag_removeTag(
    song_path: Path, table_tags: list[SongTag]
) -> None:
    """Test that setting and then removing tags works."""
    song = Song(table_tags, table_tags, "; ", song_path)
    song.setTag("TIT2", ["Some Title"])
    song.setTag("TCOM", ["Some Composer", "Another Composer"])
    assert song.hasTag("TIT2")
    assert song.hasTag("TCOM")
    song.updateInfo()
    expected_output: list[str] = []
    for col in table_tags:
        if col.id3_key == "TIT2":
            expected_output.append("Some Title")
        elif col.id3_key == "TCOM":
            expected_output.append("Some Composer; Another Composer")
        else:
            expected_output.append("")
    assert song.display_info == expected_output
    song.removeTag("TIT2")
    song.removeTag("TCOM")
    assert not song.hasTag("TIT2")
    assert not song.hasTag("TCOM")


def test_Song_invalid_tag(
    monkeypatch: pytest.MonkeyPatch, table_tags: list[SongTag]
) -> None:
    """Test that invalid tags work correctly.

    They should return False for hasTag, None for getValue, and don't call removeTag.
    """
    song = Song(table_tags, table_tags, "")

    mock_songtag_remove = MagicMock()
    monkeypatch.setattr(SongTag, "removeTag", mock_songtag_remove)

    assert not song.hasTag("ABCD")
    assert song.getValue("ABCD") is None

    song.removeTag("ABCD")
    mock_songtag_remove.assert_not_called()


def test_Song_save_calls_updateInfo(
    song_path: Path, monkeypatch: pytest.MonkeyPatch, table_tags: list[SongTag]
) -> None:
    """Test that saving a song updates the file and the displayed info."""
    song = Song(table_tags, table_tags, "", song_path)
    song.setTag("TIT2", ["Some Title"])

    mock_save = MagicMock()
    monkeypatch.setattr(song.id3, "save", mock_save)
    mock_update = MagicMock()
    monkeypatch.setattr(song, "updateInfo", mock_update)

    song.save()

    mock_save.assert_called_once()
    mock_update.assert_called_once()


def test_Song_save_calls_updateInfo_file_None(
    monkeypatch: pytest.MonkeyPatch, table_tags: list[SongTag]
) -> None:
    """Test that saving a song updates the displayed info, but doesn't save a file."""
    song = Song(table_tags, table_tags, "")
    song.setTag("TIT2", ["Some Title"])

    mock_save = MagicMock()
    monkeypatch.setattr(song.id3, "save", mock_save)
    mock_update = MagicMock()
    monkeypatch.setattr(song, "updateInfo", mock_update)

    song.save()

    mock_save.assert_not_called()
    mock_update.assert_called_once()


def test_Song_load(song_path: Path, table_tags: list[SongTag]) -> None:
    """Test that creating a song and loading the file later still populates data."""
    song = Song(table_tags, table_tags, "")
    assert song.file is None

    song.updateInfo = MagicMock()
    song.load(song_path)
    assert song.file == song_path

    song.updateInfo.assert_called_once()
