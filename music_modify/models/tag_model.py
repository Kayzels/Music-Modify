# pyright: reportIncompatibleMethodOverride=false, reportCallInDefaultInitializer=false

import dataclasses
import logging
from typing import override, cast

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    Signal,
)

from music_modify.custom_types import TagInfo
from music_modify.utils import tableHeader

logger = logging.getLogger(__name__)

TAG_MODEL_COLUMNS = [field.name for field in dataclasses.fields(TagInfo)]


class TagModel(QAbstractTableModel):
    invalid_input: Signal = Signal(str)

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
        return tableHeader(TAG_MODEL_COLUMNS[section])

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
        field = TAG_MODEL_COLUMNS[col]

        if field == "show_in_table":
            if role == Qt.ItemDataRole.CheckStateRole:
                return (
                    Qt.CheckState.Checked
                    if getattr(self._tags[row], field)
                    else Qt.CheckState.Unchecked
                )
            if role == Qt.ItemDataRole.DisplayRole:
                return ""
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return getattr(self._tags[row], field)

        return None

    @override
    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        col = index.column()
        field = TAG_MODEL_COLUMNS[col]

        if field == "show_in_table":
            return super().flags(index) | Qt.ItemFlag.ItemIsUserCheckable
        elif field in ("display_name", "id3_key"):
            return super().flags(index) | Qt.ItemFlag.ItemIsEditable

        return super().flags(index)

    @override
    def setData(
        self,
        index: QModelIndex | QPersistentModelIndex,
        value: str | int,
        role: Qt.ItemDataRole,
    ) -> bool:
        if not index.isValid():
            return False

        col = index.column()
        row = index.row()
        field = TAG_MODEL_COLUMNS[col]

        # Editing display name or id3_key
        if role == Qt.ItemDataRole.EditRole and field in ("display_name", "id3_key"):
            value = cast(str, value)
            if value == "":
                self.invalid_input.emit(f"{tableHeader(field)} cannot be empty.")
                return False
            if value in (
                getattr(tag, field) for i, tag in enumerate(self._tags) if i != row
            ):
                self.invalid_input.emit(
                    f"{tableHeader(field)} with {value} already exists."
                )
                return False

            # Update the value
            setattr(self._tags[row], field, value)
            self.dataChanged.emit(index, index, [role])
            return True

        # Editing checkbox for Show column
        if field == "show_in_table" and role == Qt.ItemDataRole.CheckStateRole:
            value = cast(int, value)
            # Note that you need to convert to the enum value for comparison,
            # otherwise it's always false.
            self._tags[row].show_in_table = value == Qt.CheckState.Checked.value
            self.dataChanged.emit(index, index, [role])
            return True

        return False

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

    def setTags(self, tags: list[TagInfo]) -> None:
        """Resets the model and sets the model to have the tags defined in the given list.
        The list being sent in should be a copy, unless you want to edit the original list."""
        self.beginResetModel()
        self._tags = tags
        self.endResetModel()
