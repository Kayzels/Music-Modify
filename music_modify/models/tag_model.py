# pyright: reportIncompatibleMethodOverride=false

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
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex) -> int:
        return len(self._tags)

    @override
    def columnCount(self, parent: QModelIndex | QPersistentModelIndex) -> int:
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
