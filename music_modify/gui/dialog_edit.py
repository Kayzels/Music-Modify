# pyright: reportPrivateImportUsage=false
import logging
from typing import cast

from mutagen.id3 import ID3TimeStamp

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types import Song, SongTag
from music_modify.custom_types.enums import TagType
from music_modify.prefs import prefs
from music_modify.utils import mapKey

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
            current_data = tag.getTag(self.song_info.id3)
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
        current_data: list[str] | list[ID3TimeStamp] | list[list[str]] | None,
    ) -> QWidget:
        if current_data is None:
            return QLineEdit()

        # Check that it's a tag that only allows a single value, put in LineEdit
        if not tag.allow_multiple and not isinstance(current_data[0], list):
            current_data = cast(list[str] | list[ID3TimeStamp], current_data)

            line_edit = QLineEdit(str(current_data[0]))
            line_edit.editingFinished.connect(
                lambda: self._setValueChange(
                    id3_key=tag.id3_key,
                    value=line_edit.text().strip()
                    if line_edit.text().strip() != ""
                    else None,
                )
            )
            return line_edit

        # Create container for non-LineEdit widgets, so we can add and remove rows, and move them.
        container_widget = QWidget()
        container_layout = QHBoxLayout()
        container_widget.setLayout(container_layout)
        container_layout.setContentsMargins(0, 0, 0, 0)

        button_layout = QVBoxLayout()

        up_button = QToolButton(container_widget)
        up_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp)))
        button_layout.addWidget(up_button)
        add_button = QToolButton(container_widget)
        add_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd)))
        button_layout.addWidget(add_button)
        remove_button = QToolButton(container_widget)
        remove_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove)))
        button_layout.addWidget(remove_button)
        down_button = QToolButton(container_widget)
        down_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown)))
        button_layout.addWidget(down_button)

        # A non-people tag that allows multiple values, create a ListWidget
        if tag.frame_type != TagType.People:
            current_data = cast(list[str], current_data)
            list_widget = QListWidget()
            for val in current_data:
                item = QListWidgetItem(val)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                list_widget.addItem(item)

            def setListChanges():
                # PERF: Need to iterate through because there might be new values.
                # Is there a way to prevent needing to do this?
                values: list[str] = []
                for row in range(list_widget.count()):
                    item = list_widget.item(row)
                    values.append(item.text())
                self._setValueChange(tag.id3_key, values)

            list_widget.itemChanged.connect(setListChanges)

            # TODO: Connect the buttons to slots for list widget

            container_layout.addWidget(list_widget)
            container_layout.addLayout(button_layout)

            return container_widget

        # If this far, it must be a people list, so put in table.
        current_data = cast(list[list[str]], current_data)
        table = QTableWidget()
        table.setColumnCount(2)  # Role, Person
        table.setHorizontalHeaderLabels(["Role", "Person"])  # pyright: ignore[reportUnknownMemberType]
        table.setRowCount(len(current_data))

        def setTableChanges():
            # PERF: Find way to avoid needing to rebuild the list on each change
            values: list[list[str]] = []
            for row in range(table.rowCount()):
                current_value: list[str] = []
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item is not None:
                        val = item.text()
                        current_value.append(val)
                if len(current_value) > 0:
                    values.append(current_value)
            self._setValueChange(tag.id3_key, values)

        for row_count, (role, person) in enumerate(current_data):
            table.setItem(row_count, 0, QTableWidgetItem(role))
            table.setItem(row_count, 1, QTableWidgetItem(person))
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        table.itemChanged.connect(setTableChanges)

        # TODO: Connect the buttons to slots for table widget

        container_layout.addWidget(table)
        container_layout.addLayout(button_layout)

        return container_widget

    def _setValueChange(
        self, id3_key: str, value: str | list[str] | list[list[str]] | None
    ) -> None:
        """Records the change if it's different from the original value, else removes it."""
        # Remove unneeded ones from change list
        logger.info(f"Called set value change with {id3_key} and {value}")

        key = mapKey(id3_key)
        if key is None:
            return
        tag = key.getTag(self.song_info.id3)

        if tag is None:
            if value is None:
                return
            else:
                self.changed_values[id3_key] = value
                return

        self.changed_values[id3_key] = value

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
