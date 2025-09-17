"""Tests for EditDialog."""

# pyright: reportPrivateUsage = false

import logging
from unittest.mock import MagicMock

from PySide6.QtWidgets import QDialog, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types import Song, TagInfo
from music_modify.custom_types.enums import NavDirection
from music_modify.custom_types.tag_value import TextTagValue
from music_modify.gui.edit.dialog_edit import EditDialog
from music_modify.gui.edit.widget_edit_abstract import EditAbstractWidget
from music_modify.gui.edit.widget_edit_line import EditLineWidget
from music_modify.models.song_repository import SongRepository


def _createDialog(
    qtbot: QtBot, rows: list[int], info_tags: list[TagInfo], *, num_songs: int = 0
) -> tuple[QWidget, EditDialog]:
    widget = QWidget()
    qtbot.addWidget(widget)
    repo = SongRepository()
    for _ in range(num_songs):
        repo.add()
    dialog = EditDialog(repo, rows, info_tags, widget)
    return widget, dialog


def test_EditDialog_init_no_rows(qtbot: QtBot, info_tags: list[TagInfo]) -> None:
    """Tests that passing no rows through rejects the dialog."""
    _, dialog = _createDialog(qtbot, [], info_tags, num_songs=0)
    assert dialog.result() == QDialog.DialogCode.Rejected
    assert not hasattr(dialog, "song_info")


def test_EditDialog_init_song_None(qtbot: QtBot, info_tags: list[TagInfo]) -> None:
    """Tests that the dialog is rejected if there is no song at that index."""
    _, dialog = _createDialog(qtbot, [0], info_tags, num_songs=0)
    assert dialog.result() == QDialog.DialogCode.Rejected
    assert not hasattr(dialog, "song_info")


def test_EditDialog_init_song_single(qtbot: QtBot, info_tags: list[TagInfo]) -> None:
    """Tests that the song is found at the index, and nav buttons aren't created."""
    _, dialog = _createDialog(qtbot, [0], info_tags, num_songs=1)

    assert dialog.song_info is not None
    assert isinstance(dialog.song_info, Song)

    assert not hasattr(dialog, "previous_button")
    assert not hasattr(dialog, "next_button")


def test_EditDialog_init_song_multiple(qtbot: QtBot, info_tags: list[TagInfo]) -> None:
    """Tests that the songs are found at the indexes, and nav buttons are created."""
    _, dialog = _createDialog(qtbot, [0, 1], info_tags, num_songs=2)

    assert dialog.song_info is not None
    assert isinstance(dialog.song_info, Song)

    assert hasattr(dialog, "previous_button")
    assert not dialog.previous_button.isEnabled()
    assert hasattr(dialog, "next_button")
    assert dialog.next_button.isEnabled()

    assert dialog.current_index == 0
    first_song = dialog.song_info
    dialog.next_button.click()
    assert dialog.current_index == 1
    second_song = dialog.song_info
    assert first_song != second_song

    assert not dialog.next_button.isEnabled()
    assert dialog.previous_button.isEnabled()

    dialog.previous_button.click()
    assert dialog.current_index == 0
    current_song = dialog.song_info
    assert current_song == first_song

    assert not dialog.previous_button.isEnabled()
    assert dialog.next_button.isEnabled()


def test_EditDialog_updateSongInfo_setsValue(
    qtbot: QtBot, info_tags: list[TagInfo]
) -> None:
    """Tests that calling updateSongInfo saves the values to the song."""
    mock_song = MagicMock(spec=Song)
    _, dialog = _createDialog(qtbot, [0], info_tags, num_songs=1)
    dialog.song_info = mock_song
    line_widget = EditLineWidget()
    line_widget.value = TextTagValue(["First"])
    dialog._edit_widgets["TIT2"] = line_widget

    with qtbot.waitSignal(dialog.info_updated, timeout=1000):
        dialog.updateSongInfo()

    mock_song.setTag.assert_any_call("TIT2", TextTagValue(["First"]))
    mock_song.save.assert_called_once()


def test_EditDialog_updateSongInfo_afterReset(
    qtbot: QtBot, info_tags: list[TagInfo]
) -> None:
    """Tests that calling updateSongInfo saves values to the song after resetting."""
    song = Song()
    initial_value = TextTagValue(["First"])
    new_value = TextTagValue(["New"])
    song.setTag("TIT2", initial_value)
    repo = SongRepository()
    repo.add(song)
    widget = QWidget()
    qtbot.addWidget(widget)
    dialog = EditDialog(repo, [0], info_tags, widget)
    line_widget = dialog._edit_widgets["TIT2"]
    line_widget.value = new_value
    with qtbot.waitSignal(dialog.info_updated, timeout=1000):
        dialog.updateSongInfo()
    assert song.getTag("TIT2") == new_value
    dialog.resetSongInfo()
    assert line_widget.value == initial_value
    assert song.getTag("TIT2") == new_value
    with qtbot.waitSignal(dialog.info_updated, timeout=1000):
        dialog.updateSongInfo()
    assert song.getTag("TIT2") == initial_value


def test_EditDialog_switchButtonState_no_buttons_logged(
    qtbot: QtBot, info_tags: list[TagInfo], caplog: pytest.LogCaptureFixture
) -> None:
    """Tests logging when trying to change button state for non-existing buttons."""
    _, dialog = _createDialog(qtbot, [], info_tags, num_songs=0)

    assert not hasattr(dialog, "next_button")
    assert not hasattr(dialog, "previous_button")

    with caplog.at_level(logging.WARNING):
        dialog._switchButtonState()

        assert "Missing next or previous button in edit dialog" in caplog.text
        assert caplog.records[0].levelname == "WARNING"


def test_EditDialog_showSongInDirection_last_or_first_logged(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture, info_tags: list[TagInfo]
) -> None:
    """Tests that invalid navigation on first or last is logged."""
    _, dialog = _createDialog(qtbot, [0, 1], info_tags, num_songs=2)

    assert dialog.current_index == 0

    with caplog.at_level(logging.DEBUG):
        dialog.showSongInDirection(NavDirection.Previous)

        assert (
            "Tried to go to next song on last, or previous song on first."
            in caplog.records[0].message
        )
        assert caplog.records[0].levelname == "DEBUG"

        dialog.showSongInDirection(NavDirection.Next)
        caplog.clear()
        dialog.showSongInDirection(NavDirection.Next)

        assert (
            "Tried to go to next song on last, or previous song on first."
            in caplog.records[0].message
        )
        assert caplog.records[0].levelname == "DEBUG"


def test_EditDialog_showSongInDirection_no_song(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture, info_tags: list[TagInfo]
) -> None:
    """Tests that trying to display a song at an invalid index closes the dialog."""
    _, dialog = _createDialog(qtbot, [0, 1], info_tags, num_songs=1)

    with caplog.at_level(logging.WARNING):
        dialog.showSongInDirection(NavDirection.Next)
        assert "Invalid song, closing dialog" in caplog.text

    assert dialog.result() == QDialog.DialogCode.Rejected


def test_EditDialog_resetSongInfo(
    qtbot: QtBot, info_tags: list[TagInfo], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tests that song values can be reset."""
    mock_reset_method = MagicMock()
    monkeypatch.setattr(EditAbstractWidget, "reset", mock_reset_method)
    _, dialog = _createDialog(qtbot, [0], info_tags, num_songs=1)
    dialog.resetSongInfo()
    assert mock_reset_method.call_count == len(dialog._edit_widgets)
