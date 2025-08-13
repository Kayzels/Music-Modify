"""Module that contains the widget that is used for bulk editing data,
when the tag can contain multiple values, but these values are not pairs."""

import logging
from typing import Unpack, cast, override

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QWidget,
)

from music_modify.custom_types import Song, SongTag
from music_modify.custom_types.qt_types import QLineEditArgs
from music_modify.gui.completion import EditWithComplete, createCompletionWidget
from music_modify.prefs import prefs
from music_modify.utils import getUniqueOrdered

from .widget_edit_bulk_abstract_group import EditBulkAbstractGroupWidget

logger = logging.getLogger(__name__)


class _MultipleLineEdit(QLineEdit):
    """Private class that stores a list of strings, but displays a single string."""

    def __init__(
        self,
        value: str,
        parent: QWidget | None = None,
        **kwargs: Unpack[QLineEditArgs],
    ) -> None:
        super().__init__(value, parent, **kwargs)

    @property
    def items(self) -> list[str]:
        """The list of strings that is displayed."""
        text = self.text()
        return getUniqueOrdered(text, prefs.settings.split_text_entered)


class EditBulkMultipleWidget(EditBulkAbstractGroupWidget):
    """Widget that is used for bulk editing data,
    when the tag can contain multiple values,
    but these values are not pairs."""

    def __init__(self, parent: QWidget, data: set[str], tag: SongTag) -> None:
        super().__init__(parent, tag)

        self.items: tuple[str, ...] = tuple(data)
        self.setupUi()

        self.add_line: _MultipleLineEdit
        self.remove_line: EditWithComplete

    @override
    def createForm(self) -> QWidget:
        form_layout = QFormLayout()
        # Make a container, so it can be enabled and disabled.
        form_container: QWidget = QWidget()
        form_container.setLayout(form_layout)
        form_layout.setContentsMargins(0, 0, 0, 0)

        add_layout = QHBoxLayout()
        self.add_line = _MultipleLineEdit("")
        add_layout.addWidget(self.add_line)
        form_layout.addRow("Add", add_layout)

        remove_layout = QHBoxLayout()
        self.remove_line = createCompletionWidget(
            parent=self,
            items=self.items,
            multiple=True,
        )
        remove_layout.addWidget(self.remove_line)
        form_layout.addRow("Remove", remove_layout)

        return form_container

    @override
    def _resetView(self) -> None:
        self.add_line.setText("")
        self.remove_line.setText("")
        self.remove_line.updateItemsCache(self.items)
        self.clear_checkbox.setChecked(False)
        self.group_box.setChecked(False)

    @override
    def updateTag(self, songs: list[Song]) -> bool:
        if not self.group_box.isChecked():
            return False
        should_clear = self.clear_checkbox.isChecked()
        if should_clear:
            for song in songs:
                self.tag.removeTag(song.id3)
            return True

        should_add = len(self.add_line.items) > 0
        should_remove = len(self.remove_line.values) > 0

        if not should_add and not should_remove:
            self._resetView()
            return False

        all_items: list[str] = list(self.items)
        for song in songs:
            original_values = self.tag.getValue(song.id3)
            if original_values is None:
                if not self.tag.hasTag(song.id3):
                    self.tag.generateFrame(song.id3)
                original_values = []
            original_values = cast(list[str], original_values)
            # TODO: Consider the logic for adding and removing.
            # At the moment, if the same value is in add and remove,
            # it gets added and then removed.
            # But that might not be obvious.
            if should_add:
                new_values = self.add_line.items
                not_present = [
                    value for value in new_values if value not in original_values
                ]
                values = original_values + not_present
                self.tag.setTag(song.id3, values)

                all_items += [value for value in new_values if value not in all_items]
                self.items = tuple(all_items)

                # Do this so that the remove part has the data
                original_values = values
            if should_remove:
                remove_values = self.remove_line.values
                # Doing it this way with a list comprehension,
                # so that order remains.
                values = [
                    value for value in original_values if value not in remove_values
                ]
                self.tag.setTag(song.id3, values)

        # Clear the values after an update
        self._resetView()

        return True
