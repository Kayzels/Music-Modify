"""Module that governs how the metadata related to songs should be managed.

Defines a `SongTableModel`.
"""

from typing import Final, cast, override

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)

from music_modify.custom_types import constants
from music_modify.custom_types.song import Song
from music_modify.prefs import prefs

from .song_repository import SongRepository


class SongTableModel(QAbstractTableModel):
    """Model that stores the extracted metadata from the song files.

    Attributes:
        empty_message: The message to display when there are no songs.
        repository: The repository that stores the actual songs.
    """

    empty_message: Final[str] = "Files will show here when added. Drag files here."

    def __init__(self, repository: SongRepository) -> None:
        """Create a new model for the songs that should be managed.

        Args:
            repository: The list of songs that can be edited.
        """
        super().__init__()
        self.repository: SongRepository = repository
        self.repository.songs_updated.connect(self.layoutChanged.emit)

    @override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: Qt.ItemDataRole | int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            # We know Song always exists, as otherwise index would be invalid
            song = cast(Song, self.repository.getSong(index.row()))
            return song.display_info[index.column()]
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
            # NOTE: Uses 1 to keep a column for info
            return 1
        return len(prefs.settings.table_tags)

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
                prefs.settings.table_tags,
            ):
                return prefs.settings.table_tags[section].display_name
            if orientation == Qt.Orientation.Vertical and section < len(
                self.repository,
            ):
                return f"{section + 1}"
            return None
        return None
