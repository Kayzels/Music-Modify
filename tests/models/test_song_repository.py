from os import PathLike
from pathlib import Path

from music_modify.models.song_repository import SongRepository


def test_init() -> None:
    repo = SongRepository()
    assert len(repo) == 0
    assert repo.getSongs() == []
    assert repo.getSong(0) is None


def test_add_single(song_path: Path) -> None:
    repo = SongRepository()
    repo.addFile(song_path)
    assert len(repo) == 1
    assert (song := repo.getSong(0)) is not None and song.file == song_path


def test_add_multiple(song_paths: list[PathLike[str]]) -> None:
    repo = SongRepository()
    repo.addFiles(song_paths)
    assert len(repo) == len(song_paths)
    for i in range(len(repo)):
        assert (song := repo.getSong(i)) is not None and song.file == song_paths[i]


def test_reject_duplicates(song_paths: list[PathLike[str]]) -> None:
    repo = SongRepository()
    repo.addFiles(song_paths)
    repo.addFile(song_paths[0])
    assert len(repo) == len(song_paths)


def test_clear(song_path: Path) -> None:
    repo = SongRepository()
    repo.addFile(song_path)
    assert len(repo) > 0
    repo.clearFiles()
    assert len(repo) == 0


def test_remove_single(song_paths: list[PathLike[str]]) -> None:
    repo = SongRepository()
    repo.addFiles(song_paths)
    repo.removeSongs([0])
    assert (song := repo.getSong(0)) is not None and song.file == song_paths[1]


def test_remove_multiple(song_paths: list[PathLike[str]]) -> None:
    repo = SongRepository()
    repo.addFiles(song_paths)
    repo.removeSongs([0, 1])
    assert (song := repo.getSong(0)) is not None and song.file == song_paths[2]
