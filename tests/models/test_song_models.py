from os import PathLike
from pathlib import Path
from PySide6.QtCore import Qt
from music_modify.models import SongRepository, SongTableModel
from music_modify.prefs import prefs


def test_init():
    repo = SongRepository()
    model = SongTableModel(repo)
    assert model.rowCount() == 0
    assert model.columnCount() == 1
    assert (
        model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        == SongTableModel.empty_message
    )


def test_add(song_path: Path):
    repo = SongRepository()
    model = SongTableModel(repo)
    repo.addFile(song_path)
    assert model.rowCount() == 1
    assert model.columnCount() == len(prefs.settings.table_tags)


def test_headers(song_paths: list[PathLike[str]]):
    repo = SongRepository()
    model = SongTableModel(repo)
    repo.addFiles(song_paths)
    assert len(repo) > 0
    assert (
        model.headerData(0, Qt.Orientation.Vertical, Qt.ItemDataRole.DisplayRole) == "1"
    )
    assert (
        model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        == prefs.settings.table_tags[0].display_name
    )
    assert (
        model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.EditRole) is None
    )
    assert (
        model.headerData(0, Qt.Orientation.Vertical, Qt.ItemDataRole.EditRole) is None
    )
    assert (
        model.headerData(
            len(prefs.settings.table_tags),
            Qt.Orientation.Horizontal,
            Qt.ItemDataRole.DisplayRole,
        )
        is None
    )
    assert (
        model.headerData(
            len(repo),
            Qt.Orientation.Vertical,
            Qt.ItemDataRole.DisplayRole,
        )
        is None
    )


def test_data(song_paths: list[PathLike[str]]):
    repo = SongRepository()
    model = SongTableModel(repo)
    repo.addFiles(song_paths)
    assert model.rowCount() == len(song_paths)

    assert (
        model.data(model.index(len(song_paths), 0), Qt.ItemDataRole.DisplayRole) is None
    )
    assert model.data(model.index(0, 0), Qt.ItemDataRole.EditRole) is None
    assert (song := repo.getSong(0)) is not None
    assert (
        model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole)
        == song.display_info[0]
    )
