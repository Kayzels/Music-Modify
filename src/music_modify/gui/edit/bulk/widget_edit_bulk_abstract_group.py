"""Module that defines an EditBulkAbstractGroupWidget.

This is the abstract class that defines all functionality
that widgets that display grouped data should have.
"""

from abc import ABC, abstractmethod
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGroupBox, QHBoxLayout, QVBoxLayout, QWidget

from music_modify.custom_types import Song, TagInfo

from .widget_edit_bulk_abstract import EditBulkAbstractWidget


class EditBulkAbstractGroupWidget(EditBulkAbstractWidget, ABC):
    """Defines the functionality for widgets that display grouped data.

    Attributes:
        group_box: The checkable box that the widget should be contained in.
        clear_checkbox: A checkbox that, when checked, clears the data.
        form_container: The container that holds the form that holds the main widget.
    """

    def __init__(self, tag: TagInfo, parent: QWidget | None = None) -> None:
        """Creates a widget for bulk editing on the `parent` widget.

        Args:
            tag: The tag that the data should be displayed for.
            parent: The widget that this widget should be displayed on.
        """
        super().__init__(tag, parent)

        self.group_box: QGroupBox
        "The checkable box that the widget should be contained in."
        self.clear_checkbox: QCheckBox
        "A checkbox that, when checked, clears the data."
        self.form_container: QWidget
        "The container that holds the form that holds the main widget."

    @override
    def setupUi(self) -> None:
        self.group_box = QGroupBox(self.tag.display_name)
        group_layout = QVBoxLayout()
        self.group_box.setCheckable(True)
        self.group_box.setLayout(group_layout)
        # Have the group disabled by default
        self.group_box.setChecked(False)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.clear_checkbox = QCheckBox("Clear")
        self.clear_checkbox.stateChanged.connect(self._toggleClearState)
        group_layout.addWidget(self.clear_checkbox)

        self.form_container = self.createForm()
        group_layout.addWidget(self.form_container)

        main_layout.addWidget(self.group_box)
        self.setLayout(main_layout)

    @abstractmethod
    def createForm(self) -> QWidget:
        """Creates the form layout that holds the widgets needed."""

    def _toggleClearState(self, state: Qt.CheckState) -> None:
        """Toggle whether the data should be cleared on confirm, or not."""
        self.form_container.setEnabled(state == Qt.CheckState.Unchecked.value)

    @abstractmethod
    def _resetView(self) -> None:
        """Resets the display to be the same as it was on initialisation."""

    def _handleCheckboxes(self, songs: list[Song]) -> set[Song] | None:
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
            return set()
        if not self.clear_checkbox.isChecked():
            return None
        updated_songs: set[Song] = set()
        for song in songs:
            if song.hasTag(self.tag.id3_key):
                song.removeTag(self.tag.id3_key)
                updated_songs.add(song)
        self._resetView()
        return updated_songs
