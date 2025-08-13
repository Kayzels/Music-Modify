"""Module that defines the model that is used for completion
in widgets, when entering text."""

# Adapted from https://github.com/kovidgoyal/calibre/blob/master/src/calibre/gui2/complete2.py

from typing import override

from PySide6.QtCore import QAbstractListModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtWidgets import QWidget

from music_modify.custom_types import qt_types


def primary_contains(word: str, key: str) -> bool:
    """Function that checks whether `key` appears in `word`."""
    return key in word


def primary_startswith(word: str, key: str) -> bool:
    """Function that checks whether `key` is at the start of `word`."""
    return word.startswith(key)


class CompleteModel(QAbstractListModel):
    """Model that is used for text completion suggestions."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        strip_completion_entries: bool = True,
    ) -> None:
        super().__init__(parent)

        self.strip_completion_entries: bool = strip_completion_entries
        self.all_items: tuple[str, ...] = ()
        self.current_items: tuple[str, ...] = ()
        self.current_prefix: str = ""

    def setItems(self, items: tuple[str, ...]) -> None:
        """Sets the items that should be used as suggestions when typing."""
        if self.strip_completion_entries:
            item_gen = (str(x).strip() for x in items if x)
        else:
            item_gen = (str(x) for x in items if x)
        new_items = tuple(sorted(item_gen))
        self.beginResetModel()
        self.all_items = self.current_items = new_items
        self.current_prefix = ""
        self.endResetModel()

    def setCompletionPrefix(self, prefix: str) -> None:
        """Sets the text that should be used as a filter for completion suggestions."""
        old_prefix = self.current_prefix
        self.current_prefix = prefix
        if prefix == old_prefix:
            return
        if not prefix:
            self.beginResetModel()
            self.current_items = self.all_items
            self.endResetModel()
            return
        subset = prefix.startswith(old_prefix)
        universe = self.current_items if subset else self.all_items

        self.beginResetModel()
        self.current_items = tuple(x for x in universe if primary_contains(x, prefix))
        self.endResetModel()

    @override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = qt_types.Q_MODEL_INDEX,
    ) -> int:
        return len(self.current_items)

    @override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex = qt_types.Q_MODEL_INDEX,
        role: Qt.ItemDataRole | int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            item = self.current_items[index.row()].replace("\n", " ")
            if not self.strip_completion_entries:
                left = item.lstrip()
                if len(left) < len(item):
                    item = "␣" * (len(item) - len(left)) + left
                right = item.rstrip()
                if len(right) < len(item):
                    item = right + "␣" * (len(item) - len(right))
            return item
        if role == Qt.ItemDataRole.UserRole:
            return self.current_items[index.row()]

        return None

    def indexForPrefix(self, prefix: str) -> QModelIndex | None:
        """Gets the index of the first item that starts with the given string."""
        for i, item in enumerate(self.current_items):
            if primary_startswith(item, prefix):
                return self.index(i)

        return None

    @override
    def index(
        self,
        row: int,
        column: int | None = 0,
        parent: QModelIndex | QPersistentModelIndex = qt_types.Q_MODEL_INDEX,
    ) -> QModelIndex:
        return super().index(row, column, parent)
