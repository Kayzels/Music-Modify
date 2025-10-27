"""Module that defines a dialog that displays a way for remapping a name in all tags."""

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types import Song, TagInfo
from music_modify.custom_types.tag_value import PairedTextTagValue, TextTagValue
from music_modify.models import SongRepository

if TYPE_CHECKING:
    from music_modify.custom_types.tag_value import AbstractTagValue

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DialogRemap(QDialog):
    """Dialog that displays a way for remapping a name in all tags."""

    songs_updated: Signal = Signal(list)
    """Signal that is emitted after the songs are updated.
    Emits a list of the repo indexes as ints."""

    def __init__(
        self,
        repository: SongRepository,
        rows: list[int],
        person_tags: list[TagInfo],
        parent: QWidget | None = None,
    ) -> None:
        """Creates a dialog for remapping names in all tags.

        Args:
            parent: The widget that the dialog should be displayed on.
            repository: The list of songs being managed by the app.
            rows: The indexes of the songs to be edited in the `repository`.
            person_tags: Tags that contain people values that may need to be remapped.
        """
        super().__init__(parent)
        self.setModal(True)
        self.setMinimumWidth(300)

        self.repository: SongRepository = repository
        "The list of songs that is currently being managed."
        self.rows: list[int] = rows
        "The indexes of the songs to edit, from the repository."
        self._person_tags: list[TagInfo] = person_tags

        self.setWindowTitle("Remapping Names")
        self.setupUi()

    def setupUi(self) -> None:
        """Sets up the basic user interface for the dialog."""
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.original_line_edit = QLineEdit(self)
        form_layout.addRow("Original Name", self.original_line_edit)
        self.new_line_edit = QLineEdit(self)
        form_layout.addRow("New Name", self.new_line_edit)

        main_layout.addLayout(form_layout)

        button_box = QDialogButtonBox(self)
        button_box.setOrientation(Qt.Orientation.Horizontal)
        button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        button_box.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(
            self.accept
        )
        button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
            self.reject
        )

        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def _getSongs(self) -> list[Song]:
        songs: list[Song] = []
        for index in self.rows:
            try:
                song = self.repository[index]
                songs.append(song)
            except IndexError:
                logger.warning(f"Tried to get a song at an invalid index: {index}")
        return songs

    @staticmethod
    def _processTags(
        song: Song,
        tag: TagInfo,
        original_name: str,
        new_name: str,
        updated_songs: set[Song],
    ) -> set[Song]:
        current_data: AbstractTagValue | None = song.getTag(tag.id3_key)
        updated_tag_value = False
        match current_data:
            case None:
                return updated_songs
            case TextTagValue():
                text_values: list[str] = current_data.value
                for i, current in enumerate(text_values):
                    if current == original_name:
                        text_values[i] = new_name
                        updated_tag_value = True
                if updated_tag_value:
                    song.setTag(tag.id3_key, TextTagValue(text_values))
                    updated_songs.add(song)
            case PairedTextTagValue():
                pair_values: list[list[str]] = current_data.value
                for i, pair in enumerate(pair_values):
                    _, person = pair
                    if person == original_name:
                        pair_values[i][1] = new_name
                        updated_tag_value = True
                if updated_tag_value:
                    song.setTag(tag.id3_key, PairedTextTagValue(pair_values))
                    updated_songs.add(song)
            case _:
                logger.warning("Unsupported tag value type for remapping.")

        return updated_songs

    def updateSongs(self) -> None:
        """Update the selected songs to remap the values."""
        original_name = self.original_line_edit.text()
        new_name = self.new_line_edit.text()
        if not original_name or not new_name:
            logger.info("One of the update values was empty.")
            return
        songs = self._getSongs()

        updated_songs: set[Song] = set()
        for song in songs:
            for tag in self._person_tags:
                updated_songs = self._processTags(
                    song, tag, original_name, new_name, updated_songs
                )

        if updated_songs:
            updated_indexes: list[int] = [
                self.repository.index(song) for song in updated_songs
            ]
            for song in updated_songs:
                song.save()
            self.songs_updated.emit(updated_indexes)
