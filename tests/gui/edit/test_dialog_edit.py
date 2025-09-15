"""Tests for EditDialog."""

# pyright: reportPrivateUsage = false

import logging
from typing import cast
from unittest.mock import Mock, PropertyMock

from PySide6.QtWidgets import QDialog, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.enums import NavDirection
from music_modify.custom_types.song import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.gui.edit.dialog_edit import EditDialog
from music_modify.gui.edit.widget_edit_abstract import EditAbstractWidget
from music_modify.models.song_repository import SongRepository


def _createParentAndRepo(
    qtbot: QtBot,
    num_songs: int = 0,
) -> tuple[QWidget, SongRepository]:
    widget = QWidget()
    qtbot.addWidget(widget)
    repo = SongRepository()
    for _ in range(num_songs):
        repo.add()
    return widget, repo


def _createDialog(
    qtbot: QtBot, rows: list[int], table_tags: list[SongTag], *, num_songs: int = 0
) -> tuple[QWidget, EditDialog]:
    widget, repo = _createParentAndRepo(qtbot, num_songs)
    dialog = EditDialog(widget, repo, rows, table_tags)
    return widget, dialog


def test_EditDialog_init_no_rows(qtbot: QtBot, table_tags: list[SongTag]) -> None:
    """Tests that passing no rows through rejects the dialog."""
    _, dialog = _createDialog(qtbot, [], table_tags, num_songs=0)
    assert dialog.result() == QDialog.DialogCode.Rejected


def test_EditDialog_init_song_None(qtbot: QtBot, table_tags: list[SongTag]) -> None:
    """Tests that the dialog is rejected if there is no song at that index."""
    _, dialog = _createDialog(qtbot, [0], table_tags, num_songs=0)
    assert dialog.result() == QDialog.DialogCode.Rejected


def test_EditDialog_init_song_single(qtbot: QtBot, table_tags: list[SongTag]) -> None:
    """Tests that the song is found at the index, and nav buttons aren't created."""
    _, dialog = _createDialog(qtbot, [0], table_tags, num_songs=1)

    assert dialog.song_info is not None
    assert isinstance(dialog.song_info, Song)

    assert not hasattr(dialog, "previous_button")
    assert not hasattr(dialog, "next_button")


def test_EditDialog_init_song_multiple(qtbot: QtBot, table_tags: list[SongTag]) -> None:
    """Tests that the songs are found at the indexes, and nav buttons are created."""
    _, dialog = _createDialog(qtbot, [0, 1], table_tags, num_songs=2)

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
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, table_tags: list[SongTag]
) -> None:
    """Tests that calling updateSongInfo saves the values to the song."""
    _, dialog = _createDialog(qtbot, [0], table_tags, num_songs=1)

    mock_tag = Mock(spec=SongTag)
    test_key: str = "TIT2"
    test_value: str | None = "New Title"
    mock_tag.id3_key = test_key
    mock_tag.setTag = Mock()
    mock_tag.removeTag = Mock()

    monkeypatch.setattr(
        "music_modify.gui.edit.dialog_edit.mapKey",
        lambda key, tags: mock_tag if key == test_key else None,
    )
    monkeypatch.setattr(dialog.song_info, "save", Mock())

    dialog.changed_values = {test_key: test_value}

    # Check that info_updated signal is emitted after updateSongInfo
    with qtbot.waitSignal(dialog.info_updated, timeout=1000):
        dialog.updateSongInfo()

    mock_tag.setTag.assert_called_once_with(dialog.song_info.id3, [test_value])
    mock_tag.removeTag.assert_not_called()
    cast(Mock, dialog.song_info.save).assert_called_once()
    assert not dialog.changed_values


