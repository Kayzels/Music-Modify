# pyright: reportIncompatibleMethodOverride=false

import copy
import logging
from typing import override, Self

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QWidget

from music_modify.custom_types import TagInfo
from music_modify.gui.utils import getSelectedRows
from music_modify.models import TagModel
from music_modify.prefs import prefs

from .ui_dialog_prefs_tag import Ui_PrefsTagDialog
from .dialog_prefs_tag_add import PrefsTagAddDialog
from .dialog_prefs_abstract import PrefsAbstractDialog

logger = logging.getLogger(__name__)


class PrefsTagDialog(PrefsAbstractDialog, Ui_PrefsTagDialog):
    """Allows the user to edit the metadata tags that are edited and displayed for songs."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Tags")

        tags: list[TagInfo] = copy.deepcopy(prefs.settings.info_tags)
        self.original_tags: list[TagInfo] = copy.deepcopy(prefs.settings.info_tags)

        self.model: TagModel = TagModel(tags)
        self.tag_table.setModel(self.model)
        self.tag_table.resizeColumnsToContents()
        self.tag_table.setShowGrid(False)
        self.tag_table.setAlternatingRowColors(True)
        self.model.invalid_input.connect(self.showInvalidInputMessage)

        self.add_toolbutton.clicked.connect(self.addTag)
        self.remove_toolbutton.clicked.connect(self.removeSelectedTags)
        self.up_toolbutton.clicked.connect(self.moveTagsUp)
        self.down_toolbutton.clicked.connect(self.moveTagsDown)

    @override
    def setupUi(self, dialog: Self):
        Ui_PrefsTagDialog.setupUi(self, dialog)

    def addTag(self):
        """Add a new tag to the group of tags that can be used."""
        add_dialog = PrefsTagAddDialog(self)
        add_dialog.accepted.connect(lambda: add_dialog.addToModel(self.model))
        add_dialog.show()

    def removeSelectedTags(self):
        """Remove selected tags from the table and settings."""
        selected_rows = getSelectedRows(self.tag_table)

        if len(selected_rows) == 0:
            return

        # Construct warning message
        delete_message = "Are you sure you want to remove the tags with the info:\n"
        for row in selected_rows:
            for col in range(self.model.columnCount()):
                header_val = self.model.headerData(
                    col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
                )
                cell_index = self.model.index(row, col)
                data = self.model.data(cell_index, Qt.ItemDataRole.DisplayRole)
                delete_message += (
                    f"{header_val if header_val is not None else ''}: "
                    f"{data if data is not None else 'empty'}\n"
                )

        # Show warning dialog with constructed message
        reply = QMessageBox.warning(
            self,
            "Remove Tags",
            delete_message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        # Remove tags if user confirms
        if reply == QMessageBox.StandardButton.Yes:
            for row in sorted(selected_rows, reverse=True):
                self.model.removeTag(row)

    def moveTagsUp(self) -> None:
        """Moves all selected tags up, which will change their order in the main table."""
        selected_rows = sorted(getSelectedRows(self.tag_table))
        if not selected_rows or selected_rows[0] == 0:
            return  # Can't move the first row up

        for row in selected_rows:
            self.model.moveTag(row, row - 1)

    def moveTagsDown(self) -> None:
        """Moves all selected tags down, which will change their order in the main table."""
        selected_rows = sorted(getSelectedRows(self.tag_table), reverse=True)
        if not selected_rows or selected_rows[0] == self.model.rowCount() - 1:
            return  # Can't move the last row down

        for row in selected_rows:
            self.model.moveTag(row, row + 1)

    def showInvalidInputMessage(self, message: str):
        """Displays a message about invalid input."""
        QMessageBox.warning(self.tag_table, "Invalid Input", message)

    @override
    def updateSettings(self) -> None:
        """A slot that should be called from the parent widget when the dialog is accepted.
        Changes the values in the settings file to match the ones set in the dialog.
        """
        logger.info("Called update settings inside tag dialog")
        prefs.settings.info_tags = self.model.tags
        self.settings_updated.emit()

    @override
    def restoreDefaults(self) -> None:
        logger.debug("Restore defaults called for tag")
        self.model.tags = prefs.settings.default_tags

    @override
    def resetSettings(self) -> None:
        logger.debug("Called reset settings in tag")
        """Reset the settings to the values they had when the dialog opened."""
        self.model.tags = self.original_tags
