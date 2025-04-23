from typing import TYPE_CHECKING, TypedDict
from PySide6.QtWidgets import QDialog, QWidget
from .ui_dialog_prefs import Ui_PrefsDialog

if TYPE_CHECKING:
    from music_modify.prefs import _Settings


class SettingPair(TypedDict):
    setting_name: str
    setting_value: str


class PrefsDialog(QDialog, Ui_PrefsDialog):
    def __init__(self, /, parent: QWidget | None = None):
        # Import at runtime to avoid import cycle
        from music_modify.prefs import settings

        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]
        self._settings: _Settings = settings
        self.changed_settings: list[SettingPair] = []
        self.displaySettings()

        self.line_edit_split_text_entered.editingFinished.connect(
            lambda: self.updateSetting(
                "split_text_entered", self.line_edit_split_text_entered.text()
            )
        )
        self.line_edit_split_values_display.editingFinished.connect(
            lambda: self.updateSetting(
                "split_values_display", self.line_edit_split_values_display.text()
            )
        )
        self.line_edit_split_values_at.editingFinished.connect(
            lambda: self.updateSetting(
                "split_values_at", self.line_edit_split_values_at.text()
            )
        )

    def displaySettings(self):
        self.line_edit_split_text_entered.setText(self._settings.split_text_entered)
        self.line_edit_split_values_display.setText(self._settings.split_values_display)
        self.line_edit_split_values_at.setText(self._settings.split_values_at)

    def updateSetting(self, setting_name: str, setting_value: str):
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
        if getattr(self._settings, setting_name) != setting_value:
            self.changed_settings.append(
                {"setting_name": setting_name, "setting_value": setting_value}
            )
        print(self.changed_settings)