def test_EditDialog_updateSongInfo_removesValue(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, table_tags: list[SongTag]
) -> None:
    """Tests that calling updateSongInfo removes values when needed."""
    _, dialog = _createDialog(qtbot, [0], table_tags, num_songs=1)

    mock_tag = Mock(spec=SongTag)
    test_key: str = "TPE1"
    test_value: str | None = None  # Indicates removal
    mock_tag.id3_key = test_key
    mock_tag.setTag = Mock()
    mock_tag.removeTag = Mock()

    monkeypatch.setattr(
        "music_modify.gui.edit.dialog_edit.mapKey",
        lambda key, tags: mock_tag if key == test_key else None,
    )
    monkeypatch.setattr(dialog.song_info, "save", Mock())

    dialog.changed_values = {test_key: test_value}

    # Check that info_updated signal is emitted after updateSongInfo
    with qtbot.waitSignal(dialog.info_updated, timeout=1000):
        dialog.updateSongInfo()

    mock_tag.setTag.assert_not_called()
    mock_tag.removeTag.assert_called_once_with(dialog.song_info.id3)
    cast(Mock, dialog.song_info.save).assert_called_once()
    assert not dialog.changed_values


def test_EditDialog_updateSongInfo_unknownTag(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    table_tags: list[SongTag],
) -> None:
    """Tests that updating an unknown tag logs, and doesn't save."""
    _, dialog = _createDialog(qtbot, [0], table_tags, num_songs=1)

    mock_tag = Mock(spec=SongTag)
    test_key: str = "TPE1"
    test_value: str | None = None  # Indicates removal
    mock_tag.id3_key = test_key
    mock_tag.setTag = Mock()
    mock_tag.removeTag = Mock()

    invalid_key = "TIT2"

    monkeypatch.setattr(
        "music_modify.gui.edit.dialog_edit.mapKey",
        lambda key, tags: mock_tag if key == test_key else None,
    )
    monkeypatch.setattr(dialog.song_info, "save", Mock())

    dialog.changed_values = {invalid_key: test_value}

    expected_log_message = "Unknown id3 key: TIT2"

    caplog.set_level(logging.DEBUG, logger="music_modify.gui.edit.dialog_edit")
    with qtbot.assertNotEmitted(dialog.info_updated):
        dialog.updateSongInfo()

        assert expected_log_message in caplog.text

    mock_tag.setTag.assert_not_called()
    mock_tag.removeTag.assert_not_called()
    cast(Mock, dialog.song_info.save).assert_not_called()
    assert not dialog.changed_values


def test_EditDialog_switchButtonState_no_buttons_logged(
    qtbot: QtBot, table_tags: list[SongTag], caplog: pytest.LogCaptureFixture
) -> None:
    """Tests logging when trying to change button state for non-existing buttons."""
    _, dialog = _createDialog(qtbot, [], table_tags, num_songs=0)

    assert not hasattr(dialog, "next_button")
    assert not hasattr(dialog, "previous_button")

    with caplog.at_level(logging.WARNING):
        dialog._switchButtonState()

        assert "Missing next or previous button in edit dialog" in caplog.text
        assert caplog.records[0].levelname == "WARNING"


def test_EditDialog_showSongInDirection_last_or_first_logged(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture, table_tags: list[SongTag]
) -> None:
    """Tests that invalid navigation on first or last is logged."""
    _, dialog = _createDialog(qtbot, [0, 1], table_tags, num_songs=2)

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
    qtbot: QtBot, caplog: pytest.LogCaptureFixture, table_tags: list[SongTag]
) -> None:
    """Tests that trying to display a song at an invalid index closes the dialog."""
    _, dialog = _createDialog(qtbot, [0, 1], table_tags, num_songs=1)

    with caplog.at_level(logging.WARNING):
        dialog.showSongInDirection(NavDirection.Next)
        assert "Invalid song, closing dialog" in caplog.text

    assert dialog.result() == QDialog.DialogCode.Rejected


