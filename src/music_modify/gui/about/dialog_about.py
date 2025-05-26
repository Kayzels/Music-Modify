from PySide6.QtWidgets import QDialog, QWidget

from .ui_dialog_about import Ui_AboutDialog


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent: QWidget | None = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
