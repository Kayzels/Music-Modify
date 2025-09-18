"""Module that governs how the metadata related to songs should be managed.

Defines a `SongTableModel`.
"""

import logging
from typing import Final, override

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    Slot,
)

from music_modify.core import constants
from music_modify.custom_types import TagInfo

from .song_repository import SongRepository

logger = logging.getLogger(__name__)


class SongTableModel(QAbstractTableModel):
    """Model that stores the extracted metadata from the song files.

    Attributes:
        empty_message: The message to display when there are no songs.
        repository: The repository that stores the actual songs.
    """

    empty_message: Final[str] = "Files will show here when added. Drag files here."

    def __init__(self, repository: SongRepository, table_tags: list[TagInfo]) -> None:
        """Create a new model for the songs that should be managed.

        Args:
            repository: The list of songs that can be edited.
            table_tags: The tags that should be used to populate the columns.
        """
        super().__init__()
        self.repository: SongRepository = repository
        self.repository.songs_updated.connect(self.layoutChanged.emit)
        self._table_tags: list[TagInfo] = table_tags

    @Slot()
    def updateTableTags(self, table_tags: list[TagInfo]) -> None:
        """Update the tags that should be used for the columns."""
        self._table_tags = table_tags

    @override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: Qt.ItemDataRole | int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            song = self.repository[index.row()]
            id3_key = self._table_tags[index.column()].id3_key
            tag_value = song.getTag(id3_key)
            if tag_value:
                return tag_value.getDisplayValue()
            return ""
        return None

    @override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = constants.Q_MODEL_INDEX,
    ) -> int:
        return len(self.repository)

    @override
    def columnCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = constants.Q_MODEL_INDEX,
    ) -> int:
        if self.rowCount(parent) == 0:
            # Uses 1 to keep a column for info
            return 1
        return len(self._table_tags)

    @override
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: Qt.ItemDataRole | int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            if len(self.repository) == 0:
                if orientation == Qt.Orientation.Horizontal:
                    return SongTableModel.empty_message
                if orientation == Qt.Orientation.Vertical:
                    return None
            if orientation == Qt.Orientation.Horizontal and section < len(
                self._table_tags
            ):
                return self._table_tags[section].display_name
            if orientation == Qt.Orientation.Vertical and section < len(
                self.repository,
            ):
                return f"{section + 1}"
            return None
        return None

    def refreshData(self, rows: list[int] | None = None) -> None:
        """Call dataChanged on all rows sent.

        If not sent in any rows, calls it on every item.
        """
        if self.rowCount() == 0 or self.columnCount() == 0:
            return

        def updateRow(first: QModelIndex, last: QModelIndex) -> None:
            self.dataChanged.emit(first, last, [])

        if rows is None:
            first_index = self.index(0, 0)
            last_index = self.index(self.rowCount() - 1, self.columnCount() - 1)
            updateRow(first_index, last_index)
            return
        for row in rows:
            first_index = self.index(row, 0)
            last_index = self.index(row, self.columnCount() - 1)
            if not first_index.isValid() or not last_index.isValid():
                logger.error(f"Invalid QModelIndex for row {row}")
                continue
            updateRow(first_index, last_index)


# TODO: setData and flags
