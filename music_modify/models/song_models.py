# pyright: reportIncompatibleMethodOverride=false

from typing import Final, override
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    QSortFilterProxyModel,
)
from music_modify.models.song_repository import SongRepository
from music_modify.prefs.settings import settings


class SongTableModel(QAbstractTableModel):
    empty_message: Final[str] = "Files will show here when added. Drag files here."

    def __init__(self, repository: SongRepository):
        super().__init__()
        self.repository: SongRepository = repository

    @override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            song = self.repository.get_songs()[index.row()]
            tag_info = song.display_info[index.column()]
            return tag_info
        return None

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex) -> int:
        return len(self.repository)

    @override
    def columnCount(self, parent: QModelIndex | QPersistentModelIndex) -> int:
        if self.rowCount(parent) == 0:
            return 1
            # ? Uses 1 to keep a column for info
        else:
            return len(settings.file_tags)

    @override
    def headerData(
        self, section: int, orientation: Qt.Orientation, /, role: Qt.ItemDataRole
    ) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            if len(self.repository) == 0:
                if orientation == Qt.Orientation.Horizontal:
                    return SongTableModel.empty_message
                if orientation == Qt.Orientation.Vertical:
                    return None
            if orientation == Qt.Orientation.Horizontal:
                return settings.file_tags[section].display_name
            elif orientation == Qt.Orientation.Vertical:
                return f"{section + 1}"
        return None


class SongTableProxyModel(QSortFilterProxyModel):
    """Model used to show selected songs being edited"""

    def __init__(self):
        super().__init__()
        self.model_indexes: list[QModelIndex] = []
        self.selected_rows: list[int] = []

    @override
    def filterAcceptsRow(self, source_row: int, _: QModelIndex) -> bool:
        return source_row in self.selected_rows

    def change_model_indexes(self, model_indexes: list[QModelIndex]):
        self.model_indexes = model_indexes
        self.selected_rows = [model_index.row() for model_index in self.model_indexes]
        self.invalidateFilter()
