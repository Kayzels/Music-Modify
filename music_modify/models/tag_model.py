# pyright: reportIncompatibleMethodOverride=false, reportCallInDefaultInitializer=false

import logging
from typing import override, NamedTuple

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

from music_modify.custom_types import TagInfo

logger = logging.getLogger(__name__)


class ColumnId(NamedTuple):
    key: str
    display_name: str


TAG_MODEL_COLUMNS: tuple[ColumnId, ...] = (
    ColumnId(key="show_in_table", display_name="Show"),
    ColumnId(key="id3_key", display_name="ID3 Key"),
    ColumnId(key="display_name", display_name="Display Name"),
)


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
        return len(TAG_MODEL_COLUMNS)

    @override
    def headerData(
        self, section: int, orientation: Qt.Orientation, /, role: Qt.ItemDataRole
    ) -> str | None:
        if (
            role != Qt.ItemDataRole.DisplayRole
            or orientation == Qt.Orientation.Vertical
        ):
            return None
        if section >= self.columnCount() or section < 0:
            return None
        return TAG_MODEL_COLUMNS[section].display_name

    @override
    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: Qt.ItemDataRole
    ) -> str | Qt.CheckState | None:
        if not index.isValid():
            return None

        col = index.column()
        if col >= self.columnCount() or col < 0:
            return None

        row = index.row()
        field = TAG_MODEL_COLUMNS[col].key

        if field == "show_in_table":
            if role == Qt.ItemDataRole.CheckStateRole:
                return (
                    Qt.CheckState.Checked
                    if getattr(self._tags[row], field)
                    else Qt.CheckState.Unchecked
                )
            if role == Qt.ItemDataRole.DisplayRole:
                return ""

        if role == Qt.ItemDataRole.DisplayRole:
            return getattr(self._tags[row], field)

        return None

    @override
    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        col = index.column()
        field = TAG_MODEL_COLUMNS[col].key

        if field == "show_in_table":
            return super().flags(index) | Qt.ItemFlag.ItemIsUserCheckable

        return super().flags(index)

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
