import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget

from .dialog_tag import TagDialog
from .dialog_prefs_split import PrefsSplitDialog
from .ui_dialog_prefs import Ui_PrefsDialog

logger = logging.getLogger(__name__)


class PrefsDialog(QDialog, Ui_PrefsDialog):
    settings_updated: Signal = Signal()

    def __init__(self, /, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]

        self.button_edit_tags.clicked.connect(lambda: self.openEditDialog(TagDialog))
        self.button_edit_split.clicked.connect(
            lambda: self.openEditDialog(PrefsSplitDialog)
        )

    def openEditDialog(self, dialog_type: type[TagDialog] | type[PrefsSplitDialog]):
        dialog = dialog_type(self)
        dialog.setModal(True)

        # Process accept result
        def processDialogResult(result: QDialog.DialogCode):
            if result == QDialog.DialogCode.Accepted:
                dialog.updateSettings()

        dialog.settings_updated.connect(lambda: self.settings_updated.emit())
        dialog.finished.connect(processDialogResult)

        dialog.show()

        # TODO: Create parent class or interface that can be for both.
        # They both inherit from QDialog, but they have an extra
        # signal that's needed: settings_updated
        # Would also be useful to explicitly say what functions are needed.
