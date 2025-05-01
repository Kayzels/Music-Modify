from PySide6.QtWidgets import QDialog, QWidget
from .ui_dialog_prefs_tag_add import Ui_AddTagDialog


class AddTagDialog(QDialog, Ui_AddTagDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]
