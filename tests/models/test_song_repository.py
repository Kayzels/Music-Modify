"""Tests for SongRepository."""

from os import PathLike
from pathlib import Path
from unittest.mock import MagicMock

from PySide6.QtTest import QSignalSpy
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.song import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.models.song_repository import SongRepository


def test_SongRepository_getitem_invalid_index_raises(table_tags: list[SongTag]) -> None:
    """Test that IndexError returned when trying to get a song at an invalid index."""
    repo = SongRepository(table_tags, table_tags, ", ")
    with pytest.raises(IndexError):
        _ = repo[0]


def test_SongRepository_getitem_valid_index(table_tags: list[SongTag]) -> None:
    """Test that a Song is returned when using a valid index."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.add()
    assert isinstance(repo[0], Song)


def test_SongRepository_contains(song_path: Path, table_tags: list[SongTag]) -> None:
    """Test that contains returns True if the song is present, otherwise False."""
    repo = SongRepository(table_tags, table_tags, ", ")
    song1 = Song(table_tags, table_tags, ", ")
    assert (song1 in repo) is False
    repo.add(song1)
    assert (song1 in repo) is True
    assert (song_path in repo) is False
    repo.add(song_path)
    assert (song_path in repo) is True


def test_SongRepository_add_file_single(
    song_path: Path, qtbot: QtBot, table_tags: list[SongTag]
) -> None:
    """Test that adding a file that doesn't exist works."""
    repo = SongRepository(table_tags, table_tags, ", ")
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.add(song_path)
    assert len(repo) == 1
    assert repo[0].file == song_path


def test_SongRepository_add_file_as_string_single(
    song_path: Path, qtbot: QtBot, table_tags: list[SongTag]
) -> None:
    """Test that adding a file as a string adds it."""
    repo = SongRepository(table_tags, table_tags, ", ")
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.add(str(song_path))
    assert len(repo) == 1
    assert repo[0].file == str(song_path)


def test_SongRepository_add_file_exists_rejected(
    song_path: Path, table_tags: list[SongTag]
) -> None:
    """Tests that adding a file that exists doesn't add it again."""
    repo = SongRepository(table_tags, table_tags, ", ")
    spy = QSignalSpy(repo.songs_updated)
    repo.add(song_path)
    repo.add(song_path)
    assert len(repo) == 1
    assert spy.count() == 1
    assert repo[0].file == song_path


def test_SongRepository_add_with_song(qtbot: QtBot, table_tags: list[SongTag]) -> None:
    """Tests that calling addSong with a song adds it the repo."""
    repo = SongRepository(table_tags, table_tags, ", ")
    song = Song(table_tags, table_tags, ", ")
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.add(song)
    assert len(repo) == 1
    assert repo[0] == song


def test_SongRepository_add_with_song_multiple(table_tags: list[SongTag]) -> None:
    """Tests that calling addSong with multiple songs adds them to the repo."""
    repo = SongRepository(table_tags, table_tags, ", ")
    song1 = Song(table_tags, table_tags, ", ")
    song2 = Song(table_tags, table_tags, ", ")
    assert song1 != song2
    repo.add(song1)
    repo.add(song2)
    assert len(repo) == 2
    assert repo[0] == song1
    assert repo[1] == song2


def test_SongRepository_add_with_None(qtbot: QtBot, table_tags: list[SongTag]) -> None:
    """Tests that calling addSong with None creates a song and adds it."""
    repo = SongRepository(table_tags, table_tags, ", ")
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.add()
    assert len(repo) == 1
    assert isinstance(repo[0], Song)


def test_SongRepository_add_with_multiple_files(
    song_paths: list[PathLike[str]], table_tags: list[SongTag]
) -> None:
    """Test that multiple songs are added when calling addFiles."""
    repo = SongRepository(table_tags, table_tags, ", ")
    spy = QSignalSpy(repo.songs_updated)
    repo.add(song_paths)
    assert len(repo) == len(song_paths)
    for i in range(len(repo)):
        song = repo[i]
        assert song.file == song_paths[i]
    assert spy.count() == len(repo)


def test_SongRepository_clear(
    song_path: Path, qtbot: QtBot, table_tags: list[SongTag]
) -> None:
    """Test that clearing files makes the repo empty."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.add(song_path)
    assert len(repo) > 0
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.clear()
    assert len(repo) == 0


def test_SongRepository_removeAtIndexes_single(
    song_paths: list[PathLike[str]],
    qtbot: QtBot,
    table_tags: list[SongTag],
) -> None:
    """Test that removing a single song from the repo works."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.add(song_paths)
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.removeAtIndexes([0])
    assert repo[0].file == song_paths[1]


def test_SongRepository_removeAtIndexes_multiple(
    song_paths: list[PathLike[str]],
    qtbot: QtBot,
    table_tags: list[SongTag],
) -> None:
    """Test that removing multiple songs from the repo works."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.add(song_paths)
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.removeAtIndexes([0, 1])
    assert repo[0].file == song_paths[2]


def test_SongRepository_removeAtIndexes_empty_indexes(
    song_paths: list[PathLike[str]],
    qtbot: QtBot,
    table_tags: list[SongTag],
) -> None:
    """Test that the repo doesn't change, and songs_updated isn't emitted."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.add(song_paths)
    with qtbot.assertNotEmitted(repo.songs_updated):
        repo.removeAtIndexes([])
    assert len(repo) == len(song_paths)


def test_SongRepository_refreshDisplay(
    monkeypatch: pytest.MonkeyPatch, table_tags: list[SongTag]
) -> None:
    """Test that refreshDisplay calls updateInfo for each song in songs."""
    mock_update_info = MagicMock()
    monkeypatch.setattr(Song, "updateInfo", mock_update_info)

    num_songs = 3

    repo = SongRepository(table_tags, table_tags, ", ")
    for _ in range(num_songs):
        repo.add()

    # Reset to not worry about the init calls
    mock_update_info.reset_mock()

    repo.refreshDisplay()

    assert mock_update_info.call_count == num_songs
