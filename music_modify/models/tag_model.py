# pyright: reportIncompatibleMethodOverride=false, reportCallInDefaultInitializer=false

import logging
from typing import override

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

from music_modify.custom_types import TagInfo

logger = logging.getLogger(__name__)


class TagModel(QAbstractTableModel):
    def __init__(self, tags: list[TagInfo]):
        super().__init__()
        self._tags: list[TagInfo] = tags

    @override
    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self._tags)

    @override
    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        # ID3 Tag, Display Name
        return 2

    @override
    def headerData(
        self, section: int, orientation: Qt.Orientation, /, role: Qt.ItemDataRole
    ) -> str | None:
        if (
            role != Qt.ItemDataRole.DisplayRole
            or orientation == Qt.Orientation.Vertical
        ):
            return None
        match section:
            case 0:
                return "ID3 Tag"
            case 1:
                return "Display Name"
            case _:
                return None

    @override
    def data(
        self, index: QModelIndex | QPersistentModelIndex, /, role: Qt.ItemDataRole
    ) -> str | None:
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        col = index.column()
        if col > 1 or col < 0:
            return None
        row = index.row()
        field = "id3_key" if col == 0 else "display_name"
        return getattr(self._tags[row], field)
        # return self._tags[row][field]

    def addTag(self, id3_key: str, display_name: str, show_in_table: bool = False):
        new_tag: TagInfo = TagInfo(id3_key, display_name, show_in_table)
        self.beginInsertRows(QModelIndex(), len(self._tags), len(self._tags))
        self._tags.append(new_tag)
        self.endInsertRows()

    def removeTag(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._tags[row]
        self.endRemoveRows()

    def moveTag(self, source_row: int, destination_row: int):
        if (
            source_row < 0
            or destination_row < 0
            or source_row >= self.rowCount()
            or destination_row >= self.rowCount()
        ):
            return

        # Need to add 1 to destination if source is lower, otherwise stays in same place
        self.beginMoveRows(
            QModelIndex(),
            source_row,
            source_row,
            QModelIndex(),
            destination_row + (1 if source_row < destination_row else 0),
        )
        self._tags.insert(destination_row, self._tags.pop(source_row))
        self.endMoveRows()
