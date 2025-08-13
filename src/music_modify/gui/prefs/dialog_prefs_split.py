"""Module that defines the dialog used to let the user change
how multiple values should be entered, and displayed."""

# pyright: reportIncompatibleMethodOverride=false

import logging
from typing import Self, override

from PySide6.QtWidgets import QLineEdit, QWidget

from music_modify.prefs import prefs

from .dialog_prefs_abstract import PrefsAbstractDialog
from .ui_dialog_prefs_split import Ui_PrefsSplitDialog

logger = logging.getLogger(__name__)


class PrefsSplitDialog(PrefsAbstractDialog, Ui_PrefsSplitDialog):
    """Allows the user to edit the values stored in the Split settings section,
    which have to do with how strings are displayed when there are multiple values."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.changed_settings: dict[str, str] = {}
        """Stores the name of the setting that has been changed,
        with its new value. An empty dict implies that nothing has changed."""
        self._initializeDisplay()

        self.line_edit_split_text_entered.editingFinished.connect(
            lambda: self._getSettingChange(
                "split_text_entered",
                self.line_edit_split_text_entered.text(),
            ),
        )
        self.line_edit_split_values_display.editingFinished.connect(
            lambda: self._getSettingChange(
                "split_values_display",
                self.line_edit_split_values_display.text(),
            ),
        )
        self.line_edit_split_values_at.editingFinished.connect(
            lambda: self._getSettingChange(
                "split_values_at",
                self.line_edit_split_values_at.text(),
            ),
        )

    @override
    def setupUi(self, dialog: Self) -> None:
        Ui_PrefsSplitDialog.setupUi(self, dialog)

    def _initializeDisplay(self) -> None:
        """Displays the current values for the split settings
        before the user changes them.
        """
        self.line_edit_split_text_entered.setText(prefs.settings.split_text_entered)
        self.line_edit_split_values_display.setText(prefs.settings.split_values_display)
        self.line_edit_split_values_at.setText(prefs.settings.split_values_at)

    def _getSettingChange(self, setting_name: str, setting_value: str) -> None:
        """Gets the value a specific setting has been changed to.
        Stores this in the list of settings to change, which will be reflected
        when the dialog is confirmed.

        Args:
            setting_name: The name of the setting to change
            setting_value: The new value that the setting should be set to
        """
        logger.debug(
            f"Called _getSettingChange with {setting_name} and {setting_value}",
        )
        if setting_value == "":
            # Don't want to use empty string for values
            return

        if getattr(prefs.settings, setting_name) != setting_value:
            # Set the value in changed_settings if it's different
            self.changed_settings[setting_name] = setting_value
        else:
            # Remove the value if it's set back to previous one
            self.changed_settings.pop(setting_name, None)
        logger.debug(f"Changed settings is {self.changed_settings}")

    @override
    def updateSettings(self) -> None:
        """A slot that should be called from the parent widget when
        the dialog is accepted.
        Changes the values in the settings file to match the ones set in the dialog.
        """
        logger.debug("Called update settings inside split dialog")
        if len(self.changed_settings) > 0:
            for setting_name, setting_value in self.changed_settings.items():
                setattr(prefs.settings, setting_name, setting_value)
            self.settings_updated.emit()

    @override
    def restoreDefaults(self) -> None:
        logger.debug("Restore defaults called for split")

        split_defaults: dict[QLineEdit, str] = {
            self.line_edit_split_text_entered: prefs.settings.default_split_text_entered,  # noqa: E501
            self.line_edit_split_values_at: prefs.settings.default_split_values_at,
            self.line_edit_split_values_display: prefs.settings.default_split_values_display,  # noqa: E501
        }

        for line_edit, text in split_defaults.items():
            if text != line_edit.text():
                line_edit.setText(text)
                # Call this explicitly, otherwise would need to use textChanged slot,
                # which is called on every change (not ideal)
                line_edit.editingFinished.emit()

    @override
    def resetSettings(self) -> None:
        logger.debug("Called reset settings in split")
        if len(self.changed_settings) == 0:
            return

        # TODO:Disable reset button when there are no changes
        self.changed_settings = {}
        self._initializeDisplay()
