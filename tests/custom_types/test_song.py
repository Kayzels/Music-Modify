"""Tests for Song."""

# pyright: reportUnusedParameter = false

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from music_modify.custom_types import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.prefs import prefs

logger = logging.getLogger(__name__)


def test_Song_init_with_None(mock_settings: MagicMock) -> None:
    """Test that a Song object is created correctly when not passed a file."""
    song = Song()
    assert song.file is None
    info: list[str] = ["" for _ in range(len(mock_settings.table_tags))]
    assert song.display_info == info


def test_Song_init_with_file(song_path: Path, mock_settings: MagicMock) -> None:
    """Test that a Song object is created correctly when passed a file."""
    song = Song(song_path)
    assert song.file == song_path
    assert hasattr(song, "display_info")
    assert isinstance(song.display_info, list)


def test_Song_columns_setTag_removeTag(
    song_path: Path, mock_settings: MagicMock
) -> None:
    """Test that setting and then removing tags works."""
    song = Song(song_path)
    song.setTag("TIT2", ["Some Title"])
    song.setTag("TPE2", ["Some Artist"])
    assert song.hasTag("TIT2")
    assert song.hasTag("TPE2")
    song.updateInfo()
    expected_output: list[str] = []
    for col in prefs.settings.table_tags:
        if col.id3_key == "TIT2":
            logger.info("ID3 key was TIT2")
            expected_output.append("Some Title")
        elif col.id3_key == "TPE2":
            logger.info("ID3 key was TPE2")
            expected_output.append("Some Artist")
        else:
            expected_output.append("")
    assert song.display_info == expected_output
    song.removeTag("TIT2")
    song.removeTag("TPE2")
    assert not song.hasTag("TIT2")
    assert not song.hasTag("TPE2")


def test_Song_invalid_tag(
    monkeypatch: pytest.MonkeyPatch, mock_settings: MagicMock
) -> None:
    """Test that invalid tags work correctly.

    They should return False for hasTag, None for getValue, and don't call removeTag.
    """
    song = Song()

    mock_songtag_remove = MagicMock()
    monkeypatch.setattr(SongTag, "removeTag", mock_songtag_remove)

    assert not song.hasTag("ABCD")
    assert song.getValue("ABCD") is None

    song.removeTag("ABCD")
    mock_songtag_remove.assert_not_called()


def test_Song_save_calls_updateInfo(
    song_path: Path, monkeypatch: pytest.MonkeyPatch, mock_settings: MagicMock
) -> None:
    """Test that saving a song updates the file and the displayed info."""
    song = Song(song_path)
    song.setTag("TIT2", ["Some Title"])

    mock_save = MagicMock()
    monkeypatch.setattr(song.id3, "save", mock_save)
    mock_update = MagicMock()
    monkeypatch.setattr(song, "updateInfo", mock_update)

    song.save()

    mock_save.assert_called_once()
    mock_update.assert_called_once()


def test_Song_save_calls_updateInfo_file_None(
    monkeypatch: pytest.MonkeyPatch, mock_settings: MagicMock
) -> None:
    """Test that saving a song updates the displayed info, but doesn't save a file."""
    song = Song()
    song.setTag("TIT2", ["Some Title"])

    mock_save = MagicMock()
    monkeypatch.setattr(song.id3, "save", mock_save)
    mock_update = MagicMock()
    monkeypatch.setattr(song, "updateInfo", mock_update)

    song.save()

    mock_save.assert_not_called()
    mock_update.assert_called_once()


def test_Song_load(song_path: Path, mock_settings: MagicMock) -> None:
    """Test that creating a song and loading the file later still populates data."""
    song = Song()
    assert song.file is None

    song.updateInfo = MagicMock()
    song.load(song_path)
    assert song.file == song_path

    song.updateInfo.assert_called_once()
