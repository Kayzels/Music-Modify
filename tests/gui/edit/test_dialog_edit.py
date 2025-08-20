# pyright: reportPrivateUsage = false

import logging
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


def test_EditDialog_init_no_rows(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    repo = SongRepository()
    rows = []

    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

    assert dialog.result() == QDialog.DialogCode.Rejected


def test_EditDialog_init_song_None(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    repo = SongRepository()
    rows = [0]

    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

    assert dialog.result() == QDialog.DialogCode.Rejected


def test_EditDialog_init_song_single(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    repo.addSong()
    rows = [0]

    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

    assert dialog.song_info is not None
    assert isinstance(dialog.song_info, Song)

    assert not hasattr(dialog, "previous_button")
    assert not hasattr(dialog, "next_button")


def test_EditDialog_init_song_multiple(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    repo.addSong()
    repo.addSong()
    rows = [0, 1]

    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

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
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    repo.addSong()
    rows: list[int] = [0]

    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

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
    with qtbot.waitSignal(dialog.info_updated, timeout=1000):  # pyright: ignore[reportArgumentType]
        dialog.updateSongInfo()

    mock_tag.setTag.assert_called_once_with(dialog.song_info.id3, [test_value])
    mock_tag.removeTag.assert_not_called()
    dialog.song_info.save.assert_called_once()  # pyright: ignore[reportAttributeAccessIssue]
    assert not dialog.changed_values


def test_EditDialog_updateSongInfo_removesValue(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    repo.addSong()
    rows: list[int] = [0]

    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

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
    with qtbot.waitSignal(dialog.info_updated, timeout=1000):  # pyright: ignore[reportArgumentType]
        dialog.updateSongInfo()

    mock_tag.setTag.assert_not_called()
    mock_tag.removeTag.assert_called_once_with(dialog.song_info.id3)
    dialog.song_info.save.assert_called_once()  # pyright: ignore[reportAttributeAccessIssue]
    assert not dialog.changed_values


def test_EditDialog_updateSongInfo_unknownTag(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    repo.addSong()
    rows: list[int] = [0]

    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

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
    with qtbot.assertNotEmitted(dialog.info_updated):  # pyright: ignore[reportArgumentType]
        dialog.updateSongInfo()

        assert expected_log_message in caplog.text

    mock_tag.setTag.assert_not_called()
    mock_tag.removeTag.assert_not_called()
    dialog.song_info.save.assert_not_called()  # pyright: ignore[reportAttributeAccessIssue]
    assert not dialog.changed_values


def test_EditDialog_switchButtonState_no_buttons_logged(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    rows = []
    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

    assert not hasattr(dialog, "next_button")
    assert not hasattr(dialog, "previous_button")

    with caplog.at_level(logging.WARNING):
        dialog._switchButtonState()

        assert "Missing next or previous button in edit dialog" in caplog.text
        assert caplog.records[0].levelname == "WARNING"


def test_EditDialog_showSongInDirection_last_or_first_logged(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    repo.addSong()
    repo.addSong()
    rows = [0, 1]
    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

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
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    repo.addSong()
    rows = [0, 1]
    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

    with caplog.at_level(logging.WARNING):
        dialog.showSongInDirection(NavDirection.Next)
        assert "Invalid song, closing dialog" in caplog.text

    assert dialog.result() == QDialog.DialogCode.Rejected


def test_EditDialog_resetSongInfo(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    repo.addSong()
    rows: list[int] = [0]

    mock_tag1 = Mock(spec=SongTag)
    mock_tag1.display_name = "Artist"
    mock_tag1.getValue.return_value = "Test Artist"
    mock_tag1.id3_key = "TPE1"

    mock_tag2 = Mock(spec=SongTag)
    mock_tag2.display_name = "Title"
    mock_tag2.getValue.return_value = "Test Title"
    mock_tag2.id3_key = "TIT2"

    mock_all_tags = [mock_tag1, mock_tag2]
    mock_prefs_settings = Mock()
    mock_prefs_settings.all_tags = mock_all_tags
    monkeypatch.setattr("music_modify.prefs.prefs.settings", mock_prefs_settings)

    mock_reset_method = Mock()
    monkeypatch.setattr(EditAbstractWidget, "reset", mock_reset_method)

    dialog = EditDialog(widget, repo, rows)
    qtbot.addWidget(dialog)

    found_widgets = dialog.findChildren(EditAbstractWidget)
    assert len(found_widgets) == len(mock_all_tags)
    mock_reset_method.assert_not_called()

    dialog.resetSongInfo()

    assert mock_reset_method.call_count == len(mock_all_tags)


@pytest.fixture
def edit_dialog_mocks(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> tuple[EditDialog, Mock, Mock, PropertyMock]:
    widget = QWidget()
    qtbot.addWidget(widget)

    repo = SongRepository()
    repo.addSong()
    rows: list[int] = [0]

    dialog = EditDialog(widget, repo, rows)
    # NOTE: DO NOT CALL qtbot.addWidget(dialog) here.
    # It leads to some weird Qt error.

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
    dialog, mock_tag, mock_edit_widget, _ = edit_dialog_mocks

    created_widget = dialog._createWidgetType(mock_tag, None)

    assert created_widget is mock_edit_widget
    mock_edit_widget.value_updated.connect.assert_called_once()
    mock_edit_widget.value_reset.connect.assert_called_once()


def test_EditDialog_createWidgetType_updateValue_non_empty(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
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
    # as original was None and now widget is empty
    assert dialog.changed_values == {}


def test_EditDialog_createWidgetType_resetValue_song_none_widget_non_empty(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
    # This is the case when originally a value was stored in the widget,
    # but the song has been updated since, so we need to store
    # this as a change.
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks
    mock_tag.getValue.return_value = None  # Value in song is None

    dialog._createWidgetType(mock_tag, None)
    reset_slot = mock_edit_widget.value_reset.connect.call_args[0][0]

    dialog.changed_values = {}
    non_empty_value = "New Value"
    mock_widget_value.return_value = non_empty_value
    reset_slot()

    # Assert: Key should be added to changed_values with the new value
    assert dialog.changed_values == {mock_tag.id3_key: non_empty_value}


def test_EditDialog_createWidgetType_resetValue_song_exists_widget_matches_song(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
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
    dialog, mock_tag, mock_edit_widget, mock_widget_value = edit_dialog_mocks
    song_value = "Song Value"
    mock_tag.getValue.return_value = song_value

    dialog._createWidgetType(mock_tag, song_value)
    reset_slot = mock_edit_widget.value_reset.connect.call_args[0][0]

    dialog.changed_values = {}
    new_different_value = "New Different Value"
    mock_widget_value.return_value = new_different_value
    reset_slot()

    # Assert: Key should be updated in changed_values with the new different value
    assert dialog.changed_values == {mock_tag.id3_key: new_different_value}


def test_EditDialog_createWidgetType_resetValue_original_exists_widget_empty(
    edit_dialog_mocks: tuple[EditDialog, Mock, Mock, PropertyMock],
) -> None:
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
