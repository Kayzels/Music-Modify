"""Tests for EditBulkDialog."""

import logging
from typing import cast
from unittest.mock import Mock

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.core.enums import EditorType
from music_modify.custom_types import Song, TagInfo
from music_modify.gui.edit.bulk.dialog_edit_bulk import EditBulkDialog
from music_modify.models.song_repository import SongRepository


def test_EditBulkDialog_updateSongInfo_no_changes(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, info_tags: list[TagInfo]
) -> None:
    """Tests that save is not called if no changes were made to the song."""
    parent = QWidget()
    qtbot.addWidget(parent)

    song_1 = Song()
    monkeypatch.setattr(song_1, "save", Mock())
    song_2 = Song()
    monkeypatch.setattr(song_2, "save", Mock())

    repo = SongRepository()
    repo.add(song_1)
    repo.add(song_2)
    rows = [0, 1]

    mock_widget_1 = Mock()
    mock_widget_1.updateTag.return_value = set()
    mock_widget_2 = Mock()
    mock_widget_2.updateTag.return_value = set()

    dialog = EditBulkDialog(repo, rows, info_tags, parent)
    # NOTE: DO NOT ADD to qtbot, leads to crash

    monkeypatch.setattr(
        dialog, "findChildren", lambda *args, **kwargs: [mock_widget_1, mock_widget_2]
    )

    with qtbot.assertNotEmitted(dialog.info_updated):
        dialog.updateSongInfo()

    mock_widget_1.updateTag.assert_called_once_with(dialog.songs)
    mock_widget_2.updateTag.assert_called_once_with(dialog.songs)

    cast(Mock, song_1.save).assert_not_called()
    cast(Mock, song_2.save).assert_not_called()


def test_EditBulkDialog_updateSongInfo_with_changes(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, info_tags: list[TagInfo]
) -> None:
    """Test that save is called with the updated changes."""
    parent = QWidget()
    qtbot.addWidget(parent)

    song_1 = Song()
    monkeypatch.setattr(song_1, "save", Mock())
    song_2 = Song()
    monkeypatch.setattr(song_2, "save", Mock())

    repo = SongRepository()
    repo.add(song_1)
    repo.add(song_2)
    rows = [0, 1]

    mock_widget_1 = Mock()
    mock_widget_1.updateTag.return_value = {song_1}
    mock_widget_2 = Mock()
    mock_widget_2.updateTag.return_value = {song_2}

    dialog = EditBulkDialog(repo, rows, all_tags=info_tags, parent=parent)
    # NOTE: DO NOT ADD to qtbot, leads to crash

    assert song_1 in dialog.songs
    assert song_2 in dialog.songs

    monkeypatch.setattr(
        dialog, "findChildren", lambda *args, **kwargs: [mock_widget_1, mock_widget_2]
    )

    with qtbot.waitSignal(dialog.info_updated, timeout=1000) as blocker:
        dialog.updateSongInfo()
    assert 0 in blocker.args[0]
    assert 1 in blocker.args[0]

    mock_widget_1.updateTag.assert_called_once_with(dialog.songs)
    mock_widget_2.updateTag.assert_called_once_with(dialog.songs)

    cast(Mock, song_1.save).assert_called_once()
    cast(Mock, song_2.save).assert_called_once()


def test_EditBulkDialog_updateSongInfo_with_changes_single(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, info_tags: list[TagInfo]
) -> None:
    """Test that save is only called for songs that actually change data."""
    parent = QWidget()
    qtbot.addWidget(parent)

    song_1 = Song()
    monkeypatch.setattr(song_1, "save", Mock())
    song_2 = Song()
    monkeypatch.setattr(song_2, "save", Mock())

    repo = SongRepository()
    repo.add(song_1)
    repo.add(song_2)
    rows = [0, 1]

    mock_widget_1 = Mock()
    mock_widget_1.updateTag.return_value = set()
    mock_widget_2 = Mock()
    mock_widget_2.updateTag.return_value = {song_2}

    dialog = EditBulkDialog(repo, rows, info_tags, parent)
    # NOTE: DO NOT ADD to qtbot, leads to crash

    assert song_1 in dialog.songs
    assert song_2 in dialog.songs

    monkeypatch.setattr(
        dialog, "findChildren", lambda *args, **kwargs: [mock_widget_1, mock_widget_2]
    )

    with qtbot.waitSignal(dialog.info_updated, timeout=1000) as blocker:
        dialog.updateSongInfo()
    assert blocker.args[0] == [1]

    mock_widget_1.updateTag.assert_called_once_with(dialog.songs)
    mock_widget_2.updateTag.assert_called_once_with(dialog.songs)

    cast(Mock, song_1.save).assert_not_called()
    cast(Mock, song_2.save).assert_called_once()


def test_EditBulkDialog_updateSongInfo_no_widgets(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, info_tags: list[TagInfo]
) -> None:
    """Tests that save is not called, without mocking widgets."""
    parent = QWidget()
    qtbot.addWidget(parent)

    song_1 = Song()
    monkeypatch.setattr(song_1, "save", Mock())
    song_2 = Song()
    monkeypatch.setattr(song_2, "save", Mock())

    repo = SongRepository()
    repo.add(song_1)
    repo.add(song_2)
    rows = [0, 1]

    dialog = EditBulkDialog(repo, rows, info_tags, parent)
    # NOTE: DO NOT ADD to qtbot, leads to crash

    assert song_1 in dialog.songs
    assert song_2 in dialog.songs

    monkeypatch.setattr(dialog, "findChildren", lambda *args, **kwargs: [])

    with qtbot.assertNotEmitted(dialog.info_updated):
        dialog.updateSongInfo()

    cast(Mock, song_1.save).assert_not_called()
    cast(Mock, song_2.save).assert_not_called()


def test_EditBulkDialog_setupSongInfo_unsupported_editor_type_logged(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    """Test that _setupSongInfo logs unsupported EditorType."""
    widget = QWidget()
    qtbot.addWidget(widget)

    tag = TagInfo(
        id3_key="ABCD", display_name="Automatic Tag", editor_type=EditorType.Automatic
    )

    repo = SongRepository()
    repo.add()
    rows = [0]

    with caplog.at_level(logging.WARNING):
        EditBulkDialog(repo, rows, all_tags=[tag], parent=widget)

    assert (
        "Unsupported editor type or tag value. " + "Editor type: EditorType.Automatic. "
        in caplog.text
    )
    assert caplog.records[0].levelname == "WARNING"
