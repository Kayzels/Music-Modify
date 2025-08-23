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

    @override
    def updateTag(self, songs: list[Song]) -> bool:  # noqa: C901, PLR0912
        if not self.group_box.isChecked():
            return False
        if self.clear_checkbox.isChecked():
            any_updated = False
            for song in songs:
                if self.tag.hasTag(song.id3):
                    any_updated = True
                    self.tag.removeTag(song.id3)
            self._resetView()
            return any_updated

        add_values = self.add_line.items
        remove_values = self.remove_line.values

        if not add_values and not remove_values:
            self._resetView()
            return False

        all_items: list[str] = list(self.items)

        any_updated = False
        for song in songs:
            original_values = cast(list[str] | None, self.tag.getValue(song.id3))
            if original_values is None:
                if not add_values:
                    continue
                if not self.tag.hasTag(song.id3):
                    self.tag.generateFrame(song.id3)
                original_values = []

            if add_values:
                new_values = [
                    value for value in add_values if value not in original_values
                ]
                if new_values:
                    any_updated = True
                    values = original_values + new_values
                    self.tag.setTag(song.id3, values)

                    all_items += [
                        value for value in new_values if value not in all_items
                    ]
                    self.items = tuple(all_items)
                    # Need to update this, so that remove_values has the right values
                    original_values = values

            if remove_values:
                new_values = [
                    value for value in original_values if value not in remove_values
                ]
                if new_values != original_values:
                    any_updated = True
                    self.tag.setTag(song.id3, new_values)

        if any_updated:
            self._resetView()

        return any_updated

        # TODO: Consider the logic for adding and removing.
        # At the moment, adding is processed before removing,
        # but this might not be obvious
