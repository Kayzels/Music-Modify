# pyright: reportPrivateImportUsage=false
import copy
import logging
from typing import cast

from mutagen.id3 import ID3TimeStamp

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types.enums import Direction, WidgetType

logger = logging.getLogger(__name__)

# TODO: Implement redo/undo


class EditWidget(QWidget):
    line_updated: Signal = Signal(str)
    group_updated: Signal = Signal(list)
    value_reset: Signal = Signal()

    def __init__(
        self,
        parent: QWidget | None,
        widget_type: WidgetType,
        data: list[str] | list[ID3TimeStamp] | list[list[str]] | None,
    ):
        super().__init__(parent)

        self.current_data: str | list[str] | list[list[str]]

        if data is None or len(data) == 0:
            if widget_type in (WidgetType.List, WidgetType.Table):
                self.current_data = []
            else:
                self.current_data = ""
        elif isinstance(data[0], ID3TimeStamp) or widget_type == WidgetType.String:
            self.current_data = str(data[0])
        else:
            data = cast(list[str] | list[list[str]], data)
            self.current_data = data

        self.original_data: str | list[str] | list[list[str]] = copy.deepcopy(
            self.current_data
        )

        self.widget_type: WidgetType = widget_type

        self.setupUi(widget_type)
        self.main_widget: QLineEdit | QListWidget | QTableWidget

    def setupUi(
        self,
        widget_type: WidgetType,
    ):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        if widget_type == WidgetType.String:
            self.main_widget = QLineEdit()
            self.current_data = cast(str, self.current_data)
            self.main_widget.setText(self.current_data)
            layout.addWidget(self.main_widget)
            self.main_widget.editingFinished.connect(self._changeValue)
            return

        button_layout = QVBoxLayout()

        up_button = QToolButton(self)
        up_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp)))
        button_layout.addWidget(up_button)
        up_button.clicked.connect(lambda: self._moveRows(Direction.Up))

        add_button = QToolButton(self)
        add_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd)))
        button_layout.addWidget(add_button)
        add_button.clicked.connect(self._addRow)

        remove_button = QToolButton(self)
        remove_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove)))
        button_layout.addWidget(remove_button)
        remove_button.clicked.connect(self._removeRow)

        down_button = QToolButton(self)
        down_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown)))
        button_layout.addWidget(down_button)
        down_button.clicked.connect(lambda: self._moveRows(Direction.Down))

        if widget_type == WidgetType.List:
            self.current_data = cast(list[str], self.current_data)
            self.main_widget = QListWidget()
            for val in self.current_data:
                item = QListWidgetItem(val)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.main_widget.addItem(item)
            self.main_widget.setDragDropMode(
                QAbstractItemView.DragDropMode.InternalMove
            )
            self.main_widget.model().rowsMoved.connect(lambda: self._changeValue(None))
            self.main_widget.setSelectionMode(
                QAbstractItemView.SelectionMode.ExtendedSelection
            )
        elif widget_type == WidgetType.Table:
            self.current_data = cast(list[list[str]], self.current_data)
            self.main_widget = QTableWidget()
            self.main_widget.setColumnCount(2)
            self.main_widget.setHorizontalHeaderLabels(["Role", "Person"])  # pyright: ignore[reportUnknownMemberType]
            self.main_widget.setRowCount(len(self.current_data))

            for row_count, pair in enumerate(self.current_data):
                for col_count, value in enumerate(pair):
                    self.main_widget.setItem(
                        row_count, col_count, QTableWidgetItem(value)
                    )
            self.main_widget.resizeColumnsToContents()
            self.main_widget.horizontalHeader().setStretchLastSection(True)

        self.main_widget.itemChanged.connect(self._changeValue)

        layout.addWidget(self.main_widget)
        layout.addLayout(button_layout)

    @Slot()
    @Slot(QListWidgetItem)
    @Slot(QTableWidgetItem)
    def _changeValue(
        self, item: QListWidgetItem | QTableWidgetItem | None = None
    ) -> None:
        logger.info("Called change value")
        match self.widget_type:
            case WidgetType.String:
                self.main_widget = cast(QLineEdit, self.main_widget)
                new_text = self.main_widget.text()
                if new_text != self.current_data:
                    self.current_data = new_text
                    self._emitUpdate()
                    return
            case WidgetType.List:
                self.main_widget = cast(QListWidget, self.main_widget)
                item = cast(QListWidgetItem, item)
                self.current_data = cast(list[str], self.current_data)

                # Need to create the list from scratch,
                # as not sure what changes have been made:
                # could be a single line, or lines moved or deleted.
                self.current_data = [
                    self.main_widget.item(row).text().strip()
                    for row in range(self.main_widget.count())
                    if self.main_widget.item(row).text().strip() != ""
                ]
                self._emitUpdate()
                return

            case WidgetType.Table:
                # TODO: Deal with empty string
                self.main_widget = cast(QTableWidget, self.main_widget)
                item = cast(QTableWidgetItem, item)
                self.current_data = cast(list[list[str]], self.current_data)
                row = self.main_widget.row(item)
                col = self.main_widget.column(item)
                new_text = item.text()
                if new_text != self.current_data[row][col]:
                    self.current_data[row][col] = new_text
                    self._emitUpdate()
                    return

        logger.info("Value not changed")

    def _addRow(self) -> None:
        match self.widget_type:
            case WidgetType.String:
                return
            case WidgetType.List:
                self.main_widget = cast(QListWidget, self.main_widget)
                self.current_data = cast(list[str], self.current_data)
                item = QListWidgetItem("")
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.main_widget.addItem(item)
            case WidgetType.Table:
                self.main_widget = cast(QTableWidget, self.main_widget)
                raise NotImplementedError

    def _removeRow(self) -> None:
        match self.widget_type:
            case WidgetType.String:
                return
            case WidgetType.List:
                self.main_widget = cast(QListWidget, self.main_widget)
                self.current_data = cast(list[str], self.current_data)
                row = self.main_widget.currentRow()
                _ = self.main_widget.takeItem(row)
                _ = self.current_data.pop(row)
                self._emitUpdate()
            case WidgetType.Table:
                self.main_widget = cast(QTableWidget, self.main_widget)
                raise NotImplementedError

    def _moveRows(self, direction: Direction):
        match self.widget_type:
            case WidgetType.String:
                return
            case WidgetType.List:
                self.main_widget = cast(QListWidget, self.main_widget)
                self.current_data = cast(list[str], self.current_data)

                selected_indexes = self.main_widget.selectedIndexes()

                # No items selected, nothing to move
                if len(selected_indexes) == 0:
                    return

                selected_rows = sorted(
                    [index.row() for index in selected_indexes],
                    reverse=direction == Direction.Down,
                )

                match direction:
                    case Direction.Up:
                        # Don't move up if first selected item is already at top
                        if selected_rows[0] == 0:
                            return
                        direction_num = -1
                    case Direction.Down:
                        # Don't move down if the last selected item is already at the bottom
                        if selected_rows[0] == self.main_widget.count() - 1:
                            return
                        direction_num = 1

                for index in selected_rows:
                    item = self.main_widget.takeItem(index)
                    self.main_widget.insertItem(index + direction_num, item)
                    item.setSelected(True)

                self._changeValue()

            case WidgetType.Table:
                raise NotImplementedError

    def _isReset(self) -> bool:
        """Returns whether the value that is being stored is the same as the original value."""
        match self.widget_type:
            case WidgetType.String:
                self.current_data = cast(str, self.current_data)
                self.original_data = cast(str, self.original_data)
                return self.current_data == self.original_data
            case WidgetType.List:
                self.current_data = cast(list[str], self.current_data)
                self.original_data = cast(list[str], self.original_data)

                # If the other methods worked correctly, there should be no empty strings in current_data
                if any([val.strip() == "" for val in self.current_data]):
                    logger.warning("There were empty strings inside current_data")
                    self.current_data = [
                        val.strip() for val in self.current_data if val.strip() != ""
                    ]

                if len(self.current_data) != len(self.original_data):
                    return False
                for i in range(len(self.current_data)):
                    if self.current_data[i] != self.original_data[i]:
                        return False
                return True
            case WidgetType.Table:
                # TODO: Deal with empty string
                self.current_data = cast(list[list[str]], self.current_data)
                self.original_data = cast(list[list[str]], self.original_data)
                if len(self.current_data) != len(self.original_data):
                    return False
                for i in range(len(self.current_data)):
                    for j in range(1):
                        if self.current_data[i][j] != self.original_data[i][j]:
                            return False
                return True

    def _emitUpdate(self):
        """Emits either line_updated, group_updated, or value_reset, depending on change."""
        if self._isReset():
            self.value_reset.emit()
            return
        match self.widget_type:
            case WidgetType.String:
                self.line_updated.emit(self.current_data)
            case WidgetType.List | WidgetType.Table:
                self.group_updated.emit(self.current_data)
