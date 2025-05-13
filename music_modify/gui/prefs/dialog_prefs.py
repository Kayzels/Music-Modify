import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget

from .dialog_prefs_abstract import PrefsAbstractDialog
from .dialog_prefs_tag import PrefsTagDialog
from .dialog_prefs_split import PrefsSplitDialog
from .ui_dialog_prefs import Ui_PrefsDialog

logger = logging.getLogger(__name__)


class PrefsDialog(QDialog, Ui_PrefsDialog):
    settings_updated: Signal = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]

        self.button_edit_tags.clicked.connect(
            lambda: self.openChildDialog(PrefsTagDialog)
        )
        self.button_edit_split.clicked.connect(
            lambda: self.openChildDialog(PrefsSplitDialog)
        )

    def openChildDialog(self, dialog_type: type[PrefsAbstractDialog]):
        dialog = dialog_type(self)
        dialog.setModal(True)

        # Process accept result
        def processDialogResult(result: QDialog.DialogCode):
            if result == QDialog.DialogCode.Accepted:
                dialog.updateSettings()

        dialog.settings_updated.connect(lambda: self.settings_updated.emit())
        dialog.finished.connect(processDialogResult)

        dialog.show()
