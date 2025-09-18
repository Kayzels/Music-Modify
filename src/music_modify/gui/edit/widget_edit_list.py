"""Module that defines an EditListWidget.

This widget is used when lists of single values are contained for a tag.
"""

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

from music_modify.core.enums import EditButton, RowDirection
from music_modify.custom_types.tag_value import (
    AbstractTagValue,
    TextTagValue,
)
from music_modify.gui.utils import getSelectedRows

from .widget_edit_abstract_group import EditAbstractGroupWidget

logger = logging.getLogger(__name__)


class EditListWidget(EditAbstractGroupWidget):
    """Displays data in a list widget, with each row being a string."""

    def __init__(
        self,
        initial_value: AbstractTagValue | None = None,
        parent: QWidget | None = None,
    ) -> None:
        """Create an EditListWidget.

        Args:
            initial_value: Original value that should be displayed.
            parent: Widget this widget should be displayed on.
        """
        if initial_value is not None and not isinstance(initial_value, TextTagValue):
            logger.warning(
                "Got an invalid initial_value for an EditListWidget. "
                + f"Expected None or a TextTagValue. Got {type(initial_value)}. "
                + "Setting to None."
            )
            initial_value = None
        if initial_value is not None and not initial_value.value:
            initial_value = None
        super().__init__(initial_value, parent)

        self.main_widget: QListWidget
        "Main widget used to display the values currently being stored."

        self._cached_value: TextTagValue | None = initial_value

    def _setMainWidget(self) -> QListWidget:
        main_widget = QListWidget()
        main_widget.setMinimumHeight(200)
        main_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        main_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection,
        )
        main_widget.setAlternatingRowColors(True)
        return main_widget

    @override
    def _setupUi(self) -> None:
        layout = self.main_layout
        self.main_widget = self._setMainWidget()
        layout.addWidget(self.main_widget)

        self.value = self.original

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

    @property
    @override
    def value(self) -> AbstractTagValue | None:
        texts: list[str] = [
            text
            for row in range(self.main_widget.count())
            if (text := self.main_widget.item(row).text().strip()) != ""
        ]
        if not texts:
            return None
        if self._cached_value is None or texts != self._cached_value.value:
            self._cached_value = TextTagValue(texts)
        return self._cached_value

    @value.setter
    @override
    def value(self, value: AbstractTagValue | None) -> None:
        # Remove all current items and rebuild the list.
        self.main_widget.clear()
        if isinstance(value, TextTagValue):
            for val in value.value:
                item = QListWidgetItem(val)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.main_widget.addItem(item)
        elif value is not None:
            logger.warning(
                f"EditListWidget received unexpected value type: {type(value)}. "
                + "Expected TextTagValue or None. "
                + "Clearing the stored value."
            )

        # Ensure there's always one row available for editing
        if self.main_widget.model().rowCount() == 0:
            self._addRow()

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
