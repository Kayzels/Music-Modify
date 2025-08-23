# pyright: reportPrivateUsage = false, reportArgumentType = false, reportAttributeAccessIssue = false

from unittest.mock import Mock

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.song import Song
from music_modify.gui.edit.bulk.dialog_edit_bulk import (
    EditBulkDialog,
    _addMultiValues,
    _addSingleValues,
)
from music_modify.models.song_repository import SongRepository


def test_addMultiValues() -> None:
    assert _addMultiValues(None, {1}) == {1}
    assert _addMultiValues([22], {3}) == {3, 22}
    assert _addMultiValues(["a"], set()) == {"a"}


def test_addSingleValues() -> None:
    assert _addSingleValues(None, {"a"}) == ({"a"}, False)
    assert _addSingleValues("a", {"a"}) == ({"a"}, True)
    assert _addSingleValues("b", {"a"}) == ({"a", "b"}, False)


def test_EditBulkDialog_updateSongInfo_no_changes(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)

    song_1 = Song()
    monkeypatch.setattr(song_1, "save", Mock())
    song_2 = Song()
    monkeypatch.setattr(song_2, "save", Mock())

    repo = SongRepository()
    repo.addSong()
    repo.addSong()
    rows = [0, 1]

    mock_widget_1 = Mock()
    mock_widget_1.updateTag.return_value = False
    mock_widget_2 = Mock()
    mock_widget_2.updateTag.return_value = False

    dialog = EditBulkDialog(parent, repo, rows)
    # NOTE: DO NOT ADD to qtbot, leads to crash

    monkeypatch.setattr(
        dialog, "findChildren", lambda *args, **kwargs: [mock_widget_1, mock_widget_2]
    )

    with qtbot.assertNotEmitted(dialog.info_updated):
        dialog.updateSongInfo()

    mock_widget_1.updateTag.assert_called_once_with(dialog.songs)
    mock_widget_2.updateTag.assert_called_once_with(dialog.songs)

    song_1.save.assert_not_called()
    song_2.save.assert_not_called()


def test_EditBulkDialog_updateSongInfo_with_changes(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)

    song_1 = Song()
    monkeypatch.setattr(song_1, "save", Mock())
    song_2 = Song()
    monkeypatch.setattr(song_2, "save", Mock())

    repo = SongRepository()
    repo.addSong(song_1)
    repo.addSong(song_2)
    rows = [0, 1]

    mock_widget_1 = Mock()
    mock_widget_1.updateTag.return_value = True
    mock_widget_2 = Mock()
    mock_widget_2.updateTag.return_value = True

    dialog = EditBulkDialog(parent, repo, rows)
    # NOTE: DO NOT ADD to qtbot, leads to crash

    assert song_1 in dialog.songs
    assert song_2 in dialog.songs

    monkeypatch.setattr(
        dialog, "findChildren", lambda *args, **kwargs: [mock_widget_1, mock_widget_2]
    )

    with qtbot.waitSignal(dialog.info_updated, timeout=1000):
        dialog.updateSongInfo()

    mock_widget_1.updateTag.assert_called_once_with(dialog.songs)
    mock_widget_2.updateTag.assert_called_once_with(dialog.songs)

    song_1.save.assert_called_once()
    song_2.save.assert_called_once()


def test_EditBulkDialog_updateSongInfo_no_widgets(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)

    song_1 = Song()
    monkeypatch.setattr(song_1, "save", Mock())
    song_2 = Song()
    monkeypatch.setattr(song_2, "save", Mock())

    repo = SongRepository()
    repo.addSong(song_1)
    repo.addSong(song_2)
    rows = [0, 1]

    dialog = EditBulkDialog(parent, repo, rows)
    # NOTE: DO NOT ADD to qtbot, leads to crash

    assert song_1 in dialog.songs
    assert song_2 in dialog.songs

    monkeypatch.setattr(dialog, "findChildren", lambda *args, **kwargs: [])

    with qtbot.assertNotEmitted(dialog.info_updated):
        dialog.updateSongInfo()

    song_1.save.assert_not_called()
    song_2.save.assert_not_called()
