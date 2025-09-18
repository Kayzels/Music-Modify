"""Tests for SongModel."""

from os import PathLike
from pathlib import Path
import logging

from PySide6.QtCore import Qt
from PySide6.QtTest import QSignalSpy
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types import Song, TagInfo
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


def test_SongTableModel_songs_added(song_path: Path, info_tags: list[TagInfo]) -> None:
    """Test that the model is updated when songs are added to the repo."""
    repo = SongRepository()
    model = SongTableModel(repo, info_tags)
    repo.add(song_path)
    assert model.rowCount() == 1
    assert model.columnCount() == len(info_tags)


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
    song_paths: list[PathLike[str]], info_tags: list[TagInfo]
) -> None:
    """Test that headers display when songs are added."""
    repo = SongRepository()
    model = SongTableModel(repo, info_tags)
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
        == info_tags[0].display_name
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
            len(info_tags),
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


def test_SongTableModel_data_no_data_in_field(info_tags: list[TagInfo]) -> None:
    """Test that data returns an empty string when the song doesn't have the tag."""
    repo = SongRepository()
    repo.add()
    model = SongTableModel(repo, info_tags)
    song = repo[0]
    assert song is not None

    assert model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole) == ""


def test_SongTableModel_data_invalid(info_tags: list[TagInfo]) -> None:
    """Test that data returns None when the role or index is invalid."""
    repo = SongRepository()
    repo.add()
    model = SongTableModel(repo, info_tags)

    # Invalid index, valid role
    assert model.data(model.index(len(repo), 0), Qt.ItemDataRole.DisplayRole) is None

    # Valid index, invalid role
    assert model.data(model.index(0, 0), Qt.ItemDataRole.CheckStateRole) is None


def test_SongTableModel_data_has_value(info_tags: list[TagInfo]) -> None:
    """Test that data returns a string representation when there is a value stored."""
    repo = SongRepository()
    song = Song()
    tag_value = TextTagValue(["Title"])
    song.setTag(info_tags[0].id3_key, tag_value)
    repo.add(song)
    model = SongTableModel(repo, info_tags)
    assert (
        model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole)
        == tag_value.getDisplayValue()
    )


def test_SongTableModel_refreshData_empty(
    info_tags: list[TagInfo], qtbot: QtBot
) -> None:
    """Test that refreshData does not emit dataChanged when there is no data."""
    repo = SongRepository()
    model = SongTableModel(repo, info_tags)
    with qtbot.assertNotEmitted(model.dataChanged):
        model.refreshData()


def test_SongTableModel_refreshData_full(
    info_tags: list[TagInfo], qtbot: QtBot
) -> None:
    """Test that refreshData emits dataChanged for the full table when passed None."""
    repo = SongRepository()
    num_songs = 4
    for _ in range(num_songs):
        repo.add()
    model = SongTableModel(repo, info_tags)
    first_index = model.index(0, 0)
    last_index = model.index(num_songs - 1, model.columnCount() - 1)
    with qtbot.waitSignal(model.dataChanged, timeout=1000) as blocker:
        model.refreshData()

    assert blocker.args[0].row() == first_index.row()
    assert blocker.args[0].row() == first_index.row()
    assert blocker.args[1].column() == last_index.column()
    assert blocker.args[1].column() == last_index.column()
    assert blocker.args[2] == []


def test_SongTableModel_refreshData_empty_list(
    info_tags: list[TagInfo], qtbot: QtBot
) -> None:
    """Test that refreshData does not emit dataChanged when passed an empty list."""
    repo = SongRepository()
    num_songs = 2
    for _ in range(num_songs):
        repo.add()
    model = SongTableModel(repo, info_tags)
    with qtbot.assertNotEmitted(model.dataChanged):
        model.refreshData([])


def test_SongTableModel_refreshData_with_rows(info_tags: list[TagInfo]) -> None:
    """Tests that dataChanged is emitted correctly when passed valid rows."""
    repo = SongRepository()
    num_songs = 4
    for _ in range(num_songs):
        repo.add()
    model = SongTableModel(repo, info_tags)
    spy = QSignalSpy(model.dataChanged)
    rows = [1, 3]
    model.refreshData(rows)
    assert spy.count() == len(rows)
    for i, row in enumerate(rows):
        first_index = model.index(row, 0)
        last_index = model.index(row, model.columnCount() - 1)
        signal = spy.at(i)
        assert signal[0].row() == first_index.row()
        assert signal[0].column() == first_index.column()
        assert signal[1].row() == last_index.row()
        assert signal[1].column() == last_index.column()
        assert signal[2] == []


def test_SongTableModel_refreshData_invalid_rows(
    info_tags: list[TagInfo], caplog: pytest.LogCaptureFixture, qtbot: QtBot
) -> None:
    """Tests that an error is logged when trying to access a row not in the table."""
    repo = SongRepository()
    num_songs = 2
    for _ in range(num_songs):
        repo.add()
    model = SongTableModel(repo, info_tags)
    rows = [num_songs]
    with (
        caplog.at_level(logging.ERROR),
        qtbot.assertNotEmitted(model.dataChanged),
    ):
        model.refreshData(rows)

    assert "Invalid QModelIndex for row 2" in caplog.text
    assert caplog.records[0].levelname == "ERROR"
