"""Module that defines a dialog that allows editing the metadata for a song."""

import copy
import logging
from typing import override

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QFormLayout,
    QPushButton,
    QScrollArea,
    QWidget,
)

from music_modify.custom_types import Song, SongTag
from music_modify.custom_types.aliases import SongEditData
from music_modify.custom_types.enums import NavDirection
from music_modify.custom_types.utils import mapKey
from music_modify.gui.utils import clearLayout
from music_modify.models.song_repository import SongRepository
from music_modify.prefs import prefs

from .dialog_edit_abstract import EditAbstractDialog
from .widget_edit_abstract import EditAbstractWidget
from .widget_edit_factory import EditAbstractWidgetType, EditWidgetFactory

logger = logging.getLogger(__name__)


class EditDialog(EditAbstractDialog):
    """Displays all tags for a song, in a format that can be edited."""

    def __init__(
        self,
        parent: QWidget,
        repository: SongRepository,
        rows: list[int],
    ) -> None:
        """Creates a dialog for editing songs individually.

        Args:
            parent: The widget that the dialog should be displayed on.
            repository: The list of songs being managed by the app.
            rows: The indexes of the songs to be edited in the `repository`.
        """
        super().__init__(parent, repository, rows)

        if len(rows) == 0:
            self.reject()
            return

        self.current_index: int = 0
        "The index of this specific song in the song repository"

        song_info = self._getSong()
        if song_info is None:
            self.reject()
            return

        self.song_info: Song = song_info
        self.setupUi()

        self.changed_values: dict[str, SongEditData | None] = {}

        # Add reset button here rather than in abstract.
        self.button_box.addButton(QDialogButtonBox.StandardButton.Reset)
        self.button_box.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(
            self.resetSongInfo,
        )

        # Add before and after buttons if more than one passed through
        if len(rows) > 1:
            self.previous_button: QPushButton = QPushButton(
                QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious)),
                "Previous",
            )
            self.previous_button.clicked.connect(
                lambda: self.showSongInDirection(NavDirection.Previous),
            )
            self.button_box.addButton(
                self.previous_button,
                QDialogButtonBox.ButtonRole.ActionRole,
            )

            self.next_button: QPushButton = QPushButton(
                QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext)),
                "Next",
            )
            self.next_button.clicked.connect(
                lambda: self.showSongInDirection(NavDirection.Next),
            )
            self.button_box.addButton(
                self.next_button,
                QDialogButtonBox.ButtonRole.ActionRole,
            )

            self._switchButtonState()

        self.song_layout: QFormLayout

    @override
    def _setupSongInfo(self) -> None:
        """Creates and displays the widgets for each tag in the song."""
        scroll_widget: QWidget = QWidget()
        if hasattr(self, "song_layout"):
            clearLayout(self.song_layout)
        else:
            self.song_layout = QFormLayout(scroll_widget)

        for tag in prefs.settings.all_tags:
            # Needs to be a copy to avoid editing the tag prematurely.
            current_data = copy.deepcopy(tag.getValue(self.song_info.id3))
            widget = self._createWidgetType(tag, current_data)
            self.song_layout.addRow(tag.display_name, widget)

        if not hasattr(self, "scroll_area"):
            self.scroll_area: QScrollArea = QScrollArea(self)
            self.scroll_area.setWidget(scroll_widget)
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setMinimumHeight(300)
            self.main_layout.addWidget(self.scroll_area)

        self.resize(600, 300)

    def _createWidgetType(self, tag: SongTag, data: SongEditData | None) -> QWidget:
        """Creates the widget of the required type based on the tag and data.

        It also links the signals needed for updating and resetting it.
        """
        # noinspection PyTypeHints
        widget: EditAbstractWidgetType = EditWidgetFactory.createWidget(self, tag, data)

        @Slot()
        def updateValue() -> None:
            """Stores the updated value of the widget."""
            # We want to remove values if they are empty,
            # which is marked by making the changed_value for that key None.
            value = widget.value
            if len(value) == 0:
                value = None
            self.changed_values[tag.id3_key] = value
            logger.debug(f"Value is {widget.value}")
            logger.debug(f"Changed values are {self.changed_values}")

        @Slot()
        def resetValue() -> None:
            """Clears value if it's the same as the original, and currently in the song.

            Otherwise, stores the change.
            """
            # This is needed because after a user clicks Apply,
            # the value stored in the song is now no longer the same as the original,
            # so we can't just clear it.
            value = widget.value

            # Need to get the value inside the song and compare
            song_value = tag.getValue(self.song_info.id3)
            if song_value is None and len(value) != 0:
                # The value in the song was cleared, but we have a value now that isn't
                logger.debug(
                    (
                        f"Value for key {tag.id3_key} previously removed, "
                        "but being reset now."
                    ),
                )
                self.changed_values[tag.id3_key] = value
                logger.debug(f"Changed values are now {self.changed_values}")
            elif song_value is None and len(value) == 0:
                # Same empty value, no need to remember
                logger.debug(
                    (
                        f"Song doesn't store the key {tag.id3_key} "
                        "and the value for it is being set to empty."
                    ),
                )
                self.changed_values.pop(tag.id3_key, None)
                logger.debug(f"Changed values are now {self.changed_values}")
            elif song_value != value:
                # New value than what is stored in the song (same as original value)
                logger.debug(
                    (
                        f"Value stored in song for key {tag.id3_key} "
                        "is different from the value being reset to, so storing."
                    ),
                )
                if len(value) == 0:
                    self.changed_values[tag.id3_key] = None
                else:
                    self.changed_values[tag.id3_key] = value
                logger.debug(f"Changed values are now {self.changed_values}")
            else:
                # Value matches existing song value, remove from change list.
                logger.debug(
                    (
                        f"Value matches the value in the song for {tag.id3_key}, "
                        "so removing from changed values."
                    ),
                )
                self.changed_values.pop(tag.id3_key, None)
                logger.debug(f"Changed values are now {self.changed_values}")

        widget.value_updated.connect(updateValue)
        widget.value_reset.connect(resetValue)

        return widget

    @override
    def updateSongInfo(self) -> None:
        """Adds the changes to the song, and saves it."""
        if len(self.changed_values) == 0:
            return
        logger.debug("Called updateSong")
        for id3_key, value in self.changed_values.items():
            tag: SongTag | None = mapKey(id3_key, prefs.settings.all_tags)
            if tag is None:
                logger.debug(f"Unknown id3 key: {id3_key}")
                continue
            if value is None:
                # Remove tag from song
                logger.debug(f"Value was None, so removing key {id3_key}")
                tag.removeTag(self.song_info.id3)
                continue
            new_value = value

            # Mutagen ID3 frames always store their values in a list,
            # so need to convert to that format.
            if isinstance(new_value, str):
                new_value = [new_value]
            logger.debug(f"Setting tag for {id3_key} to {new_value}")
            tag.setTag(self.song_info.id3, new_value)
        self.song_info.save()
        self.info_updated.emit()

        # Clear the values: they've been changed in the song,
        # so don't need to be stored in this list anymore
        self.changed_values = {}

    def resetSongInfo(self) -> None:
        """Sets values for the song back to original ones before changes occurred."""
        widgets = self.findChildren(EditAbstractWidget)
        for widget in widgets:
            widget.reset()

    def _getSong(self) -> Song | None:
        """Gets the song based on the index of the list of indexes.

        Returns `None` if not valid.
        """
        row = self.rows[self.current_index]
        song_info = self.repository.getSong(row)
        if song_info is None:
            logger.warning(f"Couldn't find a song at row number {row}")
            return None
        return song_info

    def _switchButtonState(self) -> None:
        """Toggles the next and previous buttons based on where we are in the list."""
        if not hasattr(self, "next_button") or not hasattr(self, "previous_button"):
            logger.warning("Missing next or previous button in edit dialog")
            return

        self.previous_button.setEnabled(self.current_index != 0)
        self.next_button.setEnabled(self.current_index != len(self.rows) - 1)

    def showSongInDirection(self, nav_direction: NavDirection) -> None:
        """Saves changes and displays next song in given direction.

        Saves the current changes to the song,
        and displays the next or previous song from the selection
        based on the direction.
        """
        if (
            nav_direction == NavDirection.Next
            and self.current_index == len(self.rows) - 1
        ) or (nav_direction == NavDirection.Previous and self.current_index == 0):
            return
        match nav_direction:
            case NavDirection.Next:
                self.current_index += 1
            case NavDirection.Previous:
                self.current_index -= 1
        self.updateSongInfo()
        logger.debug(f"Called show song in direction with {nav_direction}")
        song_info = self._getSong()
        if song_info is None:
            logger.warning("Invalid song, closing dialog")
            self.reject()
            return
        logger.debug("Got a song")

        self.song_info = song_info
        self._switchButtonState()
        self._setupSongInfo()
