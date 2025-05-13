from PySide6.QtWidgets import QDialog, QWidget
from .ui_dialog_prefs_tag_add import Ui_PrefsTagAddDialog


class PrefsTagAddDialog(QDialog, Ui_PrefsTagAddDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)
