from os import PathLike
from pathlib import Path

from music_modify.custom_types.song import Song
from music_modify.models.song_repository import SongRepository
from music_modify.prefs import prefs


def test_init() -> None:
    repo = SongRepository()
    assert len(repo) == 0
    assert repo.getSongs() == []
    assert repo.getSong(0) is None


def test_add_single_file(song_path: Path) -> None:
    repo = SongRepository()
    repo.addFile(song_path)
    assert len(repo) == 1
    assert (song := repo.getSong(0)) is not None
    assert song.file == song_path


def test_add_song_with_song() -> None:
    repo = SongRepository()
    song = Song()
    repo.addSong(song)
    assert len(repo) == 1
    assert repo[0] is not None


def test_add_song_with_None() -> None:
    repo = SongRepository()
    repo.addSong()
    assert len(repo) == 1
    assert repo[0] is not None


def test_add_multiple_files(song_paths: list[PathLike[str]]) -> None:
    repo = SongRepository()
    repo.addFiles(song_paths)
    assert len(repo) == len(song_paths)
    for i in range(len(repo)):
        assert (song := repo.getSong(i)) is not None
        assert song.file == song_paths[i]


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
    assert (song := repo.getSong(0)) is not None
    assert song.file == song_paths[1]


def test_remove_multiple(song_paths: list[PathLike[str]]) -> None:
    repo = SongRepository()
    repo.addFiles(song_paths)
    repo.removeSongs([0, 1])
    assert (song := repo.getSong(0)) is not None
    assert song.file == song_paths[2]


def test_remove_empty(song_paths: list[PathLike[str]]) -> None:
    repo = SongRepository()
    repo.addFiles(song_paths)
    repo.removeSongs([])
    assert len(repo) == len(song_paths)


def test_refreshDisplay() -> None:
    repo = SongRepository()
    repo.addSong()
    song = repo[0]
    assert song is not None
    original_display = ["" for _ in prefs.settings.table_tags]
    assert song.display_info == original_display
    song.setTag("TIT2", ["Test"])
    assert song.display_info == original_display
    repo.refreshDisplay()
    new_info: list[str] = []
    for tag in prefs.settings.table_tags:
        if tag.id3_key == "TIT2":
            new_info.append("Test")
        else:
            new_info.append("")
    assert song.display_info == new_info
