import logging
from typing import TypedDict

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget

from music_modify.prefs import prefs

from .dialog_tag import TagDialog
from .ui_dialog_prefs import Ui_PrefsDialog

logger = logging.getLogger(__name__)


class SettingPair(TypedDict):
    setting_name: str
    setting_value: str


class PrefsDialog(QDialog, Ui_PrefsDialog):
    settings_updated: Signal = Signal()

    def __init__(self, /, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]
        self.changed_settings: list[SettingPair] = []
        self.displaySettings()

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
        self.button_edit_tags.clicked.connect(self.showTags)

    def displaySettings(self):
        self.line_edit_split_text_entered.setText(prefs.settings.split_text_entered)
        self.line_edit_split_values_display.setText(prefs.settings.split_values_display)
        self.line_edit_split_values_at.setText(prefs.settings.split_values_at)

    def _getSettingChange(self, setting_name: str, setting_value: str):
        """Gets the value a specific setting has been changed to.
        Stores this in the list of settings to change, which will be reflected
        when the dialog is confirmed."""
        # TODO: Change format to also deal with lists of tags?
        if setting_value == "":
            # Don't want to use empty string for values
            return

        # Remove the setting for the current name
        self.changed_settings = [
            setting
            for setting in self.changed_settings
            if setting["setting_name"] != setting_name
        ]

        # Add the new value to the list of changed settings,
        # if it's different than the original setting.
        if getattr(prefs.settings, setting_name) != setting_value:
            self.changed_settings.append(
                {"setting_name": setting_name, "setting_value": setting_value}
            )

    def showTags(self):
        dialog = TagDialog(self, prefs.settings.info_tags)
        dialog.show()

    def updateSettings(self):
        if len(self.changed_settings) > 0:
            for change in self.changed_settings:
                setattr(prefs.settings, change["setting_name"], change["setting_value"])
            # Create a signal for knowing when it's updated, because this will need
            # to refresh the main table
            self.settings_updated.emit()
