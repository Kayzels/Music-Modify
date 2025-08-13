import copy

from PySide6.QtCore import QItemSelectionModel, QObject, Signal
from PySide6.QtWidgets import QDialogButtonBox, QMessageBox, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.tag_info import TagInfo
from music_modify.gui.prefs.dialog_prefs_tag import PrefsTagDialog
from music_modify.models.tag_model import TagModel
import music_modify.prefs.prefs as prefs_module

_testTagInfo = TagInfo(id3_key="TEST", display_name="Test Display", show_in_table=True)


class MockPrefsTagAddDialog(QObject):
    accepted: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    def show(self) -> None:
        self.accepted.emit()

    @staticmethod
    def addToModel(model: TagModel) -> None:
        id3_key = _testTagInfo.id3_key
        display_name = _testTagInfo.display_name
        show_in_table = _testTagInfo.show_in_table
        model.addTag(
            id3_key=id3_key,
            display_name=display_name,
            show_in_table=show_in_table,
        )


def _selectRows(dialog: PrefsTagDialog, rows: list[int]) -> None:
    model = dialog.tag_table.model()
    selection_model = dialog.tag_table.selectionModel()
    selection_model.clearSelection()
    for row in rows:
        # noinspection PyTypeChecker
        selection_model.select(
            model.index(row, 0),
            QItemSelectionModel.SelectionFlag.Select
            | QItemSelectionModel.SelectionFlag.Rows,
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
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,  # pyright: ignore[reportUnknownLambdaType]
    )
    monkeypatch.setattr(
        "music_modify.gui.prefs.dialog_prefs_tag.PrefsTagAddDialog",
        MockPrefsTagAddDialog,
    )


def _makeChanges(dialog: PrefsTagDialog) -> list[TagInfo]:
    model = dialog.model
    tags: list[TagInfo] = copy.deepcopy(model.tags)

    # Add row at end
    dialog.add_toolbutton.click()
    tags.append(_testTagInfo)

    # Remove some rows
    _selectRows(dialog, [0, 1])
    dialog.remove_toolbutton.click()
    tags.pop(1)
    tags.pop(0)

    # Move rows up
    up_rows = [2, 4]
    _selectRows(dialog, up_rows)
    dialog.up_toolbutton.click()
    for row in up_rows:
        tags.insert(row - 1, tags.pop(row))

    # Move rows down
    down_rows = [5, 7]
    _selectRows(dialog, down_rows)
    dialog.down_toolbutton.click()
    for row in down_rows:
        tags.insert(row + 1, tags.pop(row))
    return tags


def test_PrefsTagDialog_init(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    assert dialog.tag_table.model().rowCount() == len(temp_settings.info_tags)


def test_PrefsTagDialog_addTag(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    model = dialog.model
    before_len = model.rowCount()

    dialog.add_toolbutton.click()

    assert model.rowCount() == before_len + 1
    assert model.tags[-1] == _testTagInfo


def test_PrefsTagDialog_removeSelectedTags(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    model = dialog.model

    tags: list[TagInfo] = copy.deepcopy(model.tags)

    # With nothing selected, should do nothing
    before_len = model.rowCount()
    dialog.remove_toolbutton.click()
    assert model.rowCount() == before_len

    # Select the first row and remove
    _selectRows(dialog, [0])
    dialog.remove_toolbutton.click()
    tags.pop(0)
    assert model.tags == tags

    # Select second and fourth rows and remove
    rows_to_remove = [2, 4]
    _selectRows(dialog, rows_to_remove)
    dialog.remove_toolbutton.click()
    for row in reversed(rows_to_remove):
        tags.pop(row)
    assert model.tags == tags


def test_PrefsTagDialog_moveTagsUp(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    model = dialog.model
    tags: list[TagInfo] = copy.deepcopy(model.tags)

    # With nothing selected, should do nothing
    dialog.up_toolbutton.click()
    assert model.tags == tags

    # With first row selected, should do nothing
    _selectRows(dialog, [0])
    dialog.up_toolbutton.click()
    assert model.tags == tags

    # With second row selected, should swap first and second
    _selectRows(dialog, [1])
    dialog.up_toolbutton.click()
    val: TagInfo = tags.pop(1)
    tags.insert(0, val)
    assert model.tags == tags

    # With third and fourth selected, should become second and third
    rows_to_move = [2, 3]
    _selectRows(dialog, rows_to_move)
    dialog.up_toolbutton.click()
    for row in rows_to_move:
        tags.insert(row - 1, tags.pop(row))
    assert model.tags == tags


def test_PrefsTagDialog_moveTagsDown(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    dialog = _createDialog(qtbot, monkeypatch, temp_settings)
    model = dialog.model
    tags: list[TagInfo] = copy.deepcopy(model.tags)

    # With nothing selected, should do nothing
    dialog.down_toolbutton.click()
    assert model.tags == tags

    # With last row selected, should do nothing
    _selectRows(dialog, [len(tags) - 1])
    dialog.down_toolbutton.click()
    assert model.tags == tags

    # With second row selected, should swap second and third
    _selectRows(dialog, [1])
    dialog.down_toolbutton.click()
    val: TagInfo = tags.pop(1)
    tags.insert(2, val)
    assert model.tags == tags

    # With third and fourth selected, should become fourth and fifth
    rows_to_move = [2, 3]
    _selectRows(dialog, rows_to_move)
    dialog.down_toolbutton.click()
    for row in reversed(rows_to_move):
        tags.insert(row + 1, tags.pop(row))
    assert model.tags == tags


def test_PrefsTagDialog_updateSettings(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
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
    dialog1 = _createDialog(qtbot, monkeypatch, temp_settings)
    model1 = dialog1.model
    tags1: list[TagInfo] = copy.deepcopy(model1.tags)
    rows_to_remove = [2, 4]
    _selectRows(dialog1, rows_to_remove)
    dialog1.remove_toolbutton.click()
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
    dialog1 = _createDialog(qtbot, monkeypatch, temp_settings)
    model1 = dialog1.model
    tags1: list[TagInfo] = copy.deepcopy(model1.tags)
    rows_to_remove = [2, 4]
    _selectRows(dialog1, rows_to_remove)
    dialog1.remove_toolbutton.click()
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