def test_EditDialog_resetSongInfo(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, table_tags: list[SongTag]
) -> None:
    """Tests that the song values can be reset."""
    widget, repo = _createParentAndRepo(qtbot, 1)
    rows: list[int] = [0]

    mock_reset_method = Mock()
    monkeypatch.setattr(EditAbstractWidget, "reset", mock_reset_method)

    dialog = EditDialog(widget, repo, rows, table_tags)
    qtbot.addWidget(dialog)

    found_widgets = dialog.findChildren(EditAbstractWidget)
    assert len(found_widgets) == len(table_tags)
    mock_reset_method.assert_not_called()

    dialog.resetSongInfo()

    assert mock_reset_method.call_count == len(table_tags)


@pytest.fixture
def edit_dialog_mocks(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, table_tags: list[SongTag]
) -> tuple[EditDialog, Mock, Mock, PropertyMock]:
    """Fixture for creating multiple mocks for EditDialogs."""
    _, dialog = _createDialog(qtbot, [0], table_tags, num_songs=1)

    mock_tag = Mock(spec=SongTag)
    mock_tag.id3_key = "TEST"
    mock_tag.display_name = "Test Tag"
    mock_tag.getValue.return_value = None

    mock_edit_widget = Mock(spec=EditAbstractWidget)
    mock_edit_widget.value_updated = Mock()
    mock_edit_widget.value_updated.connect = Mock()
    mock_edit_widget.value_reset = Mock()
    mock_edit_widget.value_reset.connect = Mock()

    mock_widget_value = PropertyMock()
    type(mock_edit_widget).value = mock_widget_value

    monkeypatch.setattr(
        "music_modify.gui.edit.widget_edit_factory.EditWidgetFactory.createWidget",
        Mock(return_value=mock_edit_widget),
    )

    return dialog, mock_tag, mock_edit_widget, mock_widget_value


