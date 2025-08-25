"""Module that defines the model that is used for completion in widgets."""

# Adapted from https://github.com/kovidgoyal/calibre/blob/master/src/calibre/gui2/complete2.py

from typing import override

from PySide6.QtCore import QAbstractListModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtWidgets import QWidget

from music_modify.custom_types import constants


class CompleteModel(QAbstractListModel):
    """Model that is used for text completion suggestions.

    Attributes:
        strip_completion_entries (bool): Whether the entires should keep or remove
            leading and trailing whitespace
        all_items (tuple[str, ...]): The unfiltered possible items that can be listed
            as suggestions
        current_items (tuple[str, ...]): The possible items that can be listed as
            suggestions, based on `current_prefix`
        current_prefix (str): The text used to filter items to only include the ones
            that start with this value
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        strip_completion_entries: bool = True,
    ) -> None:
        """Creates a model that can be used for completion.

        Args:
            parent: The widget that the model should be used for
            strip_completion_entries: Whether the entries should keep or remove
                leading and trailing whitespace
        """
        super().__init__(parent)

        self.strip_completion_entries: bool = strip_completion_entries
        "Whether the entries should keep or remove leading and trailing whitespace"
        self.all_items: tuple[str, ...] = ()
        "The possible items that can be listed as suggestions"
        self.current_items: tuple[str, ...] = ()
        "The filtered possible items that can be listed as suggestions"
        self.current_prefix: str = ""
        "The text used to filter items to include only ones that start with this value"

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
        self.current_items = tuple(x for x in universe if prefix in x)
        self.endResetModel()

    @override
    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = constants.Q_MODEL_INDEX,
    ) -> int:
        return len(self.current_items)

    @override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex = constants.Q_MODEL_INDEX,
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
            if item.startswith(prefix):
                return self.index(i)

        return None

    @override
    def index(
        self,
        row: int,
        column: int | None = 0,
        parent: QModelIndex | QPersistentModelIndex = constants.Q_MODEL_INDEX,
    ) -> QModelIndex:
        return super().index(row, column, parent)
