"""Module that defines a PrefsTagDialog.

This dialog configures which tags should be editable and displayed.
"""

import copy
import logging
from typing import TYPE_CHECKING, override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QMessageBox,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from music_modify.core.enums import RowDirection
from music_modify.gui.mixins.row_operation_mixin import RowOperationMixin
from music_modify.gui.prefs.delegate_editor_type import EditorTypeDelegate
from music_modify.gui.utils import getSelectedRows
from music_modify.models import TagModel
from music_modify.models.tag_model import TAG_MODEL_COLUMNS
from music_modify.prefs import Settings

from .dialog_prefs_abstract import PrefsAbstractDialog
from .dialog_prefs_tag_add import PrefsTagAddDialog

if TYPE_CHECKING:
    from music_modify.custom_types import TagInfo

logger = logging.getLogger(__name__)


class PrefsTagDialog(PrefsAbstractDialog, RowOperationMixin):
    """Dialog for editing metadata tags.

    Allows the user to edit the metadata tags that are edited
    and displayed for songs.
    """

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        """Create a PrefsTagDialog.

        Args:
            settings: Settings object to read from and update.
            parent: The widget that this dialog should be displayed on.
        """
        super().__init__(settings, parent)
        self.setWindowTitle("Edit Tags")

        tags: list[TagInfo] = copy.deepcopy(self._settings.info_tags)
        self.original_tags: list[TagInfo] = copy.deepcopy(self._settings.info_tags)

        self.model: TagModel = TagModel(tags)
        self.tag_table.setModel(self.model)
        self.tag_table.resizeColumnsToContents()

        editor_type_col_index = TAG_MODEL_COLUMNS.index("editor_type")
        delegate = EditorTypeDelegate()
        self.tag_table.setItemDelegateForColumn(editor_type_col_index, delegate)

        self.model.invalid_input.connect(self.showInvalidInputMessage)

    @override
    def _addRow(self) -> None:
        add_dialog = PrefsTagAddDialog(self)
        add_dialog.accepted.connect(lambda: add_dialog.addToModel(self.model))
        add_dialog.show()

    @override
    def _removeRow(self) -> None:
        selected_rows = getSelectedRows(self.tag_table)

        if len(selected_rows) == 0:
            return

        # Construct warning message
        delete_message = "Are you sure you want to remove the tags with the info:\n"
        for row in selected_rows:
            for col in range(self.model.columnCount()):
                header_val = self.model.headerData(
                    col,
                    Qt.Orientation.Horizontal,
                    Qt.ItemDataRole.DisplayRole,
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

    @override
    def _moveRows(self, direction: RowDirection) -> None:
        selected_rows = sorted(
            getSelectedRows(self.tag_table), reverse=direction == RowDirection.Down
        )
        if not selected_rows:
            return
        direction_num = 1
        match direction:
            case RowDirection.Up:
                if selected_rows[0] == 0:
                    return
                direction_num = -1
            case RowDirection.Down:
                if selected_rows[0] == self.model.rowCount() - 1:
                    return
                direction_num = 1
        for row in selected_rows:
            self.model.moveTag(row, row + direction_num)

    def showInvalidInputMessage(self, message: str) -> None:
        """Displays a message about invalid input."""
        QMessageBox.warning(self.tag_table, "Invalid Input", message)

    @override
    def updateSettings(self) -> None:
        logger.info("Called update settings inside tag dialog")
        self._settings.info_tags = self.model.tags

    @override
    def restoreDefaults(self) -> None:
        logger.debug("Restore defaults called for tag")
        self.model.tags = self._settings.default_tags

    @override
    def resetSettings(self) -> None:
        logger.debug("Called reset settings in tag")
        """Reset the settings to the values they had when the dialog opened."""
        self.model.tags = self.original_tags

    @override
    def setupUi(self) -> None:
        """Creates the interface for the dialog."""
        self.resize(510, 434)

        vertical_layout = QVBoxLayout(self)

        horizontal_layout = QHBoxLayout()

        self.tag_table: QTableView = QTableView(self)
        self.tag_table.setAlternatingRowColors(True)
        self.tag_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tag_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tag_table.setShowGrid(False)
        self.tag_table.horizontalHeader().setStretchLastSection(True)
        self.tag_table.verticalHeader().setVisible(False)

        horizontal_layout.addWidget(self.tag_table)

        button_layout = QVBoxLayout()
        new_buttons = self.createOperationButtons(self)
        for new_button in new_buttons:
            button_layout.addWidget(new_button)
        horizontal_layout.addLayout(button_layout)

        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.setStretch(0, 10)
