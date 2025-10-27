"""Module that defines a `TagModel`.

This model defines which frames in a song should be displayed and editable.
"""

import copy
import dataclasses
import logging
from typing import cast, override

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    Signal,
)

from music_modify.core import constants
from music_modify.core.enums import EditorType
from music_modify.custom_types import TagInfo
from music_modify.utils import tableHeader

logger = logging.getLogger(__name__)

TAG_MODEL_COLUMNS = dataclasses.fields(TagInfo)
"List of display names for the tags that should be managed."


class TagModel(QAbstractTableModel):
    """Stores the information about the different tags that should be displayed."""

    invalid_input: Signal = Signal(str)
    "Signal that is emitted when a user enters invalid input."

    def __init__(self, tags: list[TagInfo]) -> None:
        """Create a new TagModel, based on the list of tags.

        Args:
            tags: A list of details about the tags that the model should manage.
        """
        super().__init__()
        self._tags: list[TagInfo] = tags

    @override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = constants.Q_MODEL_INDEX,
    ) -> int:
        return len(self._tags)

    @override
    def columnCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = constants.Q_MODEL_INDEX,
    ) -> int:
        return len(TAG_MODEL_COLUMNS)

    @override
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: Qt.ItemDataRole | int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if (
            role != Qt.ItemDataRole.DisplayRole
            or orientation == Qt.Orientation.Vertical
        ):
            return None
        if section >= self.columnCount() or section < 0:
            return None
        return tableHeader(TAG_MODEL_COLUMNS[section].name)

    @override
    def data(  # noqa: PLR0911
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: Qt.ItemDataRole | int = Qt.ItemDataRole.DisplayRole,
    ) -> str | Qt.CheckState | None:
        if not index.isValid() or (
            (col := index.column()) >= self.columnCount() or col < 0
        ):
            return None

        row = index.row()
        field = TAG_MODEL_COLUMNS[col]

        if field.type is bool:
            if role == Qt.ItemDataRole.CheckStateRole:
                return (
                    Qt.CheckState.Checked
                    if getattr(self._tags[row], field.name)
                    else Qt.CheckState.Unchecked
                )
            if role == Qt.ItemDataRole.DisplayRole:
                return ""
            return None

        if field.name == "editor_type":
            editor_type_enum = getattr(self._tags[row], field.name)
            if role == Qt.ItemDataRole.DisplayRole:
                return editor_type_enum.value
            if role == Qt.ItemDataRole.EditRole:
                return editor_type_enum
            return None

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return getattr(self._tags[row], field.name)

        return None

    @override
    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        col = index.column()
        field = TAG_MODEL_COLUMNS[col]

        if field.type is bool:
            return super().flags(index) | Qt.ItemFlag.ItemIsUserCheckable
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    @override
    def setData(  # noqa: PLR0911
        self,
        index: QModelIndex | QPersistentModelIndex,
        value: str | int,
        role: Qt.ItemDataRole | int = Qt.ItemDataRole.EditRole,
    ) -> bool:
        if not index.isValid():
            return False

        col = index.column()
        row = index.row()
        field = TAG_MODEL_COLUMNS[col]

        # Editing display name or id3_key
        if role == Qt.ItemDataRole.EditRole and field.name in (
            "display_name",
            "id3_key",
        ):
            value = cast(str, value)
            if value == "":
                self.invalid_input.emit(f"{tableHeader(field.name)} cannot be empty.")
                return False
            if value in (
                getattr(tag, field.name) for i, tag in enumerate(self._tags) if i != row
            ):
                self.invalid_input.emit(
                    f"{tableHeader(field.name)} with {value} already exists.",
                )
                return False

            # Only update the value if it's not the same already
            if getattr(self._tags[row], field.name) != value:
                setattr(self._tags[row], field.name, value)
                self.dataChanged.emit(index, index, [role])
            return True

        # Editing checkbox for Bool columns
        if field.type is bool and role == Qt.ItemDataRole.CheckStateRole:
            value = cast(int, value)
            # Need to convert to the enum value for comparison,
            # otherwise it's always false.
            setattr(self._tags[row], field.name, value == Qt.CheckState.Checked.value)
            self.dataChanged.emit(index, index, [role])
            return True

        if field.name == "editor_type" and role == Qt.ItemDataRole.EditRole:
            new_editor_type: EditorType | None = None
            for et in EditorType:
                if value == et.value:
                    new_editor_type = et
                    break

            if new_editor_type is None:
                logger.warning(f"Could not find EditorType for value: {value}")
                return False

            if getattr(self._tags[row], field.name) != new_editor_type:
                setattr(self._tags[row], field.name, new_editor_type)
                self.dataChanged.emit(index, index, [role])
            return True

        return False

    def addTag(
        self,
        *,
        id3_key: str,
        display_name: str,
        show_in_table: bool = False,
    ) -> None:
        """Add a Tag with the given information to the model.

        Args:
            id3_key: The frame in the song that this tag refers to
            display_name: The human-readable name for the id3 key
            show_in_table: Whether this tag should be displayed in the main table,
                or just stored.
        """
        new_tag: TagInfo = TagInfo(
            id3_key=id3_key,
            display_name=display_name,
            show_in_table=show_in_table,
        )
        self.beginInsertRows(QModelIndex(), len(self._tags), len(self._tags))
        self._tags.append(new_tag)
        self.endInsertRows()

    def removeTag(self, row: int) -> None:
        """Remove the tag at the specific row from the model."""
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._tags[row]
        self.endRemoveRows()

    def moveTag(self, source_row: int, destination_row: int) -> None:
        """Move the tag information at the source row to the destination row."""
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

    @property
    def tags(self) -> list[TagInfo]:
        """The current grouping of tags used for song metadata manipulation."""
        return self._tags

    @tags.setter
    def tags(self, tags: list[TagInfo]) -> None:
        # Resets the model and sets it to have the tags defined in the given list.
        # Creates a copy of the tags list sent in, to avoid modifying the original.
        # This is needed so that the default value isn't altered,
        # and to allow multiple resets.
        self.beginResetModel()
        self._tags = copy.deepcopy(tags)
        self.endResetModel()
