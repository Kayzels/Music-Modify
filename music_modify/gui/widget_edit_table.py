# pyright: reportIncompatibleMethodOverride=false
import copy
import logging
from typing import override, cast
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from music_modify.custom_types.enums import Direction

from .widget_edit_abstract import EditAbstractWidget

logger = logging.getLogger(__name__)


class EditTableWidget(EditAbstractWidget):
    def __init__(self, parent: QWidget, data: list[list[str]] | None):
        super().__init__(parent, data)

        self.main_widget: QTableWidget
        self._original_data: list[list[str]]

    @override
    def _initValue(self, data: list[list[str]] | None):
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
        self.main_widget = QTableWidget()
        self.main_widget.setColumnCount(2)
        self.main_widget.setHorizontalHeaderLabels(["Role", "Person"])  # pyright: ignore[reportUnknownMemberType]
        self.main_widget.setRowCount(len(self.value))

        for row_count, pair in enumerate(self.value):
            for col_count, value in enumerate(pair):
                self.main_widget.setItem(row_count, col_count, QTableWidgetItem(value))
        self.main_widget.resizeColumnsToContents()
        self.main_widget.horizontalHeader().setStretchLastSection(True)

        self.main_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.main_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # TODO:Drag and drop rows, don't replace existing but move instead
        # It works if dropped between the lines, but dropping on top of an existing row
        # shouldn't remove it.

        # self.main_widget.setDragDropOverwriteMode(False)
        # self.main_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

        self.main_widget.itemChanged.connect(self._updateValue)
        layout.addWidget(self.main_widget)

        button_layout = self._createButtons()
        layout.addLayout(button_layout)

    @override
    def _isReset(self) -> bool:
        if len(self.value) != len(self._original_data):
            return False
        for i in range(len(self.value)):
            for j in range(1):
                if self.value[i][j] != self._original_data[i][j]:
                    return False
        return True

    @override
    def _updateValue(self) -> None:
        values: list[list[str]] = []
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
    def _addRow(self) -> None:
        self.main_widget.insertRow(self.main_widget.rowCount())

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
    def value(self) -> list[list[str]]:
        return self._value

    @value.setter
    @override
    def value(self, value: list[list[str]]):
        self._value: list[list[str]] = value
