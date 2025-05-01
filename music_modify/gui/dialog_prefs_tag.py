import copy
import logging
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QWidget

from music_modify.custom_types import TagInfo
from music_modify.models import TagModel
from music_modify.prefs import prefs

from .ui_dialog_prefs_tag import Ui_PrefsTagDialog
from .dialog_prefs_tag_add import PrefsTagAddDialog
from .dialog_prefs_abstract import PrefsAbstractDialog

logger = logging.getLogger(__name__)


class PrefsTagDialog(PrefsAbstractDialog, Ui_PrefsTagDialog):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]
        self.setWindowTitle("Edit Tags")

        tags: list[TagInfo] = copy.deepcopy(prefs.settings.info_tags)
        self.original_tags: list[TagInfo] = copy.deepcopy(prefs.settings.info_tags)

        self.model: TagModel = TagModel(tags)
        self.tag_table.setModel(self.model)
        self.tag_table.resizeColumnsToContents()
        self.model.invalid_input.connect(self.showInvalidInputMessage)

        self.add_toolbutton.clicked.connect(self.addTag)
        self.remove_toolbutton.clicked.connect(self.removeSelectedTags)
        self.up_toolbutton.clicked.connect(self.moveTagsUp)
        self.down_toolbutton.clicked.connect(self.moveTagsDown)

        self.button_box.button(
            QDialogButtonBox.StandardButton.RestoreDefaults
        ).clicked.connect(self.restoreDefaults)

        self.button_box.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(
            self.resetSettings
        )

    def addTag(self):
        add_dialog = PrefsTagAddDialog(self)

        def processDialogResult(result: QDialog.DialogCode):
            if result == QDialog.DialogCode.Accepted:
                id3_key = add_dialog.id3_line_edit.text().strip()
                display_name = add_dialog.display_name_line_edit.text().strip()
                show_in_table = add_dialog.show_checkbox.isChecked()
                if not id3_key or not display_name:
                    message = (
                        "Tried to create a tag without display name or key.\n"
                        f"ID3 Key: {id3_key}\n"
                        f"Display Name: {display_name}\n"
                        f"Show in Table: {show_in_table}"
                    )
                    logger.warning(message)
                    QMessageBox.warning(self, "Missing Info", message)
                    return
                if any(
                    tag.id3_key == id3_key or tag.display_name == display_name
                    for tag in self.model._tags
                ):
                    message = (
                        "Tag with this key or display name already exists.\n"
                        f"ID3 Key: {id3_key}\n"
                        f"Display Name: {display_name}\n"
                        f"Show in Table: {show_in_table}\n"
                        "You can edit the existing display name, "
                        "or remove the tag if you want a different key with the same display name."
                    )
                    logger.warning(message)
                    QMessageBox.warning(self, "Tag Exists", message)
                    return

                self.model.addTag(id3_key, display_name, show_in_table)

        add_dialog.finished.connect(processDialogResult)
        add_dialog.show()

    def removeSelectedTags(self):
        selected_rows = self.tag_table.selectionModel().selectedRows()

        if len(selected_rows) == 0:
            return

        # Construct warning message
        delete_message = "Are you sure you want to remove the tags with the info:\n"
        for index in selected_rows:
            row = index.row()
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
            for row in sorted([index.row() for index in selected_rows], reverse=True):
                self.model.removeTag(row)

    def moveTagsUp(self) -> None:
        selected_rows = sorted(
            [index.row() for index in self.tag_table.selectionModel().selectedRows()]
        )
        if not selected_rows or selected_rows[0] == 0:
            return  # Can't move the first row up

        for row in selected_rows:
            self.model.moveTag(row, row - 1)

    def moveTagsDown(self) -> None:
        selected_rows = sorted(
            [index.row() for index in self.tag_table.selectionModel().selectedRows()],
            reverse=True,
        )
        if not selected_rows or selected_rows[0] == self.model.rowCount() - 1:
            return  # Can't move the last row down

        for row in selected_rows:
            self.model.moveTag(row, row + 1)

    def showInvalidInputMessage(self, message: str):
        QMessageBox.warning(self.tag_table, "Invalid Input", message)

    @override
    def updateSettings(self) -> None:
        """A slot that should be called from the parent widget when the dialog is accepted.
        Changes the values in the settings file to match the ones set in the dialog.
        """
        logger.info("Called update settings inside tag dialog")
        prefs.settings.info_tags = self.model._tags
        self.settings_updated.emit()

    @override
    def restoreDefaults(self) -> None:
        logger.info("Restore defaults called for tag")
        # Make a copy to avoid changing the original default settings
        self.model.setTags(prefs.settings.default_tags)

    @override
    def resetSettings(self) -> None:
        """Reset the settings to the values they had when the dialog opened."""
        # Make a copy to avoid changing the original_tags value,
        # which would prevent resetting a second time.
        self.model.setTags(self.original_tags)