def test_EditDialog_createWidgetType_signal_connections(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    """Tests that the signal connections are created for the widgets."""
    dialog, mock_tag, mock_edit_widget, _ = edit_dialog_mocks

    created_widget = dialog._createWidgetType(mock_tag, None)

    assert created_widget is mock_edit_widget
    mock_edit_widget.value_updated.connect.assert_called_once()
    mock_edit_widget.value_reset.connect.assert_called_once()


def test_EditDialog_createWidgetType_updateValue_non_empty(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    """Tests that updating a value in a widget gets stored in `changed_values`."""
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks

    dialog._createWidgetType(mock_tag, None)
    update_slot = mock_edit_widget.value_updated.connect.call_args[0][0]

    dialog.changed_values = {}
    new_value_str = "Updated Value"
    mock_widget_value.return_value = new_value_str
    update_slot()

    assert dialog.changed_values == {mock_tag.id3_key: new_value_str}


def test_EditDialog_createWidgetType_updateValue_empty(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    """Tests that updating a value to be empty stores None in `changed_values`."""
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks

    dialog._createWidgetType(mock_tag, "Initial Value")  # Start with a value
    update_slot = mock_edit_widget.value_updated.connect.call_args[0][0]

    dialog.changed_values = {
        mock_tag.id3_key: "Initial Value"
    }  # Simulate pre-existing change
    empty_value_str = ""
    mock_widget_value.return_value = empty_value_str
    update_slot()

    assert dialog.changed_values == {mock_tag.id3_key: None}


def test_EditDialog_createWidgetType_resetValue_song_none_widget_empty(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    """Tests that adding and then removing a change should reflect no changes."""
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks
    mock_tag.getValue.return_value = None  # Value in song is None

    dialog._createWidgetType(mock_tag, None)
    reset_slot = mock_edit_widget.value_reset.connect.call_args[0][0]

    dialog.changed_values = {
        mock_tag.id3_key: "Some Change"
    }  # Widget value previously changed
    mock_widget_value.return_value = ""  # Widget value is now empty
    reset_slot()

    # Assert: Key should be removed from changed_values
    # as song value was was None and now widget is empty
    assert dialog.changed_values == {}


def test_EditDialog_createWidgetType_resetValue_song_none_widget_non_empty(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    """Tests that removing a change from the song, and then resetting adds it back.

    The idea here is that it's possible for the song to be updated
    by clicking the Apply button.
    And then when we reset, we don't want to get the current value from the song,
    but the _original_ value that was in the song,
    which should be the original value for the widget.
    """
    # This is the case when originally a value was stored in the widget,
    # but the song has been updated since, so we need to store
    # this as a change.
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks
    mock_tag.getValue.return_value = None  # Value currently song is None

    dialog._createWidgetType(mock_tag, None)
    reset_slot = mock_edit_widget.value_reset.connect.call_args[0][0]

    dialog.changed_values = {}
    widget_original_value = "Value Originally in Song"
    mock_widget_value.return_value = widget_original_value
    reset_slot()

    # Assert: Key should be added to changed_values with the widget's value.
    assert dialog.changed_values == {mock_tag.id3_key: widget_original_value}


def test_EditDialog_createWidgetType_resetValue_song_exists_widget_matches_song(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    """Tests resetting widget value when song matches removes from changed_values."""
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks
    song_value = "Song Value"
    mock_tag.getValue.return_value = song_value  # Song value exists

    dialog._createWidgetType(mock_tag, song_value)
    reset_slot = mock_edit_widget.value_reset.connect.call_args[0][0]

    dialog.changed_values = {mock_tag.id3_key: "Some Different Value"}
    mock_widget_value.return_value = song_value
    reset_slot()

    # Assert: Key should be removed from changed_values as it now matches original
    assert dialog.changed_values == {}


def test_EditDialog_createWidgetType_resetValue_song_exists_widget_diff_non_empty(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    """Tests that changing the value in the song, and then resetting sets it back.

    The idea here is that it's possible for the song to be updated
    by clicking the Apply button.
    And then when we reset, we don't want to get the current value from the song,
    but the _original_ value that was in the song,
    which should be the original value for the widget.
    """
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks
    song_value = "Song Current Value"
    mock_tag.getValue.return_value = song_value

    dialog._createWidgetType(mock_tag, song_value)
    reset_slot = mock_edit_widget.value_reset.connect.call_args[0][0]

    dialog.changed_values = {}
    widget_original_value = "Value Originally in Song"
    mock_widget_value.return_value = widget_original_value
    reset_slot()

    # Assert: Key should be updated in changed_values with the widget value.
    assert dialog.changed_values == {mock_tag.id3_key: widget_original_value}


def test_EditDialog_createWidgetType_resetValue_song_exists_widget_empty(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    """Tests that tags added since initialization are removed on reset.

    The idea here is that it's possible for the song to be updated
    by clicking the Apply button.
    And then when we reset, we don't want to get the current value from the song,
    but the _original_ value that was in the song,
    which here doesn't exist, so that tag should be removed.
    """
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks
    song_value = "Original Value"
    mock_tag.getValue.return_value = song_value

    dialog._createWidgetType(mock_tag, song_value)
    reset_slot = mock_edit_widget.value_reset.connect.call_args[0][0]

    dialog.changed_values = {}
    mock_widget_value.return_value = ""  # Widget value is empty
    reset_slot()

    # Assert: Key should be set to None in changed_values, indicating removal from song
    assert dialog.changed_values == {mock_tag.id3_key: None}


def test_EditDialog_createWidgetType_resetValue_preexisting_changed_value_still_diff(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    """Tests that tags updated since initialization are reset to their original values.

    The idea here is that it's possible for the song to be updated
    by clicking the Apply button.
    And then when we reset, we don't want to get the current value from the song,
    but the _original_ value that was in the song,
    which is the original value for the widget.
    """
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks
    song_value = "Original Value"
    mock_tag.getValue.return_value = song_value

    # Act
    dialog._createWidgetType(mock_tag, song_value)
    reset_slot = mock_edit_widget.value_reset.connect.call_args[0][0]

    dialog.changed_values = {mock_tag.id3_key: "First Edit"}
    mock_widget_value.return_value = "Second Edit"  # Still different from original
    reset_slot()

    # Assert: The `changed_values` entry should reflect `Second Edit`
    assert dialog.changed_values == {mock_tag.id3_key: "Second Edit"}
