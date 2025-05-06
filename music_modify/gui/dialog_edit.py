# pyright: reportPrivateImportUsage=false, reportUnusedCallResult=false
import copy
import logging
from typing import cast

from mutagen.id3 import ID3TimeStamp

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types import Song, SongTag
from music_modify.custom_types.enums import TagType, WidgetType
from music_modify.prefs import prefs
from music_modify.utils import mapKey

from .widget_edit import EditWidget


logger = logging.getLogger(__name__)


class EditDialog(QDialog):
    def __init__(self, song_info: Song, parent: QWidget | None = None):
        super().__init__(parent)
        self.song_info: Song = song_info
        self.setupUi(self)

        self.changed_values: dict[str, str | list[str] | list[list[str]] | None] = {}

        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
            self.reject
        )

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
        self.scroll_widget: QWidget = QWidget()
        self.song_layout: QFormLayout = QFormLayout(self.scroll_widget)

        for tag in prefs.settings.all_tags:
            current_data = copy.deepcopy(tag.getTag(self.song_info.id3))
            widget = self._createWidgetType(tag, current_data)
            self.song_layout.addRow(tag.display_name, widget)

        self.scroll_area: QScrollArea = QScrollArea(self)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(300)
        self.main_layout.addWidget(self.scroll_area)

        self.resize(600, 300)

    def _createWidgetType(
        self,
        tag: SongTag,
        data: list[str] | list[ID3TimeStamp] | list[list[str]] | None,
    ) -> QWidget:
        group: tuple[TagType, bool] = (tag.frame_type, tag.allow_multiple)

        match group:
            case (TagType.People, _):
                # Is a people tag, so table with current data
                widget_type = WidgetType.Table
            case (_, True):
                # Allow multiple is true, so list with current data
                widget_type = WidgetType.List
                if data is not None:
                    # Send a copy otherwise when checking if a value is changed,
                    # it will always be false, because it's comparing the two
                    # changed values
                    data = cast(list[str], data).copy()
            case (_, False):
                # Only allows a single value, which can be a string, ID3TimeStamp or None.
                # Show in LineEdit.
                widget_type = WidgetType.String
                if data is not None:
                    data = copy.deepcopy(cast(list[list[str]], data))
                    # data = cast(list[list[str]], data).copy()

        widget = EditWidget(self, widget_type, data)

        @Slot(str)
        @Slot(list)
        def updateValue(info: str | list[str] | list[list[str]]):
            logger.info(f"Info is {info}")
            self._setValueChange(tag.id3_key, info)

        # Line updated should only be emitted by the LineEdit, for single values
        # But group updated emitted when a list widget or table is updated
        # Either way, we just pass the information through to _setValueChange
        widget.line_updated.connect(updateValue)
        widget.group_updated.connect(updateValue)

        return widget

    def _setValueChange(
        self, id3_key: str, value: str | list[str] | list[list[str]] | None
    ) -> None:
        """Records the change if it's different from the original value, else removes it."""
        # Remove unneeded ones from change list
        logger.info(f"Called set value change with {id3_key} and {value}")

        key = mapKey(id3_key)
        if key is None:
            return
        tag = copy.deepcopy(key.getTag(self.song_info.id3))

        if tag is None:
            if value is None:
                return
            else:
                self.changed_values[id3_key] = value
                return

        self.changed_values[id3_key] = value
        logger.info(f"Changed values before processing are {self.changed_values}")

        if value is None:
            # We've set the value for the id3_key above to None,
            # nothing more to do, so return
            return

        if isinstance(value, str):
            # If the value is a string, we know the tag stores a single string or ID3TimeStamp.
            if str(tag[0]) == value:
                self.changed_values.pop(id3_key, None)
                logger.info(
                    f"Removed changed value for {id3_key}, changed values are now {self.changed_values}"
                )
            return

        # We know that it's a list at this point, because it's not None or a string
        if len(value) == 0:
            # List with no values, so key should be deleted from song later
            self.changed_values[id3_key] = None
            logger.info(f"List containing no values sent for {id3_key}, set to None")
            return
        if isinstance(value[0], str):
            # Tag stores a list of strings, check if identical.
            # If order or length is different, must add.
            value = cast(list[str], value)
            if len(tag) == len(value):
                should_change = False
                for i in range(len(tag)):
                    if tag[i] != value[i]:
                        should_change = True
                if not should_change:
                    self.changed_values.pop(id3_key, None)
                    logger.info(
                        f"Removed changed value for {id3_key}, changed values are now {self.changed_values}"
                    )
                    return
            logger.info(f"Changed values are {self.changed_values}")
        else:
            # Tag stores a people list. Check if identical.
            # If any values differ or length is different, must add.
            value = cast(list[list[str]], value)
            tag = cast(list[list[str]], tag)
            if len(tag) == len(value):
                should_change = False
                for i in range(len(tag)):
                    for j in range(1):
                        if tag[i][j] != value[i][j]:
                            should_change = True
                if not should_change:
                    self.changed_values.pop(id3_key, None)
                    logger.info(
                        f"Removed changed value for {id3_key}, changed values are now {self.changed_values}"
                    )
                    return
            logger.info(f"Changed values are {self.changed_values}")

    def updateSong(self) -> None:
        """Adds the changes to the song, and saves it."""
        raise NotImplementedError

    # TODO: Check whether all the deepcopy's are needed.
