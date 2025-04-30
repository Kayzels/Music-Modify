import logging
from typing import cast

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget

from music_modify.prefs import prefs
from music_modify.custom_types import TagInfo

from .dialog_tag import TagDialog
from .ui_dialog_prefs import Ui_PrefsDialog

logger = logging.getLogger(__name__)


class PrefsDialog(QDialog, Ui_PrefsDialog):
    settings_updated: Signal = Signal()

    def __init__(self, /, parent: QWidget | None = None):
        super().__init__(parent)
        self.changed_settings: dict[str, str | list[TagInfo]] = {}
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]
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
        self.button_edit_tags.clicked.connect(self.editTags)

    def displaySettings(self):
        self.line_edit_split_text_entered.setText(prefs.settings.split_text_entered)
        self.line_edit_split_values_display.setText(prefs.settings.split_values_display)
        self.line_edit_split_values_at.setText(prefs.settings.split_values_at)

    def _getSettingChange(self, setting_name: str, setting_value: str | list[TagInfo]):
        """Gets the value a specific setting has been changed to.
        Stores this in the list of settings to change, which will be reflected
        when the dialog is confirmed."""
        if setting_value == "":
            # Don't want to use empty string for values
            return

        if (
            isinstance(setting_value, list)
            or getattr(prefs.settings, setting_name) != setting_value
        ):
            self.changed_settings[setting_name] = setting_value

    def editTags(self):
        # Ensure it's a copy, to avoid modifying the existing list.
        # Check if already in changed_settings, and use that
        tags: list[TagInfo] = cast(
            list[TagInfo],
            self.changed_settings.get("info_tags", prefs.settings.info_tags),
        ).copy()

        dialog = TagDialog(self, tags)

        # Other parts of the program shouldn't be interacted with
        # while the dialog is open
        dialog.setModal(True)

        def processDialogResult(result: QDialog.DialogCode):
            # If the dialog is accepted, update the changed_settings dictionary value
            if result == QDialog.DialogCode.Accepted:
                self._getSettingChange("info_tags", dialog.model._tags)

        # TODO: Add warning to TagDialog to say tags are only updated on preference close.

        dialog.finished.connect(processDialogResult)
        dialog.show()

    def updateSettings(self):
        if len(self.changed_settings) > 0:
            for setting_name, setting_value in self.changed_settings.items():
                setattr(prefs.settings, setting_name, setting_value)
            # Create a signal for knowing when it's updated, because this will need
            # to refresh the main table
            self.settings_updated.emit()

    # TODO: Add way of setting back to defaults.
