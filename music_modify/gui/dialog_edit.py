# pyright: reportPrivateImportUsage=false
import logging
from typing import cast

from mutagen.id3 import ID3TimeStamp

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QListWidget,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types import Song, SongTag
from music_modify.custom_types.enums import TagType
from music_modify.prefs import prefs

logger = logging.getLogger(__name__)


class EditDialog(QDialog):
    def __init__(self, song_info: Song, parent: QWidget | None = None):
        super().__init__(parent)
        self.song_info: Song = song_info
        self.setupUi()

        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(
            self.reject
        )

    def setupUi(self):
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
            current_data = tag.getTag(self.song_info.id3)
            widget = self._createWidgetType(tag, current_data)
            self.song_layout.addRow(tag.display_name, widget)

        self.scroll_area: QScrollArea = QScrollArea(self)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(300)
        self.main_layout.addWidget(self.scroll_area)

        self.resize(300, 300)

    def _createWidgetType(
        self,
        tag: SongTag,
        current_data: list[str] | list[ID3TimeStamp] | list[list[str]] | None,
    ) -> QWidget:
        if current_data is None:
            return QLineEdit()

        # Check that it's a tag that only allows a single value, put in LineEdit
        if not tag.allow_multiple and not isinstance(current_data[0], list):
            current_data = cast(list[str] | list[ID3TimeStamp], current_data)
            return QLineEdit(str(current_data[0]))

        # A non-people tag that allows multiple values, create a ListWidget
        if tag.frame_type != TagType.People:
            current_data = cast(list[str], current_data)
            list_widget = QListWidget()
            for val in current_data:
                # logger.info(val)
                list_widget.addItem(val)
            return list_widget

        # If this far, it must be a people list, so put in table.
        current_data = cast(list[list[str]], current_data)
        table = QTableWidget()
        table.setColumnCount(2)  # Role, Person
        table.setHorizontalHeaderLabels(["Role", "Person"])  # pyright: ignore[reportUnknownMemberType]
        table.setRowCount(len(current_data))

        for row_count, (role, person) in enumerate(current_data):
            table.setItem(row_count, 0, QTableWidgetItem(role))
            table.setItem(row_count, 1, QTableWidgetItem(person))
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        return table
