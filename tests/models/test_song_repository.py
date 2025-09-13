"""Tests for SongRepository."""

from os import PathLike
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.song import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.models.song_repository import SongRepository


def test_SongRepository_getSong_invalid_index(table_tags: list[SongTag]) -> None:
    """Test that None is returned when trying to get a song at an invalid index."""
    repo = SongRepository(table_tags, table_tags, ", ")
    assert repo.getSong(0) is None
    assert repo[1] is None


def test_SongRepository_getSong_valid_index(table_tags: list[SongTag]) -> None:
    """Test that a Song is returned when using a valid index."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.addSong()
    assert isinstance(repo.getSong(0), Song)
    assert isinstance(repo[0], Song)


def test_SongRepository_contains(song_path: Path, table_tags: list[SongTag]) -> None:
    """Test that contains returns True if the song is present, otherwise False."""
    repo = SongRepository(table_tags, table_tags, ", ")
    song1 = Song(table_tags, table_tags, ", ")
    assert (song1 in repo) is False
    repo.addSong(song1)
    assert (song1 in repo) is True
    assert (song_path in repo) is False
    repo.addFile(song_path)
    assert (song_path in repo) is True


def test_SongRepository_addFile_single(
    song_path: Path, qtbot: QtBot, table_tags: list[SongTag]
) -> None:
    """Test that adding a file that doesn't exist works."""
    repo = SongRepository(table_tags, table_tags, ", ")
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.addFile(song_path)
    assert len(repo) == 1
    assert isinstance((song := repo[0]), Song)
    assert song.file == song_path


def test_SongRepository_addFile_exists_rejected(
    song_path: Path, qtbot: QtBot, table_tags: list[SongTag]
) -> None:
    """Tests that adding a file that exists doesn't add it again."""
    repo = SongRepository(table_tags, table_tags, ", ")
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.addFile(song_path)
    with qtbot.assertNotEmitted(repo.songs_updated):
        repo.addFile(song_path)
    assert len(repo) == 1
    assert (song := repo.getSong(0)) is not None
    assert song.file == song_path


def test_SongRepository_addSong_with_song(
    qtbot: QtBot, table_tags: list[SongTag]
) -> None:
    """Tests that calling addSong with a song adds it the repo."""
    repo = SongRepository(table_tags, table_tags, ", ")
    song = Song(table_tags, table_tags, ", ")
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.addSong(song)
    assert len(repo) == 1
    assert repo[0] == song


def test_SongRepository_addSong_with_None(
    qtbot: QtBot, table_tags: list[SongTag]
) -> None:
    """Tests that calling addSong with None creates a song and adds it."""
    repo = SongRepository(table_tags, table_tags, ", ")
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.addSong()
    assert len(repo) == 1
    assert isinstance(repo[0], Song)


def test_SongRepository_addFiles_adds_multiple(
    song_paths: list[PathLike[str]], table_tags: list[SongTag]
) -> None:
    """Test that multiple songs are added when calling addFiles."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.songs_updated = MagicMock()
    repo.songs_updated.emit = MagicMock()
    repo.addFiles(song_paths)
    assert len(repo) == len(song_paths)
    for i in range(len(repo)):
        assert (song := repo.getSong(i)) is not None
        assert song.file == song_paths[i]
    assert repo.songs_updated.emit.call_count == len(repo)


def test_SongRepository_clearFiles(
    song_path: Path, qtbot: QtBot, table_tags: list[SongTag]
) -> None:
    """Test that clearing files makes the repo empty."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.addFile(song_path)
    assert len(repo) > 0
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.clearFiles()
    assert len(repo) == 0


def test_SongRepository_removeSongs_single(
    song_paths: list[PathLike[str]],
    qtbot: QtBot,
    table_tags: list[SongTag],
) -> None:
    """Test that removing a single song from the repo works."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.addFiles(song_paths)
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.removeSongs([0])
    assert (song := repo.getSong(0)) is not None
    assert song.file == song_paths[1]


def test_SongRepository_removeSongs_multiple(
    song_paths: list[PathLike[str]],
    qtbot: QtBot,
    table_tags: list[SongTag],
) -> None:
    """Test that removing multiple songs from the repo works."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.addFiles(song_paths)
    with qtbot.waitSignal(repo.songs_updated, timeout=1000):
        repo.removeSongs([0, 1])
    assert (song := repo.getSong(0)) is not None
    assert song.file == song_paths[2]


def test_SongRepository_removeSongs_empty_indexes(
    song_paths: list[PathLike[str]],
    qtbot: QtBot,
    table_tags: list[SongTag],
) -> None:
    """Test that the repo doesn't change, and songs_updated isn't emitted."""
    repo = SongRepository(table_tags, table_tags, ", ")
    repo.addFiles(song_paths)
    with qtbot.assertNotEmitted(repo.songs_updated):
        repo.removeSongs([])
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
        repo.addSong()

    # Reset to not worry about the init calls
    mock_update_info.reset_mock()

    repo.refreshDisplay()

    assert mock_update_info.call_count == num_songs
