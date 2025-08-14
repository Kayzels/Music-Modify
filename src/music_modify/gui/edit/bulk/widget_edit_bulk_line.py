"""Module that contains the widget that is used for bulk editing
single value keys."""

import logging
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QWidget,
)

from music_modify.custom_types import Song, SongTag
from music_modify.gui.completion import EditWithComplete, createCompletionWidget

from .widget_edit_bulk_abstract import EditBulkAbstractWidget

logger = logging.getLogger(__name__)


class EditBulkLineWidget(EditBulkAbstractWidget):
    """Widget used for bulk editing single value keys."""

    def __init__(
        self,
        parent: QWidget,
        data: set[str],
        tag: SongTag,
        *,
        in_all: bool = False,
    ) -> None:
        super().__init__(parent, tag)

        self.items: tuple[str, ...] = tuple(data)

        self.main_widget: EditWithComplete = createCompletionWidget(
            self,
            items=self.items,
            multiple=False,
            initial=self.items[0] if in_all else "",
        )

        self.setupUi()

    @override
    def setupUi(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.main_widget)

        self.apply_checkbox: QCheckBox = QCheckBox("Apply")
        layout.addWidget(self.apply_checkbox)
        self.clear_checkbox: QCheckBox = QCheckBox("Clear")
        layout.addWidget(self.clear_checkbox)

        # Ensure the two checkboxes are mutually exclusive.
        # Needs to be done manually, to ensure deselection is possible.
        self.apply_checkbox.stateChanged.connect(
            lambda state: self._checkboxStateChanged(state, self.clear_checkbox),
        )
        self.clear_checkbox.stateChanged.connect(
            lambda state: self._checkboxStateChanged(state, self.apply_checkbox),
        )

    @staticmethod
    def _checkboxStateChanged(state: Qt.CheckState, other: QCheckBox) -> None:
        """When Apply is checked, uncheck Clear, and vice versa."""
        if state == Qt.CheckState.Checked.value:
            other.setChecked(False)

    @override
    def updateTag(self, songs: list[Song]) -> bool:
        """Update the value in all the songs sent for the tag this widget displays.
        If apply is selected, set the data to have the value in the main widget.
        If clear is selected, clear the data for that tag.
        Returns whether the songs have been updated or not."""
        should_apply = self.apply_checkbox.isChecked()
        should_clear = self.clear_checkbox.isChecked()

        if not should_apply and not should_clear:
            return False

        if should_apply:
            value = self.main_widget.text().strip()
            if value == "":
                should_clear = True
            else:
                logger.info(f"Setting value {value} for tag {self.tag.display_name}")
                for song in songs:
                    # PERF: Only update if the value isn't the same?
                    self.tag.setTag(song.id3, [value])
                    self.main_widget.setText(value)

        if should_clear:
            logger.info(f"Removing tag for {self.tag.display_name}")
            for song in songs:
                self.tag.removeTag(song.id3)
            self.main_widget.clear()

        return True
