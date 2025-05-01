from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget

from music_modify.prefs import prefs

from .ui_dialog_prefs_split import Ui_PrefsSplitDialog


class PrefsSplitDialog(QDialog, Ui_PrefsSplitDialog):
    settings_updated: Signal = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]

        self.changed_settings: dict[str, str] = {}
        self._initializeDisplay()

        self.line_edit_split_text_entered.editingFinished.connect(
            lambda: self._getSettingChange(
                "split_text_entered", self.line_edit_split_text_entered.text()
            )
        )
        self.line_edit_split_values_display.editingFinished.connect(
            lambda: self._getSettingChange(
                "split_values_display", self.line_edit_split_values_display.text()
            )
        )
        self.line_edit_split_values_at.editingFinished.connect(
            lambda: self._getSettingChange(
                "split_values_at", self.line_edit_split_values_at.text()
            )
        )

        # TODO: Store values of the settings on entry, to allow reset?

    def _initializeDisplay(self):
        self.line_edit_split_text_entered.setText(prefs.settings.split_text_entered)
        self.line_edit_split_values_display.setText(prefs.settings.split_values_display)
        self.line_edit_split_values_at.setText(prefs.settings.split_values_at)

    def _getSettingChange(self, setting_name: str, setting_value: str):
        """Gets the value a specific setting has been changed to.
        Stores this in the list of settings to change, which will be reflected
        when the dialog is confirmed."""
        if setting_value == "":
            # Don't want to use empty string for values
            return

        if getattr(prefs.settings, setting_name) != setting_value:
            # Set the value in changed_settings if it's different
            self.changed_settings[setting_name] = setting_value
        else:
            # Remove the value if it's set back to previous one
            self.changed_settings.pop(setting_name, None)

    def _updateDisplay(self) -> None:
        """Update the values inside the line edits.
        Needed because prefs.settings shouldn't be updated until confirmed,
        but the value can be changed programmatically."""
        line_edits = {
            "split_text_entered": self.line_edit_split_text_entered,
            "split_values_at": self.line_edit_split_values_at,
            "split_values_display": self.line_edit_split_values_display,
        }
        for name, line_edit in line_edits.items():
            if name in self.changed_settings:
                line_edit.setText(self.changed_settings[name])

    def updateSettings(self):
        """A slot that should be called from the parent widget when the dialog is accepted.
        Changes the values in the settings file to match the ones set in the dialog.
        """
        if len(self.changed_settings) > 0:
            for setting_name, setting_value in self.changed_settings.items():
                setattr(prefs.settings, setting_name, setting_value)
            self.settings_updated.emit()

    def restoreDefaults(self) -> None:
        split_defaults = {
            "split_text_entered": prefs.settings.default_split_text_entered,
            "split_values_at": prefs.settings.default_split_values_at,
            "split_values_display": prefs.settings.default_split_values_display,
        }
        for setting_name, setting_value in split_defaults.items():
            self._getSettingChange(setting_name, setting_value)

        # Change the display to reflect the defaults
        if len(self.changed_settings) > 0:
            self._updateDisplay()

    def resetSettings(self) -> None:
        """Should reset the settings to the values they had when opening"""
        if len(self.changed_settings) == 0:
            return

        # TODO:Disable reset button when there are no changes
        self.changed_settings = {}
        self._initializeDisplay()
