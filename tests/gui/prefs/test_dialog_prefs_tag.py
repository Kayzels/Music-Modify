"""Tests for PrefsTagDialog."""

import copy
from unittest.mock import MagicMock

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QDialogButtonBox, QMessageBox, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.tag_info import TagInfo
from music_modify.gui.prefs.dialog_prefs_tag import PrefsTagDialog
from music_modify.gui.utils import selectRows
from music_modify.models.tag_model import TagModel
import music_modify.prefs.prefs as prefs_module

_test_tag_info = TagInfo(
    id3_key="TEST",
    display_name="Test Display",
    show_in_table=True,
)


class _MockPrefsTagAddDialog(QObject):
    accepted: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    def show(self) -> None:
        self.accepted.emit()

    @staticmethod
    def addToModel(model: TagModel) -> None:
        id3_key = _test_tag_info.id3_key
        display_name = _test_tag_info.display_name
        show_in_table = _test_tag_info.show_in_table
        model.addTag(
            id3_key=id3_key,
            display_name=display_name,
            show_in_table=show_in_table,
        )


def _createDialog(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> PrefsTagDialog:
    _patchDialogs(monkeypatch, temp_settings)
    dialog = PrefsTagDialog()
    qtbot.addWidget(dialog)
    return dialog


def _patchDialogs(
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    monkeypatch.setattr(prefs_module, "settings", temp_settings)
    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )
    monkeypatch.setattr(
        "music_modify.gui.prefs.dialog_prefs_tag.PrefsTagAddDialog",
        _MockPrefsTagAddDialog,
    )


def _makeChanges(
    dialog: PrefsTagDialog,
) -> list[TagInfo]:
    model = dialog.model
    tags: list[TagInfo] = copy.deepcopy(model.tags)

    table = dialog.tag_table

    # Add row at end
    dialog.add_button.click()
    tags.append(_test_tag_info)

    # Remove some rows
    selectRows(table, [0, 1])
    dialog.remove_button.click()
    tags.pop(1)
    tags.pop(0)

    # Move rows up
    up_rows = [2, 4]
    selectRows(table, [2, 4])
    dialog.up_button.click()
    for row in up_rows:
        tags.insert(row - 1, tags.pop(row))

    # Move rows down
    down_rows = [5, 7]
    selectRows(table, down_rows)
    dialog.down_button.click()
    for row in down_rows:
        tags.insert(row + 1, tags.pop(row))
    return tags


def test_PrefsTagDialog_init(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Tests that creating a PrefsTagDialog works correctly."""
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    assert dialog.tag_table.model().rowCount() == len(temp_settings.info_tags)


def test_PrefsTagDialog_addTag(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Tests that adding a valid tag to the dialog adds it."""
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    model = dialog.model
    before_len = model.rowCount()

    dialog.add_button.click()

    assert model.rowCount() == before_len + 1
    assert model.tags[-1] == _test_tag_info


def test_PrefsTagDialog_removeSelectedTags(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Tests that removing the selected rows works."""
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    model = dialog.model

    table = dialog.tag_table

    tags: list[TagInfo] = copy.deepcopy(model.tags)

    # With nothing selected, should do nothing
    before_len = model.rowCount()
    dialog.remove_button.click()
    assert model.rowCount() == before_len

    # Select the first row and remove
    selectRows(table, [0])
    dialog.remove_button.click()
    tags.pop(0)
    assert model.tags == tags

    # Select second and fourth rows and remove
    rows_to_remove = [2, 4]
    selectRows(table, rows_to_remove)
    dialog.remove_button.click()
    for row in reversed(rows_to_remove):
        tags.pop(row)
    assert model.tags == tags


def test_PrefsTagDialog_moveTagsUp(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Tests that moving tags up in the model works."""
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    model = dialog.model
    tags: list[TagInfo] = copy.deepcopy(model.tags)

    table = dialog.tag_table

    # With nothing selected, should do nothing
    dialog.up_button.click()
    assert model.tags == tags

    # With first row selected, should do nothing
    selectRows(table, [0])
    dialog.up_button.click()
    assert model.tags == tags

    # With second row selected, should swap first and second
    selectRows(table, [1])
    dialog.up_button.click()
    val: TagInfo = tags.pop(1)
    tags.insert(0, val)
    assert model.tags == tags

    # With third and fourth selected, should become second and third
    rows_to_move = [2, 3]
    selectRows(table, rows_to_move)
    dialog.up_button.click()
    for row in rows_to_move:
        tags.insert(row - 1, tags.pop(row))
    assert model.tags == tags


def test_PrefsTagDialog_moveTagsDown(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Tests that moving tags down in the model works."""
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    model = dialog.model
    tags: list[TagInfo] = copy.deepcopy(model.tags)

    table = dialog.tag_table

    # With nothing selected, should do nothing
    dialog.down_button.click()
    assert model.tags == tags

    # With last row selected, should do nothing
    selectRows(table, [len(tags) - 1])
    dialog.down_button.click()
    assert model.tags == tags

    # With second row selected, should swap second and third
    selectRows(table, [1])
    dialog.down_button.click()
    val: TagInfo = tags.pop(1)
    tags.insert(2, val)
    assert model.tags == tags

    # With third and fourth selected, should become fourth and fifth
    rows_to_move = [2, 3]
    selectRows(table, rows_to_move)
    dialog.down_button.click()
    for row in reversed(rows_to_move):
        tags.insert(row + 1, tags.pop(row))
    assert model.tags == tags


def test_PrefsTagDialog_updateSettings(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Tests that calling updateSettings makes changes to the settings values."""
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    orig_tags: list[TagInfo] = copy.deepcopy(dialog.model.tags)
    tags: list[TagInfo] = _makeChanges(dialog)
    dialog.accept()

    assert temp_settings.info_tags == dialog.model.tags
    assert temp_settings.info_tags == tags
    assert temp_settings.info_tags != orig_tags
    assert dialog.model.tags != orig_tags
    assert tags != orig_tags


def test_PrefsTagDialog_restoreDefaults(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Tests that calling restoreDefaults puts the values back to their defaults."""
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    tags: list[TagInfo] = _makeChanges(dialog)
    assert dialog.button_box is not None
    restore_button = dialog.button_box.button(
        QDialogButtonBox.StandardButton.RestoreDefaults,
    )
    restore_button.click()
    assert tags != dialog.model.tags
    assert dialog.model.tags == temp_settings.default_tags


def test_PrefsTagDialog_resetSettings(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Tests that calling resetSettings puts the values back to initial values."""
    dialog1 = _createDialog(qtbot, monkeypatch, temp_settings)
    model1 = dialog1.model
    tags1: list[TagInfo] = copy.deepcopy(model1.tags)
    rows_to_remove = [2, 4]
    table1 = dialog1.tag_table
    selectRows(table1, rows_to_remove)
    dialog1.remove_button.click()
    assert tags1 != model1.tags
    assert len(model1.tags) == len(tags1) - 2
    dialog1.accept()

    dialog2 = _createDialog(qtbot, monkeypatch, temp_settings)
    model2 = dialog2.model
    tags2: list[TagInfo] = copy.deepcopy(model2.tags)
    assert tags1 != model2.tags
    assert model2.tags == model1.tags

    changed_tags: list[TagInfo] = _makeChanges(dialog2)
    assert changed_tags != tags2
    assert changed_tags == model2.tags

    assert dialog2.button_box is not None
    reset_button = dialog2.button_box.button(QDialogButtonBox.StandardButton.Reset)
    reset_button.click()
    assert model2.tags != changed_tags
    assert model2.tags != temp_settings.default_tags


def test_PrefsTagDialog_restore_then_reset(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Tests that restoring defaults then calling reset puts initial values back."""
    dialog1 = _createDialog(qtbot, monkeypatch, temp_settings)
    model1 = dialog1.model
    tags1: list[TagInfo] = copy.deepcopy(model1.tags)
    table1 = dialog1.tag_table
    rows_to_remove = [2, 4]
    selectRows(table1, rows_to_remove)
    dialog1.remove_button.click()
    assert tags1 != model1.tags
    assert len(model1.tags) == len(tags1) - 2
    dialog1.accept()

    dialog2 = _createDialog(qtbot, monkeypatch, temp_settings)
    model2 = dialog2.model
    tags2: list[TagInfo] = copy.deepcopy(model2.tags)
    assert tags1 != model2.tags
    assert model2.tags == model1.tags

    changed_tags: list[TagInfo] = _makeChanges(dialog2)
    assert changed_tags != tags2
    assert changed_tags == model2.tags

    assert dialog2.button_box is not None
    restore_button = dialog2.button_box.button(
        QDialogButtonBox.StandardButton.RestoreDefaults,
    )
    restore_button.click()
    assert dialog2.model.tags == temp_settings.default_tags

    reset_button = dialog2.button_box.button(QDialogButtonBox.StandardButton.Reset)
    reset_button.click()
    assert model2.tags != changed_tags
    assert model2.tags != temp_settings.default_tags


def test_PrefsTagDialog_showInvalidInputMessage(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    """Test that an invalid input message is shown when needed."""
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    qtbot.addWidget(dialog)

    mock_qmessagebox_warning = MagicMock()
    monkeypatch.setattr(QMessageBox, "warning", mock_qmessagebox_warning)

    model = dialog.model
    test_message = "This is a test invalid input message."

    model.invalid_input.emit(test_message)

    mock_qmessagebox_warning.assert_called_once_with(
        dialog.tag_table,
        "Invalid Input",
        test_message,
    )
