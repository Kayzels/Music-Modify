"""Module for the dialog shown when changing songs.
    """
from typing import List, Union

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QWidget

from gui.dialog_selection import Ui_FileSelectionDialog

from models import SongTableModel, SongTableProxyModel


class FileSelectionDialog(QDialog, Ui_FileSelectionDialog):
    """Dialog shown when changing songs.
        """
    def __init__(self,
                 parent: QWidget,
                 model: Union[SongTableModel, SongTableProxyModel],
                 ):
        """Constructor for File Selection Dialog.

            Parameters
            ----------
            parent : QWidget -
                Parent of the dialog.
                What widget the dialog should be shown on top of.\n
            model : Union[SongTableModel, SongTableProxyModel] -
                The Model of the Songs that should be shown.\n
            """
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.ok_button = self.buttonBox.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)

        self.selection: List[QModelIndex] = []

        self.model = model
        self.changeSelectionTableView.setModel(model)

        self.selectAllPushButton.clicked.connect(
            self.changeSelectionTableView.selectAll)
        self.selectNonePushButton.clicked.connect(
            self.changeSelectionTableView.clearSelection)
        self.changeSelectionTableView.selectionModel()\
            .selectionChanged.connect(self.get_selection)

    def get_selection(self, *_):
        """Get which songs have been selected within the table view.
        """
        self.selection = self.changeSelectionTableView\
            .selectionModel().selectedRows()
        selection_length = len(self.selection)
        self.ok_button.setEnabled(selection_length != 0)

    def accept(self):
        """Whether the dialog should be accepted or not.\n
            Reimplemented to check whether the OK button is enabled.
        """
        if self.ok_button.isEnabled():
            QDialog.accept(self)
