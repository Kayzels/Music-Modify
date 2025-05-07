# pyright: reportPrivateImportUsage=false
import copy
import logging
from typing import cast

from mutagen.id3 import ID3TimeStamp

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
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

from music_modify.custom_types.enums import WidgetType

logger = logging.getLogger(__name__)


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
        up_button.clicked.connect(self._moveRowsUp)

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
        down_button.clicked.connect(self._moveRowsDown)

        if widget_type == WidgetType.List:
            self.current_data = cast(list[str], self.current_data)
            self.main_widget = QListWidget()
            for val in self.current_data:
                item = QListWidgetItem(val)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.main_widget.addItem(item)
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
                    if self._isReset():
                        self.value_reset.emit()
                        return
                    self.line_updated.emit(self.current_data)
                    return
            case WidgetType.List:
                self.main_widget = cast(QListWidget, self.main_widget)
                item = cast(QListWidgetItem, item)
                self.current_data = cast(list[str], self.current_data)
                row = self.main_widget.row(item)
                new_text = item.text()
                if new_text != self.current_data[row]:
                    self.current_data[row] = new_text
                    if self._isReset():
                        self.value_reset.emit()
                        return
                    self.group_updated.emit(self.current_data)
                    return
            case WidgetType.Table:
                self.main_widget = cast(QTableWidget, self.main_widget)
                item = cast(QTableWidgetItem, item)
                self.current_data = cast(list[list[str]], self.current_data)
                row = self.main_widget.row(item)
                col = self.main_widget.column(item)
                new_text = item.text()
                if new_text != self.current_data[row][col]:
                    self.current_data[row][col] = new_text
                    if self._isReset():
                        self.value_reset.emit()
                        return
                    self.group_updated.emit(self.current_data)
                    return

        logger.info("Value not changed")

    def _addRow(self) -> None:
        raise NotImplementedError

    def _removeRow(self) -> None:
        raise NotImplementedError

    def _moveRowsUp(self) -> None:
        raise NotImplementedError

    def _moveRowsDown(self) -> None:
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
                if len(self.current_data) != len(self.original_data):
                    return False
                for i in range(len(self.current_data)):
                    if self.current_data[i] != self.original_data[i]:
                        return False
                return True
            case WidgetType.Table:
                self.current_data = cast(list[list[str]], self.current_data)
                self.original_data = cast(list[list[str]], self.original_data)
                if len(self.current_data) != len(self.original_data):
                    return False
                for i in range(len(self.current_data)):
                    for j in range(1):
                        if self.current_data[i][j] != self.original_data[i][j]:
                            return False
                return True
