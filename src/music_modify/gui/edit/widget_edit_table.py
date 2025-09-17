"""Module that defines the widget that is used to display (role, person) pairs."""

import logging
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QBoxLayout,
    QFrame,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types import constants
from music_modify.custom_types.enums import EditButton, RowDirection
from music_modify.custom_types.tag_value import (
    AbstractTagValue,
    PairedTextTagValue,
    TagValueFactory,
)
from music_modify.gui.utils import getSelectedRows, selectRows

from .widget_edit_abstract_group import EditAbstractGroupWidget
from .widget_table_drag import DragTableWidget

logger = logging.getLogger(__name__)


class EditTableWidget(EditAbstractGroupWidget):
    """Displays data in a table, used for People data.

    This is stored in the form [role, person].
    """

    def __init__(
        self,
        initial_value: AbstractTagValue | None = None,
        parent: QWidget | None = None,
    ) -> None:
        """Creates an EditTableWidget.

        Args:
            initial_value: Original value that should be displayed.
            parent: Widget that should own this widget.
        """
        if initial_value is not None and not isinstance(
            initial_value, PairedTextTagValue
        ):
            logger.warning(
                "Got an invalid initial value for an EditTableWidget. "
                + f"Expected None or a PairedTextTagValue. Got {type(initial_value)}. "
                + "Setting to None."
            )
            initial_value = None
        if initial_value is not None and not initial_value.value:
            initial_value = None
        super().__init__(initial_value, parent)

        self.main_widget: DragTableWidget
        "Main widget used to display the values currently stored."

        self._cached_value: PairedTextTagValue | None = initial_value

    def _setMainWidget(self) -> DragTableWidget:
        main_widget = DragTableWidget()
        main_widget.setMinimumHeight(250)
        main_widget.setColumnCount(2)
        main_widget.setHorizontalHeaderLabels(["Role", "Person"])
        main_widget.setShowGrid(False)
        main_widget.setAlternatingRowColors(True)

        # Allow dragging rows up and down
        main_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        main_widget.setDragDropOverwriteMode(False)

        main_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection,
        )
        main_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows,
        )

        return main_widget

    def setHorizontalHeaderLabels(self, labels: list[str]) -> None:
        """Set the labels displayed on the table widget."""
        self.main_widget.setHorizontalHeaderLabels(labels)

    @override
    def _setupUi(self) -> None:
        self.main_widget = self._setMainWidget()
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
        values: list[list[str]] = []
        for row in range(self.main_widget.rowCount()):
            pair: list[str] = []
            for col in range(self.main_widget.columnCount()):
                item = self.main_widget.item(row, col)
                if item is not None:
                    pair.append(item.text())
            if (
                not any(pair[j] == "" for j in range(len(pair)))
                and len(pair) == constants.PAIR_SIZE
            ):
                # Don't add while one of the values in the pair is empty
                # Also need to check for length,
                # because the second item won't exist at first
                # (so it won't be empty, it just won't be added)
                values.append(pair)
        if not values:
            return None

        if self._cached_value is None or values != self._cached_value.value:
            new_value: AbstractTagValue | None = TagValueFactory.createTagValue(values)
            if isinstance(new_value, PairedTextTagValue):
                self._cached_value = new_value
            else:
                logger.warning(
                    "Creating a new value in EditTableWidget didn't produce a PairedTextTagValue. "
                    + f" Got {type(new_value)}."
                )
                self._cached_value = None
        return self._cached_value

    @value.setter
    @override
    def value(self, value: AbstractTagValue | None) -> None:
        self.main_widget.clearContents()

        if value is not None and not isinstance(value, PairedTextTagValue):
            logger.warning(
                f"EditTableWidget received unexpected value type: {type(value)}. "
                + "Expected PairedTextTagValue or None. "
                + "Clearing the stored value."
            )
            value = None
        if value is None:
            self.main_widget.setRowCount(0)
            self._addRow()
            return

        pairs = [pair for pair in value.value if len(pair) == constants.PAIR_SIZE]

        # Ensure we have enough rows for the data, if a row was deleted before.
        self.main_widget.setRowCount(len(pairs))

        # In order to prevent itemChanged firing for every change,
        # block signals until the table is done being populated.
        self.main_widget.blockSignals(True)  # noqa: FBT003

        # NOTE: To ensure rows aren't overwritten,
        # need to ensure that ItemIsDropEnabled is unset
        # for all items
        for row_count, pair in enumerate(pairs):
            for col_count, val in enumerate(pair):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
                self.main_widget.setItem(row_count, col_count, item)

        # Stop blocking signals after the table is populated.
        self.main_widget.blockSignals(False)  # noqa: FBT003

        # Set to proportional if no data, otherwise fit the contents
        self.main_widget.adjustColumnWidths(proportional=not bool(pairs))

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

        selectRows(self.main_widget, [row + direction_num for row in selected_rows])
