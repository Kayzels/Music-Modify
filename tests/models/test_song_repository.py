"""Tests for SongRepository."""

from os import PathLike
from pathlib import Path

from PySide6.QtTest import QSignalSpy
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.song import Song
from music_modify.models.song_repository import SongRepository


def test_SongRepository_getitem_invalid_index_raises() -> None:
    """Test that IndexError returned when trying to get a song at an invalid index."""
    repo = SongRepository()
    with pytest.raises(IndexError):
        _ = repo[0]


def test_SongRepository_getitem_valid_index() -> None:
    """Test that a Song is returned when using a valid index."""
    repo = SongRepository()
    repo.add()
    assert isinstance(repo[0], Song)


def test_SongRepository_contains(song_path: Path) -> None:
    """Test that contains returns True if the song is present, otherwise False."""
    repo = SongRepository()
    song1 = Song()
    assert (song1 in repo) is False
    repo.add(song1)
    assert (song1 in repo) is True
    assert (song_path in repo) is False
    repo.add(song_path)
    assert (song_path in repo) is True


def test_SongRepository_add_file_single(song_path: Path, qtbot: QtBot) -> None:
    """Test that adding a file that doesn't exist works."""
    repo = SongRepository()
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.add(song_path)
    assert len(repo) == 1
    assert repo[0].file == song_path


def test_SongRepository_add_file_as_string_single(
    song_path: Path, qtbot: QtBot
) -> None:
    """Test that adding a file as a string adds it."""
    repo = SongRepository()
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.add(str(song_path))
    assert len(repo) == 1
    assert repo[0].file == str(song_path)


def test_SongRepository_add_file_exists_rejected(song_path: Path) -> None:
    """Tests that adding a file that exists doesn't add it again."""
    repo = SongRepository()
    spy = QSignalSpy(repo.songs_updated)
    repo.add(song_path)
    repo.add(song_path)
    assert len(repo) == 1
    assert spy.count() == 1
    assert repo[0].file == song_path


def test_SongRepository_add_with_song(qtbot: QtBot) -> None:
    """Tests that calling addSong with a song adds it the repo."""
    repo = SongRepository()
    song = Song()
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.add(song)
    assert len(repo) == 1
    assert repo[0] == song


def test_SongRepository_add_with_song_multiple() -> None:
    """Tests that calling addSong with multiple songs adds them to the repo."""
    repo = SongRepository()
    song1 = Song()
    song2 = Song()
    assert song1 != song2
    repo.add(song1)
    repo.add(song2)
    assert len(repo) == 2
    assert repo[0] == song1
    assert repo[1] == song2


def test_SongRepository_add_with_None(qtbot: QtBot) -> None:
    """Tests that calling addSong with None creates a song and adds it."""
    repo = SongRepository()
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.add()
    assert len(repo) == 1
    assert isinstance(repo[0], Song)


def test_SongRepository_add_with_multiple_files(
    song_paths: list[PathLike[str]],
) -> None:
    """Test that multiple songs are added when calling addFiles."""
    repo = SongRepository()
    spy = QSignalSpy(repo.songs_updated)
    repo.add(song_paths)
    assert len(repo) == len(song_paths)
    for i in range(len(repo)):
        song = repo[i]
        assert song.file == song_paths[i]
    assert spy.count() == len(repo)


def test_SongRepository_clear(song_path: Path, qtbot: QtBot) -> None:
    """Test that clearing files makes the repo empty."""
    repo = SongRepository()
    repo.add(song_path)
    assert len(repo) > 0
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.clear()
    assert len(repo) == 0


def test_SongRepository_removeAtIndexes_single(
    song_paths: list[PathLike[str]], qtbot: QtBot
) -> None:
    """Test that removing a single song from the repo works."""
    repo = SongRepository()
    repo.add(song_paths)
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.removeAtIndexes([0])
    assert repo[0].file == song_paths[1]


def test_SongRepository_removeAtIndexes_multiple(
    song_paths: list[PathLike[str]], qtbot: QtBot
) -> None:
    """Test that removing multiple songs from the repo works."""
    repo = SongRepository()
    repo.add(song_paths)
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.removeAtIndexes([0, 1])
    assert repo[0].file == song_paths[2]


def test_SongRepository_removeAtIndexes_empty_indexes(
    song_paths: list[PathLike[str]],
    qtbot: QtBot,
) -> None:
    """Test that the repo doesn't change, and songs_updated isn't emitted."""
    repo = SongRepository()
    repo.add(song_paths)
    with qtbot.assertNotEmitted(repo.songs_updated):
        repo.removeAtIndexes([])
    assert len(repo) == len(song_paths)


def test_SongRepository_index() -> None:
    """Test that the repo returns the correct index for a song."""
    repo = SongRepository()
    song1 = Song()
    song2 = Song()
    repo.add(song1)
    repo.add(song2)
    assert repo.index(song2) == 1
