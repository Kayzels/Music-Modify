# pyright: reportPrivateImportUsage=false, reportUnusedCallResult=false
import copy
import logging

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
from music_modify.gui.widget_edit_factory import EditWidgetFactory
from music_modify.prefs import prefs

# from .widget_edit import EditWidget


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
        widget = EditWidgetFactory.createWidget(self, tag, data)

        @Slot()
        def updateValue():
            self.changed_values[tag.id3_key] = widget.value
            logger.info(f"Value is {widget.value}")
            logger.info(f"Changed values are {self.changed_values}")
            # self._setValueChange(tag.id3_key, widget.value)

        @Slot()
        def clearValue():
            self.changed_values.pop(tag.id3_key, None)
            # self._removeValueChange(tag.id3_key)
            logger.info(
                f"Removed value for key {tag.id3_key}, changed values are now {self.changed_values}"
            )

        widget.value_updated.connect(updateValue)
        widget.value_reset.connect(clearValue)

        return widget

    def updateSong(self) -> None:
        """Adds the changes to the song, and saves it."""
        raise NotImplementedError

    # TODO: Check whether all the deepcopy's are needed.
