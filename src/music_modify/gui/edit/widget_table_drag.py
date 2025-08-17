"""Module that defines a DragTableWidget.

This widget is used by an EditTableWidget for knowing when rows are reodered.
"""

from typing import override

from PySide6.QtCore import Signal
from PySide6.QtGui import QDropEvent, QResizeEvent
from PySide6.QtWidgets import QTableWidget


class DragTableWidget(QTableWidget):
    """Table class that emits a signal when rows are reordered."""

    rows_reordered: Signal = Signal()

    @override
    def dropEvent(self, event: QDropEvent) -> None:
        super().dropEvent(event)
        self.rows_reordered.emit()

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.adjustColumnWidths()

    def adjustColumnWidths(self, length: int | None = None) -> None:
        """Adjusts the widths of the table to the specified length.

        Except for the last column, which is stretched.
        """
        if self.rowCount() <= 1 or length == 0:
            column_width = int(self.width() / self.columnCount())
            for column in range(self.columnCount() - 1):
                self.setColumnWidth(column, column_width)
        else:
            for column in range(self.columnCount() - 1):
                self.resizeColumnToContents(column)
        self.horizontalHeader().setStretchLastSection(True)
