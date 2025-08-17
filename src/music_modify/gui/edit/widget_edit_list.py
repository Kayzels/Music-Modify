"""Module that defines an EditListWidget.

This widget is used when lists of single values are contained for a tag.
"""

import copy
import logging
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QBoxLayout,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types.aliases import SongListData
from music_modify.custom_types.enums import EditButton, RowDirection
from music_modify.gui.utils import getSelectedRows

from .widget_edit_abstract_group import EditAbstractGroupWidget

logger = logging.getLogger(__name__)


class EditListWidget(EditAbstractGroupWidget[SongListData, QListWidget]):
    """Displays data in a list widget, with each row being a string."""

    def __init__(self, parent: QWidget, data: SongListData | None) -> None:
        """Create an EditListWidget.

        Args:
            parent: The widget that this widget should be displayed on.
            data: The data to be displayed on this widget.
        """
        super().__init__(parent, data)

        self._original_data: SongListData

    @override
    def _initValue(self, data: SongListData | None) -> None:
        if data is None:
            self.value = []
        else:
            self.value = data.copy()

        self._original_data = copy.deepcopy(self.value)

    @override
    def _setMainWidget(self) -> QListWidget:
        main_widget = QListWidget()
        main_widget.setMinimumHeight(200)
        main_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        main_widget.model().rowsMoved.connect(self._updateValue)
        main_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection,
        )
        main_widget.itemChanged.connect(self._updateValue)
        main_widget.setAlternatingRowColors(True)
        return main_widget

    @override
    def _setupUi(self) -> None:
        layout = self.main_layout
        layout.addWidget(self.main_widget)

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
        return all(self.value[i] == self.original[i] for i in range(len(self.value)))

    @override
    def _updateValue(self) -> None:
        self.value = [
            self.main_widget.item(row).text().strip()
            for row in range(self.main_widget.count())
            if self.main_widget.item(row).text().strip() != ""
        ]
        self._emitUpdate()

    @override
    def _displayValue(self) -> None:
        # Remove all current items and rebuild the list.
        self.main_widget.clear()
        for val in self.value:
            item = QListWidgetItem(val)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.main_widget.addItem(item)

        # Ensure there's always one row available for editing
        if self.main_widget.model().rowCount() == 0:
            self._addRow()

    @override
    def _clearValue(self) -> None:
        self.value = []

    @override
    def _addRow(self) -> None:
        item = QListWidgetItem("")
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.main_widget.addItem(item)

    @override
    def _removeRow(self) -> None:
        selected_rows: list[int] = sorted(
            getSelectedRows(self.main_widget),
            reverse=True,
        )
        if len(selected_rows) == 0:
            return

        for row in selected_rows:
            _ = self.main_widget.takeItem(row)
        self._updateValue()
        if self.main_widget.model().rowCount() == 0:
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
