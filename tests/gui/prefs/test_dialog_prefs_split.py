from PySide6.QtWidgets import QDialogButtonBox
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.prefs.dialog_prefs_split import PrefsSplitDialog
import music_modify.prefs.prefs as prefs_module


def test_prefsSplitDialog_init(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    monkeypatch.setattr(prefs_module, "settings", temp_settings)
    split_dialog = PrefsSplitDialog()
    qtbot.addWidget(split_dialog)

    assert (
        split_dialog.line_edit_split_text_entered.text()
        == temp_settings.split_text_entered
    )
    assert (
        split_dialog.line_edit_split_values_at.text() == temp_settings.split_values_at
    )
    assert (
        split_dialog.line_edit_split_values_display.text()
        == temp_settings.split_values_display
    )


def test_prefsSplitDialog_line_edit_single(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    monkeypatch.setattr(prefs_module, "settings", temp_settings)
    split_dialog = PrefsSplitDialog()
    qtbot.addWidget(split_dialog)

    split_dialog.line_edit_split_text_entered.setText("++")
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    assert split_dialog.changed_settings == {"split_text_entered": "++"}

    split_dialog.line_edit_split_text_entered.setText(
        temp_settings.default_split_text_entered,
    )
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    assert split_dialog.changed_settings == {}


def test_prefsSplitDialog_line_edit_multiple(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    monkeypatch.setattr(prefs_module, "settings", temp_settings)
    split_dialog = PrefsSplitDialog()
    qtbot.addWidget(split_dialog)

    split_dialog.line_edit_split_text_entered.setText("++")
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    assert split_dialog.changed_settings == {"split_text_entered": "++"}
    split_dialog.line_edit_split_values_display.setText("..")
    split_dialog.line_edit_split_values_display.editingFinished.emit()
    assert split_dialog.changed_settings == {
        "split_text_entered": "++",
        "split_values_display": "..",
    }
    split_dialog.line_edit_split_values_at.setText("--")
    split_dialog.line_edit_split_values_at.editingFinished.emit()
    assert split_dialog.changed_settings == {
        "split_text_entered": "++",
        "split_values_display": "..",
        "split_values_at": "--",
    }

    split_dialog.line_edit_split_text_entered.setText(
        temp_settings.default_split_text_entered,
    )
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    assert split_dialog.changed_settings == {
        "split_values_display": "..",
        "split_values_at": "--",
    }
    split_dialog.line_edit_split_values_at.setText(
        temp_settings.default_split_values_at,
    )
    split_dialog.line_edit_split_values_at.editingFinished.emit()
    assert split_dialog.changed_settings == {
        "split_values_display": "..",
    }
    split_dialog.line_edit_split_values_display.setText(
        temp_settings.default_split_values_display,
    )
    split_dialog.line_edit_split_values_display.editingFinished.emit()
    assert split_dialog.changed_settings == {}


def test_prefsSplitDialog_updateSettings(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    monkeypatch.setattr(prefs_module, "settings", temp_settings)
    split_dialog = PrefsSplitDialog()
    qtbot.addWidget(split_dialog)

    split_dialog.line_edit_split_text_entered.setText("++")
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    split_dialog.line_edit_split_values_display.setText("..")
    split_dialog.line_edit_split_values_display.editingFinished.emit()
    split_dialog.line_edit_split_values_at.setText("--")
    split_dialog.line_edit_split_values_at.editingFinished.emit()

    split_dialog.accept()
    assert temp_settings.split_text_entered == "++"
    assert temp_settings.split_values_display == ".."
    assert temp_settings.split_values_at == "--"


def test_prefsSplitDialog_restoreDefaults(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    monkeypatch.setattr(prefs_module, "settings", temp_settings)
    split_dialog = PrefsSplitDialog()
    qtbot.addWidget(split_dialog)

    split_dialog.line_edit_split_text_entered.setText("++")
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    split_dialog.line_edit_split_values_display.setText("..")
    split_dialog.line_edit_split_values_display.editingFinished.emit()
    split_dialog.line_edit_split_values_at.setText("--")
    split_dialog.line_edit_split_values_at.editingFinished.emit()

    assert split_dialog.button_box is not None
    restore_button = split_dialog.button_box.button(
        QDialogButtonBox.StandardButton.RestoreDefaults,
    )
    restore_button.click()
    assert (
        split_dialog.line_edit_split_text_entered.text()
        == temp_settings.default_split_text_entered
    )
    assert (
        split_dialog.line_edit_split_values_display.text()
        == temp_settings.default_split_values_display
    )
    assert (
        split_dialog.line_edit_split_values_at.text()
        == temp_settings.default_split_values_at
    )


def test_prefsSplitDialog_resetSettings(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    monkeypatch.setattr(prefs_module, "settings", temp_settings)
    temp_settings.split_text_entered = "::"
    temp_settings.split_values_display = "::"
    temp_settings.split_values_at = "::"
    split_dialog = PrefsSplitDialog()
    qtbot.addWidget(split_dialog)

    # Ensure that nothing changes if settings is empty
    split_dialog.resetSettings()

    assert split_dialog.line_edit_split_text_entered.text() == "::"
    assert split_dialog.line_edit_split_values_at.text() == "::"
    assert split_dialog.line_edit_split_values_display.text() == "::"

    split_dialog.line_edit_split_text_entered.setText("++")
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    split_dialog.line_edit_split_values_display.setText("..")
    split_dialog.line_edit_split_values_display.editingFinished.emit()
    split_dialog.line_edit_split_values_at.setText("--")
    split_dialog.line_edit_split_values_at.editingFinished.emit()

    assert split_dialog.button_box is not None
    reset_button = split_dialog.button_box.button(QDialogButtonBox.StandardButton.Reset)
    reset_button.click()
    assert split_dialog.line_edit_split_text_entered.text() == "::"
    assert split_dialog.line_edit_split_values_at.text() == "::"
    assert split_dialog.line_edit_split_values_display.text() == "::"


def test_prefsSplitDialog_line_edit_empty(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    temp_settings: prefs_module.Settings,
) -> None:
    monkeypatch.setattr(prefs_module, "settings", temp_settings)
    split_dialog = PrefsSplitDialog()
    qtbot.addWidget(split_dialog)

    split_dialog.line_edit_split_text_entered.setText("")
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    assert split_dialog.changed_settings == {}
    split_dialog.line_edit_split_text_entered.setText("++")
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    assert split_dialog.changed_settings == {"split_text_entered": "++"}
    split_dialog.line_edit_split_text_entered.setText("")
    split_dialog.line_edit_split_text_entered.editingFinished.emit()
    assert split_dialog.changed_settings == {}
