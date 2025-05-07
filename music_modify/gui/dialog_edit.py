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
        scroll_widget: QWidget = QWidget()
        song_layout: QFormLayout = QFormLayout(scroll_widget)

        for tag in prefs.settings.all_tags:
            current_data = copy.deepcopy(tag.getTag(self.song_info.id3))
            widget = self._createWidgetType(tag, current_data)
            song_layout.addRow(tag.display_name, widget)

        scroll_area: QScrollArea = QScrollArea(self)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(300)
        self.main_layout.addWidget(scroll_area)

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

        @Slot()
        def clearValue():
            logger.info(f"Removing value for key {tag.id3_key}")
            self._removeValueChange(tag.id3_key)

        # Line updated should only be emitted by the LineEdit, for single values
        # But group updated emitted when a list widget or table is updated
        # Either way, we just pass the information through to _setValueChange
        widget.line_updated.connect(updateValue)
        widget.group_updated.connect(updateValue)

        widget.value_reset.connect(clearValue)

        return widget

    def _setValueChange(
        self, id3_key: str, value: str | list[str] | list[list[str]] | None
    ) -> None:
        """Records changes made to values in the song for a specific key."""
        self.changed_values[id3_key] = value
        logger.info(f"Changed values are {self.changed_values}")

    def _removeValueChange(self, id3_key: str):
        self.changed_values.pop(id3_key, None)
        logger.info(
            f"Removing value for {id3_key}, changed values are now {self.changed_values}"
        )

    def updateSong(self) -> None:
        """Adds the changes to the song, and saves it."""
        raise NotImplementedError

    # TODO: Check whether all the deepcopy's are needed.
