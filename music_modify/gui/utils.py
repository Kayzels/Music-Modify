from typing import cast

from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtWidgets import QAbstractItemView, QLayout, QTableView, QWidget

from music_modify.models import SongRepository
from music_modify.prefs import prefs

PEOPLE_TAG_WIDTH = 150


def updateTableView(table_view: QTableView, repository: SongRepository) -> None:
    """Updates the appearance of the table view.
    Sets the column widths to the max for tags with one field,
    and the column width to PEOPLE_TAG_WIDTH for tags with multiple fields."""
    if len(repository) == 0:
        return

    for index, tag in enumerate(prefs.settings.table_tags):
        if len(tag) == 1:
            table_view.resizeColumnToContents(index)
        else:
            table_view.setColumnWidth(index, PEOPLE_TAG_WIDTH)


def clearLayout(layout: QLayout) -> None:
    """Removes all widgets from the given layout"""
    while layout.count() > 0:
        item = layout.takeAt(0)
        if cast(QLayout | None, item.layout()) is not None:
            clearLayout(item.layout())
        widget = item.widget()
        if cast(QWidget | None, widget) is not None:
            widget.deleteLater()
        del item


def getSelectedRows(view: QAbstractItemView) -> list[int]:
    """Get the row numbers for the selected rows in the provided view."""
    selection_model = view.selectionModel()
    model = view.model()

    selected_rows = selection_model.selectedRows()

    if len(selected_rows) == 0:
        return []

    # If the view is sorted or filtered, we need to map to the source.
    if isinstance(model, QSortFilterProxyModel):
        selected_rows = [model.mapToSource(row) for row in selected_rows]

    # Need to remove duplicates
    # Likely shouldn't be needed, but it's possible a row appears multiple times.
    rows = list(set([index.row() for index in selected_rows if index.isValid()]))

    return rows
