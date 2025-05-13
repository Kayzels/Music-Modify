# pyright: reportUnusedCallResult=false
import copy
import logging

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types import Song, SongTag
from music_modify.custom_types.aliases import SongEditData, SongGroupData
from music_modify.custom_types.utils import mapKey
from music_modify.prefs import prefs

from .widget_edit_abstract import EditAbstractWidget
from .widget_edit_factory import EditWidgetFactory

logger = logging.getLogger(__name__)


class EditDialog(QDialog):
    info_updated: Signal = Signal()

    def __init__(self, song_info: Song, parent: QWidget | None = None):
        super().__init__(parent)
        self.song_info: Song = song_info
        self.setupUi(self)

        self.changed_values: dict[str, SongEditData | None] = {}

        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
            self.reject
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(
            self.accept
        )

        # Update the song, but keep the dialog open
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self.updateSong
        )

        self.button_box.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(
            self.resetSong
        )

        self.song_layout: QFormLayout

    def setupUi(self, EditDialog: "EditDialog"):  # pyright: ignore[reportUnusedParameter]
        # The EditDialog parameter is not used,
        # but exists to match the uic generated ones.
        # Will make it easier to abstract it later.
        self.main_layout: QVBoxLayout = QVBoxLayout(self)

        self._setupSongInfo()

        self.button_box: QDialogButtonBox = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
            | QDialogButtonBox.StandardButton.Reset
        )

        self.main_layout.addWidget(self.button_box)

        self.setLayout(self.main_layout)

    def _setupSongInfo(self):
        scroll_widget: QWidget = QWidget()
        self.song_layout = QFormLayout(scroll_widget)

        for tag in prefs.settings.all_tags:
            current_data = copy.deepcopy(tag.getTag(self.song_info.id3))
            widget = self._createWidgetType(tag, current_data)
            self.song_layout.addRow(tag.display_name, widget)

        scroll_area: QScrollArea = QScrollArea(self)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(300)
        self.main_layout.addWidget(scroll_area)

        self.resize(600, 300)

    def _createWidgetType(self, tag: SongTag, data: SongGroupData) -> QWidget:
        widget = EditWidgetFactory.createWidget(self, tag, data)

        @Slot()
        def updateValue():
            # We want to remove values if they are empty,
            # which is marked by making the changed_value for that key None.
            value = widget.value
            if len(value) == 0:
                value = None
            self.changed_values[tag.id3_key] = value
            logger.info(f"Value is {widget.value}")
            logger.info(f"Changed values are {self.changed_values}")

        @Slot()
        def resetValue() -> None:
            """Clears the value if it's the same as the original, and that value is stored in the song.
            Otherwise stores the change."""
            # This is needed because after a user clicks Apply, the value stored in the song
            # is now no longer the same as the original, so we can't just clear it.
            value = widget.value

            # Need to get the value inside the song and compare
            song_value = tag.getValue(self.song_info.id3)
            if song_value is None and len(value) != 0:
                # The value in the song was cleared, but we have a value now that isn't
                logger.info(
                    f"Value for key {tag.id3_key} previously removed, but being reset now."
                )
                self.changed_values[tag.id3_key] = value
                logger.info(f"Changed values are now {self.changed_values}")
            elif song_value is None and len(value) == 0:
                # Same empty value, no need to remember
                logger.info(
                    f"Song doesn't store the key {tag.id3_key} and the value for it is being set to empty."
                )
                self.changed_values.pop(tag.id3_key, None)
                logger.info(f"Changed values are now {self.changed_values}")
            elif song_value != value:
                # New value than what is stored in the song (same as original value)
                logger.info(
                    f"Value stored in song for key {tag.id3_key} is different from the value being reset to, so storing."
                )
                if len(value) == 0:
                    self.changed_values[tag.id3_key] = None
                else:
                    self.changed_values[tag.id3_key] = value
                logger.info(f"Changed values are now {self.changed_values}")
            else:
                # Value matches existing song value, remove from change list.
                logger.info(
                    f"Value matches the value in the song for {tag.id3_key}, so removing from changed values."
                )
                self.changed_values.pop(tag.id3_key, None)
                logger.info(f"Changed values are now {self.changed_values}")

        widget.value_updated.connect(updateValue)
        widget.value_reset.connect(resetValue)

        return widget

    def updateSong(self) -> None:
        """Adds the changes to the song, and saves it."""
        if len(self.changed_values) == 0:
            return
        logger.info("Called updateSong")
        for id3_key, value in self.changed_values.items():
            tag = mapKey(id3_key)
            if tag is None:
                logger.info(f"Unknown id3 key: {id3_key}")
                continue
            if value is None:
                # Remove tag from song
                logger.info(f"Value was None, so removing key {id3_key}")
                tag.removeTag(self.song_info.id3)
                continue

            # Mutagen ID3 frames always store their values in a list,
            # so need to convert to that format.
            if isinstance(value, str):
                value = [value]
            logger.info(f"Setting tag for {id3_key} to {value}")
            tag.setTag(self.song_info.id3, value)
        self.song_info.save()
        self.info_updated.emit()

        # Clear the values: they've been changed in the song,
        # so don't need to be stored in this list any more
        self.changed_values = {}

        # TODO: Consider how this impacts refresh and reset
        # The widgets all contain the current values,
        # and the original values for the field.
        # But if it's updated multiple times, reset can go out of sync?

    def resetSong(self) -> None:
        """Sets the values for the song back to the original ones before the changes occurred."""
        widgets = self.findChildren(EditAbstractWidget)
        for widget in widgets:
            widget.reset()
