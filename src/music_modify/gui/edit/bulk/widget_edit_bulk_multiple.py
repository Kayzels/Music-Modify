"""Module that defines an EditBulkMultipleWidget.

This widget is used for bulk editing data, when the tag can contain multiple values,
but these values are not pairs.
"""

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
    """Widget used for bulk editing data when the tag contains multiple values."""

    def __init__(self, parent: QWidget, data: set[str], tag: SongTag) -> None:
        """Create a widget for bulk editing multiple value keys.

        Args:
            parent: The widget that this widget shouldbe displayed on.
            data: The data to be displayed.
            tag: The field in the song that should be updated.
        """
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

    def _handleCheckboxes(self, songs: list[Song]) -> bool | None:
        """Process the updating of the tag when either of the checkboxes are checked.

        Returns:
            True if any of the songs data has changed.
            None if there is further processing needed after checking the checkboxes.

        Information:
            If group_box isn't checked, returns False.
            If clear_checkbox is checked, it removes the tag from all existing songs.
            Otherwise, we need more information, so returns None.
        """
        if not self.group_box.isChecked():
            return False
        if not self.clear_checkbox.isChecked():
            return None
        any_updated = False
        for song in songs:
            if self.tag.hasTag(song.id3):
                any_updated = True
                self.tag.removeTag(song.id3)
        self._resetView()
        return any_updated

    def _getSongValue(self, song: Song) -> list[str] | None:
        """Returns the value stored in the song.

        If the song doesn't have the tag, and we plan to add to it,
        it creates the tag.

        Returns None if the song doesn't have the tag, but we aren't
        adding anything to it.
        """
        song_values = cast(list[str] | None, self.tag.getValue(song.id3))
        if song_values is None:
            if not self.add_line.items:
                return None
            self.tag.generateFrame(song.id3)
            return []
        return song_values

    def _addValuesToSong(self, song: Song) -> bool:
        """Add the values from add_line to the song.

        If the values aren't in the list of items for the current widget,
        adds them so that they are part of the completion suggestions.

        Returns:
            True if the values are added to any of the songs.
        """
        song_values = self._getSongValue(song)
        if song_values is None:
            return False
        add_values = self.add_line.items
        new_values = [value for value in add_values if value not in song_values]
        if not new_values:
            return False
        values = song_values + new_values

        widget_items = list(self.items)
        self.items = tuple(
            widget_items + [value for value in new_values if value not in widget_items]
        )
        self.tag.setTag(song.id3, values)
        return True

    def _removeValuesFromSong(self, song: Song) -> bool:
        """Remove the values from remove_line from the song."""
        remove_values = self.remove_line.values
        if not remove_values:
            return False
        song_values = self._getSongValue(song)
        if song_values is None:
            return False
        new_values = [value for value in song_values if value not in remove_values]
        if new_values != song_values:
            self.tag.setTag(song.id3, new_values)
            return True
        return False

    @override
    def updateTag(self, songs: list[Song]) -> bool:
        checkbox_result = self._handleCheckboxes(songs)
        if checkbox_result is not None:
            return checkbox_result

        any_updated = False
        for song in songs:
            any_updated = self._addValuesToSong(song) or any_updated
            any_updated = self._removeValuesFromSong(song) or any_updated

        if any_updated:
            self._resetView()

        return any_updated

        # TODO: Consider the logic for adding and removing.
        # At the moment, adding is processed before removing,
        # but this might not be obvious
