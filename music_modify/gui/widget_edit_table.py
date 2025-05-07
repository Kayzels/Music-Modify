# pyright: reportIncompatibleMethodOverride=false
import copy
import logging
from typing import override, cast
from PySide6.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget

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
        # TODO: Check, especially regarding empty string
        values: list[list[str]] = []
        for row in range(self.main_widget.rowCount()):
            pair: list[str] = []
            for col in range(self.main_widget.columnCount()):
                item = self.main_widget.item(row, col)
                if item is not None:
                    text = item.text()
                    pair.append(text)
            if not any([pair[j] == "" for j in range(len(pair))]):
                values.append(pair)
        self.value = values
        self._emitUpdate()

    @override
    def _addRow(self) -> None:
        raise NotImplementedError

    @override
    def _removeRow(self) -> None:
        raise NotImplementedError

    @override
    def _moveRows(self, direction: Direction) -> None:
        raise NotImplementedError

    @property
    @override
    def value(self) -> list[list[str]]:
        return self._value

    @value.setter
    @override
    def value(self, value: list[list[str]]):
        self._value: list[list[str]] = value
