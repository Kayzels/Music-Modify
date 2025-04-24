from PySide6.QtWidgets import QTableView

from music_modify.models import SongRepository
from music_modify.prefs import prefs

PEOPLE_TAG_WIDTH = 150


def updateTableView(table_view: QTableView, repository: SongRepository) -> None:
    """Updates the appearance of the table view.
    Sets the column widths to the max for tags with one field,
    and the column width to PEOPLE_TAG_WIDTH for tags with multiple fields."""
    if len(repository) == 0:
        return

    for index, tag in enumerate(prefs.settings.file_tags):
        if len(tag) == 1:
            table_view.resizeColumnToContents(index)
        else:
            table_view.setColumnWidth(index, PEOPLE_TAG_WIDTH)
