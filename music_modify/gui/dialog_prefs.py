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

        self.button_edit_tags.clicked.connect(self.editTags)
        self.button_edit_split.clicked.connect(self.editSplit)

    def editTags(self) -> None:
        dialog = TagDialog(self)
        dialog.setModal(True)

        # Process accept result
        def processDialogResult(result: QDialog.DialogCode):
            if result == QDialog.DialogCode.Accepted:
                dialog.updateSettings()

        dialog.settings_updated.connect(lambda: self.settings_updated.emit())
        dialog.finished.connect(processDialogResult)

        dialog.show()

    def editSplit(self) -> None:
        dialog = PrefsSplitDialog(self)
        dialog.setModal(True)

        # Process accept result
        def processDialogResult(result: QDialog.DialogCode):
            if result == QDialog.DialogCode.Accepted:
                dialog.updateSettings()

        dialog.settings_updated.connect(lambda: self.settings_updated.emit())
        dialog.finished.connect(processDialogResult)

        dialog.show()
