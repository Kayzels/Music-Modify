"""Module that defines the main dialog that is used to change the program settings."""

import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget

from .dialog_prefs_abstract import PrefsAbstractDialog
from .dialog_prefs_split import PrefsSplitDialog
from .dialog_prefs_tag import PrefsTagDialog
from .ui_dialog_prefs import Ui_PrefsDialog

logger = logging.getLogger(__name__)


class PrefsDialog(QDialog, Ui_PrefsDialog):
    """A dialog that allows the user to change the settings the program uses."""

    settings_updated: Signal = Signal()
    "Signal that is emitted whenever any setting is changed."

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a PrefsDialog.

        Args:
            parent: The widget that the dialog should be displayed on.
        """
        super().__init__(parent)
        self.setupUi(self)

        self.button_edit_tags.clicked.connect(
            lambda: self.openChildDialog(PrefsTagDialog),
        )
        self.button_edit_split.clicked.connect(
            lambda: self.openChildDialog(PrefsSplitDialog),
        )

    def openChildDialog(self, dialog_type: type[PrefsAbstractDialog]) -> None:
        """Opens a dialog of the specified type to edit those specific setting groups.

        Args:
            dialog_type: The specific type of child dialog that should be opened.
        """
        dialog = dialog_type(self)
        dialog.setModal(True)

        dialog.settings_updated.connect(lambda: self.settings_updated.emit())

        dialog.show()
