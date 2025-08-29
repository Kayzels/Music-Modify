"""Module that defines the widget that is used to display (role, person) pairs."""

import logging
from typing import override

from PySide6.QtCore import QItemSelectionModel, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QBoxLayout,
    QFrame,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types import constants
from music_modify.custom_types.aliases import SongTableData
from music_modify.custom_types.enums import EditButton, RowDirection
from music_modify.gui.utils import getSelectedRows

from .widget_edit_abstract_group import EditAbstractGroupWidget
from .widget_table_drag import DragTableWidget

logger = logging.getLogger(__name__)


class EditTableWidget(EditAbstractGroupWidget[SongTableData, DragTableWidget]):
    """Displays data in a table, used for People data.

    This is stored in the form [role, person].
    """

    def __init__(
        self,
        parent: QWidget,
        data: SongTableData | None,
        labels: list[str] | None = None,
    ) -> None:
        """Creates an EditTableWidget.

        Args:
            parent: The widget that should own this widget
            data: The information currently present for the tag
            labels (optional): The headings that the table should have
        """
        if labels is None or len(labels) != constants.PEOPLE_COL_COUNT:
            self.labels: list[str] = ["Role", "Person"]
        else:
            self.labels = labels

        super().__init__(parent, data)

        self._original_data: SongTableData

        self.main_widget.adjustColumnWidths(len(self.value))

    @override
    def _setMainWidget(self) -> DragTableWidget:
        main_widget = DragTableWidget()
        main_widget.setMinimumHeight(250)
        main_widget.setColumnCount(2)
        main_widget.setHorizontalHeaderLabels(self.labels)
        main_widget.setRowCount(len(self.value))
        main_widget.setShowGrid(False)
        main_widget.setAlternatingRowColors(True)

        # Allow dragging rows up and down
        # NOTE: To ensure rows aren't overwritten,
        # need to ensure that ItemIsDropEnabled is unset
        # for all items. (Done in _displayValue)
        main_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        main_widget.setDragDropOverwriteMode(False)

        main_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection,
        )
        main_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows,
        )

        main_widget.itemChanged.connect(self._updateValue)
        main_widget.rows_reordered.connect(self._updateValue)
        return main_widget

    @override
    def _setupUi(self) -> None:
        layout = self.main_layout

        # Put the table in a frame so that there are borders,
        # like the other EditWidgets.
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Panel)
        frame.setLineWidth(1)
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(frame)
        layout.addLayout(frame_layout)

        frame_layout.addWidget(self.main_widget)

        self._displayValue()

        button_layout = QVBoxLayout()
        layout.addLayout(button_layout)

        # noinspection PyTypeChecker
        for button_group in (
            EditButton.Up | EditButton.Down,
            EditButton.Add | EditButton.Remove,
            EditButton.Clear | EditButton.Reset,
        ):
            child_layout = self.createButtons(
                button_group,
                QBoxLayout.Direction.LeftToRight,
            )
            button_layout.addLayout(child_layout)

    @override
    def _isReset(self) -> bool:
        if len(self.value) != len(self.original):
            return False
        for i in range(len(self.value)):
            for j in range(1):
                if self.value[i][j] != self.original[i][j]:
                    return False
        return True

    @override
    def _updateValue(self) -> None:
        values: SongTableData = []
        for row in range(self.main_widget.rowCount()):
            pair: list[str] = []
            for col in range(self.main_widget.columnCount()):
                item = self.main_widget.item(row, col)
                if item is not None:
                    text = item.text()
                    pair.append(text)
            if (
                not any(pair[j] == "" for j in range(len(pair)))
                and len(pair) == constants.PAIR_SIZE
            ):
                # Don't add while one of the values in the pair is empty
                # Also need to check for length,
                # because the second item won't exist at first
                # (so it won't be empty, it just won't be added)
                values.append(pair)
        self.value = values
        self._emitUpdate()

    @override
    def _displayValue(self) -> None:
        """Sets the values for the table based on the current value property."""
        self.main_widget.clearContents()

        # Ensure we have enough rows for the data, if a row was deleted before.
        self.main_widget.setRowCount(len(self.value))

        # In order to prevent itemChanged firing for every change,
        # block signals until the table is done being populated.
        self.main_widget.blockSignals(True)  # noqa: FBT003

        # NOTE: To ensure rows aren't overwritten,
        # need to ensure that ItemIsDropEnabled is unset
        # for all items
        for row_count, pair in enumerate(self.value):
            for col_count, value in enumerate(pair):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
                self.main_widget.setItem(row_count, col_count, item)

        # Stop blocking signals after the table is populated.
        self.main_widget.blockSignals(False)  # noqa: FBT003

        # Set to proportional if no data, otherwise fit the contents
        self.main_widget.adjustColumnWidths(len(self.value))

        # Ensure there's always one row available for editing
        if self.main_widget.rowCount() == 0:
            self._addRow()

    @override
    def _addRow(self) -> None:
        self.main_widget.insertRow(self.main_widget.rowCount())
        # Need to add items here, rather than keeping as None,
        # to ensure they have the right flags for drag and drop
        for col in range(self.main_widget.columnCount()):
            item = QTableWidgetItem("")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
            self.main_widget.setItem(self.main_widget.rowCount() - 1, col, item)

    @override
    def _removeRow(self) -> None:
        selected_rows: list[int] = sorted(
            getSelectedRows(self.main_widget),
            reverse=True,
        )

        if len(selected_rows) == 0:
            return

        for row in selected_rows:
            self.main_widget.removeRow(row)
        self._updateValue()

        if self.main_widget.rowCount() == 0:
            self._addRow()

    @override
    def _moveRows(self, direction: RowDirection) -> None:
        selected_rows: list[int] = sorted(
            getSelectedRows(self.main_widget),
            reverse=direction == RowDirection.Down,
        )

        if len(selected_rows) == 0:
            return

        direction_num = 1
        match direction:
            case RowDirection.Up:
                # Don't move up if first selected item is already at top
                if selected_rows[0] == 0:
                    return
                direction_num = -1
            case RowDirection.Down:
                # Don't move down if the last selected item is already at the bottom
                if selected_rows[0] == self.main_widget.rowCount() - 1:
                    return
                direction_num = 1

        for row in selected_rows:
            items: list[QTableWidgetItem] = []
            for col in range(self.main_widget.columnCount()):
                item = self.main_widget.takeItem(row, col)
                items.append(item)
            logger.info(f"The row number to be removed is {row}")
            logger.info(f"The values for items are: {[item.text() for item in items]}")
            self.main_widget.removeRow(row)
            self.main_widget.insertRow(row + direction_num)
            for col, item in enumerate(items):
                self.main_widget.setItem(row + direction_num, col, item)

        # Select each new row
        # Doing it this way rather than on the items,
        # because there were issues with deselection and deletion when set
        # in the above loop.
        selection_model = self.main_widget.selectionModel()
        selection_model.clearSelection()
        for row in selected_rows:
            index = self.main_widget.model().index(row + direction_num, 0)
            # noinspection PyTypeChecker
            selection_model.select(
                index,
                QItemSelectionModel.SelectionFlag.Select
                | QItemSelectionModel.SelectionFlag.Rows,
            )

        self._updateValue()

    @property
    @override
    def empty(self) -> SongTableData:
        return []
