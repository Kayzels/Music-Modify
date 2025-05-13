import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget

from .dialog_prefs_abstract import PrefsAbstractDialog
from .dialog_prefs_tag import PrefsTagDialog
from .dialog_prefs_split import PrefsSplitDialog
from .ui_dialog_prefs import Ui_PrefsDialog

logger = logging.getLogger(__name__)


class PrefsDialog(QDialog, Ui_PrefsDialog):
    """A dialog that allows the user to change the settings the program uses."""

    settings_updated: Signal = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)

        self.button_edit_tags.clicked.connect(
            lambda: self.openChildDialog(PrefsTagDialog)
        )
        self.button_edit_split.clicked.connect(
            lambda: self.openChildDialog(PrefsSplitDialog)
        )

    def openChildDialog(self, dialog_type: type[PrefsAbstractDialog]):
        """Opens a dialog of the specified type to allow editing those specific setting groups."""
        dialog = dialog_type(self)
        dialog.setModal(True)

        # Process accept result
        def processDialogResult(result: QDialog.DialogCode):
            """Update the settings stored when the user accepts the child dialog."""
            if result == QDialog.DialogCode.Accepted:
                dialog.updateSettings()

        dialog.settings_updated.connect(lambda: self.settings_updated.emit())
        dialog.finished.connect(processDialogResult)

        dialog.show()
