from PySide6.QtWidgets import QDialog, QWidget
from .ui_dialog_reset import Ui_ResetDialog


class ResetDialog(QDialog, Ui_ResetDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]

