"""Tests for SongModel."""

from os import PathLike
from pathlib import Path

from PySide6.QtCore import Qt

from music_modify.custom_types.song import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.custom_types.tag_value import TextTagValue
from music_modify.models import SongRepository, SongTableModel


def test_SongTableModel_init() -> None:
    """Test that a SongTableModel is initialized correctly.

    It should have no rows, but one column,
    and the header should display the empty message.
    """
    repo = SongRepository()
    model = SongTableModel(repo, [])
    assert model.rowCount() == 0
    assert model.columnCount() == 1
    assert (
        model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        == SongTableModel.empty_message
    )


def test_SongTableModel_songs_added(song_path: Path, table_tags: list[SongTag]) -> None:
    """Test that the model is updated when songs are added to the repo."""
    repo = SongRepository()
    model = SongTableModel(repo, table_tags)
    repo.add(song_path)
    assert model.rowCount() == 1
    assert model.columnCount() == len(table_tags)


def test_SongTableModel_headerData_no_songs() -> None:
    """Test that vertical headers don't exist when there is no song data."""
    repo = SongRepository()
    model = SongTableModel(repo, [])
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
    song_paths: list[PathLike[str]], table_tags: list[SongTag]
) -> None:
    """Test that headers display when songs are added."""
    repo = SongRepository()
    model = SongTableModel(repo, table_tags)
    repo.add(song_paths)
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
        == table_tags[0].display_name
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
            len(table_tags),
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


def test_SongTableModel_data_no_data_in_field(table_tags: list[SongTag]) -> None:
    """Test that data returns an empty string when the song doesn't have the tag."""
    repo = SongRepository()
    repo.add()
    model = SongTableModel(repo, table_tags)
    song = repo[0]
    assert song is not None

    assert model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole) == ""


def test_SongTableModel_data_invalid(table_tags: list[SongTag]) -> None:
    """Test that data returns None when the role or index is invalid."""
    repo = SongRepository()
    repo.add()
    model = SongTableModel(repo, table_tags)

    # Invalid index, valid role
    assert model.data(model.index(len(repo), 0), Qt.ItemDataRole.DisplayRole) is None

    # Valid index, invalid role
    assert model.data(model.index(0, 0), Qt.ItemDataRole.CheckStateRole) is None


def test_SongTableModel_data_has_value(table_tags: list[SongTag]) -> None:
    """Test that data returns a string representation when there is a value stored."""
    repo = SongRepository()
    song = Song()
    tag_value = TextTagValue(["Title"])
    song.setTag(table_tags[0].id3_key, tag_value)
    repo.add(song)
    model = SongTableModel(repo, table_tags)
    assert (
        model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole)
        == tag_value.getDisplayValue()
    )
