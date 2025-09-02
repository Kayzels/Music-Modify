"""Tests for SongRepository."""

# pyright: reportUnusedParameter = false, reportMissingSuperCall = false

from os import PathLike
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.song import Song
from music_modify.models.song_repository import SongRepository


class _MockSong(Song):
    """Mock the Song class to not call __init__."""

    def __init__(self, file: str | PathLike[str] | None = None) -> None:
        """Deliberately _not_ calling super, so we don't need to stress about prefs."""
        self.file = file


@pytest.fixture
def mock_song(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fixture for mocking the Song class."""
    monkeypatch.setattr("music_modify.models.song_repository.Song", _MockSong)


def test_SongRepository_getSong_invalid_index() -> None:
    """Test that None is returned when trying to get a song at an invalid index."""
    repo = SongRepository()
    assert repo.getSong(0) is None
    assert repo[1] is None


def test_SongRepository_getSong_valid_index(mock_song: None) -> None:
    """Test that a Song is returned when using a valid index."""
    repo = SongRepository()
    repo.addSong()
    assert isinstance(repo.getSong(0), Song)
    assert isinstance(repo[0], Song)


def test_SongRepository_contains(song_path: Path, mock_song: None) -> None:
    """Test that contains returns True if the song is present, otherwise False."""
    repo = SongRepository()
    song1 = _MockSong()
    assert (song1 in repo) is False
    repo.addSong(song1)
    assert (song1 in repo) is True
    assert (song_path in repo) is False
    repo.addFile(song_path)
    assert (song_path in repo) is True


def test_SongRepository_addFile_single(
    song_path: Path, qtbot: QtBot, mock_song: None
) -> None:
    """Test that adding a file that doesn't exist works."""
    repo = SongRepository()
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.addFile(song_path)
    assert len(repo) == 1
    assert isinstance((song := repo[0]), Song)
    assert song.file == song_path


def test_SongRepository_addFile_exists_rejected(
    song_path: Path, qtbot: QtBot, mock_song: None
) -> None:
    """Tests that adding a file that exists doesn't add it again."""
    repo = SongRepository()
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.addFile(song_path)
    with qtbot.assertNotEmitted(repo.songs_updated):
        repo.addFile(song_path)
    assert len(repo) == 1
    assert (song := repo.getSong(0)) is not None
    assert song.file == song_path


def test_SongRepository_addSong_with_song(qtbot: QtBot, mock_song: None) -> None:
    """Tests that calling addSong with a song adds it the repo."""
    repo = SongRepository()
    song = _MockSong()
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.addSong(song)
    assert len(repo) == 1
    assert repo[0] == song


def test_SongRepository_addSong_with_None(qtbot: QtBot, mock_song: None) -> None:
    """Tests that calling addSong with None creates a song and adds it."""
    repo = SongRepository()
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.addSong()
    assert len(repo) == 1
    assert isinstance(repo[0], Song)


def test_SongRepository_addFiles_adds_multiple(
    song_paths: list[PathLike[str]], mock_song: None
) -> None:
    """Test that multiple songs are added when calling addFiles."""
    repo = SongRepository()
    repo.songs_updated = MagicMock()
    repo.songs_updated.emit = MagicMock()
    repo.addFiles(song_paths)
    assert len(repo) == len(song_paths)
    for i in range(len(repo)):
        assert (song := repo.getSong(i)) is not None
        assert song.file == song_paths[i]
    assert repo.songs_updated.emit.call_count == len(repo)


def test_SongRepository_clearFiles(
    song_path: Path, qtbot: QtBot, mock_song: None
) -> None:
    """Test that clearing files makes the repo empty."""
    repo = SongRepository()
    repo.addFile(song_path)
    assert len(repo) > 0
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.clearFiles()
    assert len(repo) == 0


def test_SongRepository_removeSongs_single(
    song_paths: list[PathLike[str]], qtbot: QtBot, mock_song: None
) -> None:
    """Test that removing a single song from the repo works."""
    repo = SongRepository()
    repo.addFiles(song_paths)
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.removeSongs([0])
    assert (song := repo.getSong(0)) is not None
    assert song.file == song_paths[1]


def test_SongRepository_removeSongs_multiple(
    song_paths: list[PathLike[str]], qtbot: QtBot, mock_song: None
) -> None:
    """Test that removing multiple songs from the repo works."""
    repo = SongRepository()
    repo.addFiles(song_paths)
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.removeSongs([0, 1])
    assert (song := repo.getSong(0)) is not None
    assert song.file == song_paths[2]


def test_SongRepository_removeSongs_empty_indexes(
    song_paths: list[PathLike[str]], qtbot: QtBot, mock_song: None
) -> None:
    """Test that the repo doesn't change, and songs_updated isn't emitted."""
    repo = SongRepository()
    repo.addFiles(song_paths)
    with qtbot.assertNotEmitted(repo.songs_updated):
        repo.removeSongs([])
    assert len(repo) == len(song_paths)


def test_SongRepository_refreshDisplay(
    monkeypatch: pytest.MonkeyPatch, mock_song: None
) -> None:
    """Test that refreshDisplay calls updateInfo for each song in songs."""
    mock_update_info = MagicMock()
    monkeypatch.setattr(Song, "updateInfo", mock_update_info)

    num_songs = 3

    repo = SongRepository()
    for _ in range(num_songs):
        repo.addSong()

    # Reset to not worry about the init calls
    mock_update_info.reset_mock()

    repo.refreshDisplay()

    assert mock_update_info.call_count == num_songs
