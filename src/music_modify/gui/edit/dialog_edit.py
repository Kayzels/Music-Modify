"""Module that defines a dialog that allows editing the metadata for a song."""

import logging
from typing import TYPE_CHECKING, override

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QFormLayout,
    QPushButton,
    QScrollArea,
    QWidget,
)

from music_modify.core.enums import NavDirection
from music_modify.custom_types import Song, TagInfo
from music_modify.gui.utils import clearLayout
from music_modify.models.song_repository import SongRepository

from .dialog_edit_abstract import EditAbstractDialog
from .widget_edit_factory import EditWidgetFactory

if TYPE_CHECKING:
    from .widget_edit_abstract import EditAbstractWidget

logger = logging.getLogger(__name__)


class EditDialog(EditAbstractDialog):
    """Displays all tags for a song, in a format that can be edited."""

    def __init__(
        self,
        repository: SongRepository,
        rows: list[int],
        all_tags: list[TagInfo],
        parent: QWidget | None = None,
    ) -> None:
        """Creates a dialog for editing songs individually.

        Args:
            parent: The widget that the dialog should be displayed on.
            repository: The list of songs being managed by the app.
            rows: The indexes of the songs to be edited in the `repository`.
            all_tags: Tags that are available for reading and editing
        """
        super().__init__(repository, rows, parent)

        self._all_tags: list[TagInfo] = all_tags

        if len(rows) == 0:
            self.reject()
            return

        self.current_index: int = 0
        "The index of this specific song in the song repository"

        try:
            song_info = self._getSong()
        except IndexError:
            logger.warning("Closing dialog, as no song found at index.")
            self.reject()
            return

        self.song_info: Song = song_info
        self._edit_widgets: dict[str, EditAbstractWidget] = {}
        self.setupUi()

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

        for tag in self._all_tags:
            widget = EditWidgetFactory.createWidget(
                tag.id3_key, self.song_info.getTag(tag.id3_key), self
            )
            if widget is not None:
                self._edit_widgets[tag.id3_key] = widget
                self.song_layout.addRow(tag.display_name, widget)
            # Needs to be a copy to avoid editing the tag prematurely.

        if not hasattr(self, "scroll_area"):
            self.scroll_area: QScrollArea = QScrollArea(self)
            self.scroll_area.setWidget(scroll_widget)
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setMinimumHeight(300)
            self.main_layout.addWidget(self.scroll_area)

        self.resize(600, 300)

    @override
    def updateSongInfo(self) -> None:
        """Update the data being stored in the song."""
        logger.debug("Called updateSong")
        any_updated = False
        for id3_key, widget in self._edit_widgets.items():
            if widget.isModified() or self.song_info.getTag(id3_key) != widget.value:
                any_updated = True
                new_value = widget.value
                self.song_info.setTag(id3_key, new_value)
        if any_updated:
            self.song_info.save()
            song_index = self.rows[self.current_index]
            self.info_updated.emit([song_index])

    def resetSongInfo(self) -> None:
        """Sets values for the song back to original ones before changes occurred."""
        for widget in self._edit_widgets.values():
            widget.reset()

    def _getSong(self) -> Song:
        """Gets the song based on the index of the list of indexes.

        Raises:
            IndexError if invalid index (no song at that row number).
        """
        row = self.rows[self.current_index]
        try:
            song_info = self.repository[row]
        except IndexError as err:
            raise IndexError from err
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
            logger.debug("Tried to go to next song on last, or previous song on first.")
            return
        match nav_direction:
            case NavDirection.Next:
                self.current_index += 1
            case NavDirection.Previous:
                self.current_index -= 1
        self.updateSongInfo()
        logger.debug(f"Called show song in direction with {nav_direction}")
        try:
            song_info = self._getSong()
        except IndexError:
            logger.warning("Invalid song, closing dialog")
            self.reject()
            return
        logger.debug("Got a song")

        self.song_info = song_info
        self._switchButtonState()
        self._setupSongInfo()
