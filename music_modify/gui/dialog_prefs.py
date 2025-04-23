from PySide6.QtWidgets import QDialog, QWidget
from .ui_dialog_prefs import Ui_PrefsDialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from music_modify.prefs import _Settings


class PrefsDialog(QDialog, Ui_PrefsDialog):
    def __init__(self, /, parent: QWidget | None = None):
        # Import at runtime to avoid import cycle
        from music_modify.prefs import settings

        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]
        self._settings: _Settings = settings
        self.displaySettings()

    def displaySettings(self):
        self.line_edit_split_text_entered.setText(self._settings.split_text_entered)
        self.line_edit_split_values_display.setText(self._settings.split_values_display)
        self.line_edit_split_values_at.setText(self._settings.split_values_at)
