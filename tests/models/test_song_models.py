"""Tests for SongModel."""

# pyright: reportUnusedParameter = false

from os import PathLike
from pathlib import Path
from unittest.mock import MagicMock

from PySide6.QtCore import Qt

from music_modify.models import SongRepository, SongTableModel


def test_SongTableModel_init() -> None:
    """Test that a SongTableModel is initialized correctly.

    It should have no rows, but one column,
    and the header should display the empty message.
    """
    repo = SongRepository()
    model = SongTableModel(repo)
    assert model.rowCount() == 0
    assert model.columnCount() == 1
    assert (
        model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        == SongTableModel.empty_message
    )


def test_SongTableModel_songs_added(song_path: Path, mock_settings: MagicMock) -> None:
    """Test that the model is updated when songs are added to the repo."""
    repo = SongRepository()
    model = SongTableModel(repo)
    repo.addFile(song_path)
    assert model.rowCount() == 1
    assert model.columnCount() == len(mock_settings.table_tags)


def test_SongTableModel_headerData_no_songs() -> None:
    """Test that vertical headers don't exist when there is no song data."""
    repo = SongRepository()
    model = SongTableModel(repo)
    assert (
        model.headerData(
            len(repo),
            Qt.Orientation.Vertical,
            Qt.ItemDataRole.DisplayRole,
        )
        is None
    )
    assert (
        model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        == SongTableModel.empty_message
    )


def test_SongTableModel_headerData_songs_added(
    song_paths: list[PathLike[str]], mock_settings: MagicMock
) -> None:
    """Test that headers display when songs are added."""
    repo = SongRepository()
    model = SongTableModel(repo)
    repo.addFiles(song_paths)
    assert len(repo) > 0
    assert (
        model.headerData(
            0,
            Qt.Orientation.Vertical,
            Qt.ItemDataRole.DisplayRole,
        )
        == "1"
    )
    assert (
        model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        == mock_settings.table_tags[0].display_name
    )
    assert (
        model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.EditRole) is None
    )
    assert (
        model.headerData(0, Qt.Orientation.Vertical, Qt.ItemDataRole.EditRole) is None
    )

    # Invalid section indexes should be None
    assert (
        model.headerData(
            len(mock_settings.table_tags),
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


def test_SongTableModel_data_no_songs() -> None:
    """Test that data is None when there are no songs."""
    repo = SongRepository()
    model = SongTableModel(repo)

    assert model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole) is None


def test_SongTableModel_data(
    song_paths: list[PathLike[str]], mock_settings: MagicMock
) -> None:
    """Test that data returns the correct type when songs exist.

    Assuming that a valid role and index is used.
    """
    repo = SongRepository()
    model = SongTableModel(repo)
    repo.addFiles(song_paths)
    assert model.rowCount() == len(song_paths)

    assert (song := repo.getSong(0)) is not None
    assert (
        model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole)
        == song.display_info[0]
    )
    # Invalid index is None
    assert (
        model.data(model.index(len(song_paths), 0), Qt.ItemDataRole.DisplayRole) is None
    )
    # Invalid role is None
    assert model.data(model.index(0, 0), Qt.ItemDataRole.EditRole) is None
