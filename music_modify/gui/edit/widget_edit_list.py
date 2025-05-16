import copy
import logging
from typing import cast, override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types.aliases import SongListData
from music_modify.custom_types.enums import Direction, EditButton
from music_modify.gui.utils import getSelectedRows

from .widget_edit_abstract_group import EditAbstractGroupWidget

logger = logging.getLogger(__name__)


class EditListWidget(EditAbstractGroupWidget):
    """Displays data in a list widget, with each row being a string."""

    def __init__(self, parent: QWidget, data: SongListData | None):
        super().__init__(parent, data)

        self.main_widget: QListWidget
        self._original_data: SongListData

    @override
    def _initValue(self, data: SongListData | None):
        if data is None:
            self.value = []
        else:
            self.value = data.copy()

        self._original_data = copy.deepcopy(self.value)

    @override
    def _setupUi(self):
        layout = self.layout()
        if layout is None:
            logger.info("Didn't create a layout for list widget")
            return
        layout = cast(QHBoxLayout, layout)

        self.main_widget = QListWidget()
        self.main_widget.setMinimumHeight(200)
        self._displayValue()
        self.main_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.main_widget.model().rowsMoved.connect(self._updateValue)
        self.main_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.main_widget.itemChanged.connect(self._updateValue)
        self.main_widget.setAlternatingRowColors(True)

        layout.addWidget(self.main_widget)

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
            if self.value[i] != self.original[i]:
                return False
        return True

    @override
    def _updateValue(self):
        self.value = [
            self.main_widget.item(row).text().strip()
            for row in range(self.main_widget.count())
            if self.main_widget.item(row).text().strip() != ""
        ]
        self._emitUpdate()

    @override
    def _displayValue(self) -> None:
        """Set the values for the widget, based on the value property currently set."""
        if not hasattr(self, "main_widget"):
            return

        # Remove all current items and rebuild the list.
        self.main_widget.clear()
        for val in self.value:
            item = QListWidgetItem(val)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.main_widget.addItem(item)

    @override
    def _clearValue(self) -> None:
        self.value = []

    @override
    def _addRow(self):
        item = QListWidgetItem("")
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.main_widget.addItem(item)

    @override
    def _removeRow(self):
        selected_rows = sorted(getSelectedRows(self.main_widget), reverse=True)
        if len(selected_rows) == 0:
            return

        for row in selected_rows:
            _ = self.main_widget.takeItem(row)
        self._updateValue()

    @override
    def _moveRows(self, direction: Direction) -> None:
        selected_rows = sorted(
            getSelectedRows(self.main_widget), reverse=direction == Direction.Down
        )
        if len(selected_rows) == 0:
            return

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

        self._updateValue()

    @property
    @override
    def value(self) -> SongListData:
        return self._value

    @value.setter
    @override
    def value(self, value: SongListData) -> None:
        self._value: SongListData = value

    @property
    @override
    def original(self) -> SongListData:
        return self._original_data
