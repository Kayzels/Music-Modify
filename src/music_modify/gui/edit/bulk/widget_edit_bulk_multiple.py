"""Module that defines an EditBulkMultipleWidget.

This widget is used for bulk editing data, when the tag can contain multiple values,
but these values are not pairs.
"""

import logging
from typing import Unpack, override

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QWidget,
)

from music_modify.custom_types import Song, TagInfo
from music_modify.custom_types.qt_types import QLineEditArgs
from music_modify.custom_types.tag_value import TextTagValue
from music_modify.gui.completion import EditWithComplete
from music_modify.utils import getUnique

from .widget_edit_bulk_abstract_group import EditBulkAbstractGroupWidget

logger = logging.getLogger(__name__)


class _MultipleLineEdit(QLineEdit):
    """Private class that stores a list of strings, but displays a single string."""

    def __init__(
        self,
        value: str,
        split_text_entered: str,
        parent: QWidget | None = None,
        **kwargs: Unpack[QLineEditArgs],
    ) -> None:
        super().__init__(value, parent, **kwargs)
        self._split_text_entered = split_text_entered

    @property
    def items(self) -> list[str]:
        """The list of strings that is displayed."""
        text = self.text()
        return getUnique(text, self._split_text_entered)


class EditBulkMultipleWidget(EditBulkAbstractGroupWidget):
    """Widget used for bulk editing data when the tag contains multiple values."""

    def __init__(
        self,
        data: set[str],
        tag: TagInfo,
        parent: QWidget | None = None,
    ) -> None:
        """Create a widget for bulk editing multiple value keys.

        Args:
            parent: The widget that this widget should be displayed on.
            data: The data to be displayed.
            tag: The field in the song that should be updated.
        """
        super().__init__(tag, parent)

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
        self.add_line = _MultipleLineEdit("", self.split_text_entered)
        add_layout.addWidget(self.add_line)
        form_layout.addRow("Add", add_layout)

        remove_layout = QHBoxLayout()
        self.remove_line = EditWithComplete(
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

    def _getSongValue(self, song: Song) -> list[str] | None:
        """Returns the value stored in the song.

        If the song doesn't have the tag, and we plan to add to it,
        it creates the tag.

        Returns None if the song doesn't have the tag, but we aren't
        adding anything to it.
        """
        song_values = song.getTag(self.tag.id3_key)
        if song_values is None:
            if not self.add_line.items:
                return None
            return []
        if not isinstance(song_values, TextTagValue):
            logger.error(
                f"Expected a TextTagValue for {self.tag.id3_key}, but got {type(song_values)}"
            )
            return None
        return song_values.value

    def _addValuesToSong(self, song: Song, add_values: list[str]) -> bool:
        """Add the values from add_line to the song.

        If the values aren't in the list of items for the current widget,
        adds them so that they are part of the completion suggestions.

        Returns:
            True if the values are added to any of the songs.
        """
        song_values = self._getSongValue(song)
        if song_values is None:
            return False
        new_values = [value for value in add_values if value not in song_values]
        if not new_values:
            return False
        values = song_values + new_values

        widget_items = list(self.items)
        self.items = tuple(
            widget_items + [value for value in new_values if value not in widget_items]
        )
        song.setTag(self.tag.id3_key, TextTagValue(values))
        return True

    def _removeValuesFromSong(self, song: Song, remove_values: list[str]) -> bool:
        """Remove the values from remove_line from the song."""
        if not remove_values:
            return False
        song_values = self._getSongValue(song)
        if song_values is None:
            return False
        new_values = [value for value in song_values if value not in remove_values]
        if new_values != song_values:
            song.setTag(self.tag.id3_key, TextTagValue(new_values))
            return True
        return False

    @override
    def updateTag(self, songs: list[Song]) -> set[Song]:
        checkbox_result = self._handleCheckboxes(songs)
        if checkbox_result is not None:
            return checkbox_result

        remove_values = self.remove_line.values
        add_values = [item for item in self.add_line.items if item not in remove_values]

        updated_songs: set[Song] = set()
        for song in songs:
            added = self._addValuesToSong(song, add_values)
            removed = self._removeValuesFromSong(song, remove_values)
            if added or removed:
                updated_songs.add(song)

        if updated_songs:
            self._resetView()

        return updated_songs

        # TODO: Consider the logic for adding and removing.
        #       At the moment, adding is processed before removing,
        #       but this might not be obvious
