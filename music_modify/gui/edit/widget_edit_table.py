import copy
import logging
from typing import cast, override

from PySide6.QtCore import QItemSelectionModel, Qt, Signal
from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types.aliases import SongTableData
from music_modify.custom_types.enums import Direction, EditButton

from .widget_edit_abstract_group import EditAbstractGroupWidget

logger = logging.getLogger(__name__)


class _DragTableWidget(QTableWidget):
    """Private table class that emits a signal when rows are reordered."""

    rowsReordered: Signal = Signal()

    @override
    def dropEvent(self, event: QDropEvent) -> None:
        super().dropEvent(event)
        self.rowsReordered.emit()


class EditTableWidget(EditAbstractGroupWidget):
    """Displays data in a table, used for People data, which is stored in the form [role, person]."""

    def __init__(self, parent: QWidget, data: SongTableData | None):
        super().__init__(parent, data)

        self.main_widget: _DragTableWidget
        self._original_data: SongTableData

    @override
    def _initValue(self, data: SongTableData | None):
        if data is None:
            self.value = []
        else:
            self.value = data

        self._original_data = copy.deepcopy(self.value)

    @override
    def _setupUi(self):
        layout = self.layout()
        if layout is None:
            logger.info("Layout was None for table widget")
            return
        layout = cast(QHBoxLayout, layout)

        # Put the table in a frame so that there are borders,
        # like the other EditWidgets.
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Panel)
        frame.setLineWidth(1)
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(frame)
        layout.addLayout(frame_layout)

        self.main_widget = _DragTableWidget()
        self.main_widget.setMinimumHeight(250)
        self.main_widget.setColumnCount(2)
        self.main_widget.setHorizontalHeaderLabels(["Role", "Person"])
        self.main_widget.setRowCount(len(self.value))
        self.main_widget.setShowGrid(False)
        self.main_widget.setAlternatingRowColors(True)

        frame_layout.addWidget(self.main_widget)

        # Allow dragging rows up and down
        # NOTE: To ensure rows aren't overwritten, need to ensure that ItemIsDropEnabled is unset
        # for all items. (Done in _displayValue)
        self.main_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.main_widget.setDragDropOverwriteMode(False)

        self._displayValue()

        self.main_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.main_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.main_widget.itemChanged.connect(self._updateValue)
        self.main_widget.rowsReordered.connect(self._updateValue)

        button_layout = QVBoxLayout()
        layout.addLayout(button_layout)

        for button_group in (
            EditButton.Up | EditButton.Down,
            EditButton.Add | EditButton.Remove,
            EditButton.Clear | EditButton.Reset,
        ):
            child_layout = self._createButtons(button_group, QHBoxLayout)
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
            if not any([pair[j] == "" for j in range(len(pair))]) and len(pair) == 2:
                # Don't add while one of the values in the pair is empty
                # Also need to check for length, because the second item won't exist at first
                # (so it won't be empty, it just won't be added)
                values.append(pair)
        self.value = values
        self._emitUpdate()

    @override
    def _displayValue(self) -> None:
        """Sets the values for the table based on the current value property."""
        if not hasattr(self, "main_widget"):
            return

        self.main_widget.clearContents()

        # In order to prevent itemChanged firing for every change,
        # block signals until the table is done being populated.
        self.main_widget.blockSignals(True)

        # NOTE: To ensure rows aren't overwritten, need to ensure that ItemIsDropEnabled is unset
        # for all items
        for row_count, pair in enumerate(self.value):
            for col_count, value in enumerate(pair):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
                self.main_widget.setItem(row_count, col_count, item)

        # Stop blocking signals after the table is populated.
        self.main_widget.blockSignals(False)

        # Fit the content to the columns, except for the last, which should stretch.
        for column in range(self.main_widget.columnCount() - 1):
            self.main_widget.resizeColumnToContents(column)
        self.main_widget.horizontalHeader().setStretchLastSection(True)

    @override
    def _clearValue(self) -> None:
        self.value = []

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
        selected_indexes = self.main_widget.selectedIndexes()
        if len(selected_indexes) == 0:
            return

        # Need to ensure it's unique, but also ordered.
        # Because a row will appear twice (once for each cell),
        # but we only want to remove the row once.
        selected_rows = sorted(
            list(set([index.row() for index in selected_indexes])), reverse=True
        )
        for row in selected_rows:
            self.main_widget.removeRow(row)
        self._updateValue()

    @override
    def _moveRows(self, direction: Direction) -> None:
        selected_indexes = self.main_widget.selectedIndexes()
        if len(selected_indexes) == 0:
            return

        # Need to ensure it's unique, but also ordered.
        # Because a row will appear twice (once for each cell),
        # but we only want to remove the row once.
        selected_rows = sorted(
            list(set([index.row() for index in selected_indexes])),
            reverse=direction == Direction.Down,
        )

        match direction:
            case Direction.Up:
                # Don't move up if first selected item is already a ttop
                if selected_rows[0] == 0:
                    return
                direction_num = -1
            case Direction.Down:
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
            selection_model.select(
                index,
                QItemSelectionModel.SelectionFlag.Select
                | QItemSelectionModel.SelectionFlag.Rows,
            )

        self._updateValue()

    @property
    @override
    def value(self) -> SongTableData:
        return self._value

    @value.setter
    @override
    def value(self, value: SongTableData):
        self._value: SongTableData = value

    @property
    @override
    def original(self) -> SongTableData:
        return self._original_data
