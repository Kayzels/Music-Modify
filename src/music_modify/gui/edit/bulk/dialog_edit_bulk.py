"""Module that defines an EditBulkDialog.

This dialog allows editing the tags of multiple songs at the same time.
"""

import logging
from typing import TYPE_CHECKING, cast, override

from PySide6.QtWidgets import (
    QFormLayout,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from music_modify.core.enums import EditorType
from music_modify.custom_types import TagInfo
from music_modify.custom_types.tag_value import PairedTextTagValue, TextTagValue
from music_modify.gui.edit.dialog_edit_abstract import EditAbstractDialog
from music_modify.gui.utils import createTab
from music_modify.models.song_repository import SongRepository
from music_modify.utils.list_utils import addItemsFromList, addItemsWithCheck, addValues

from .widget_edit_bulk_abstract import EditBulkAbstractWidget
from .widget_edit_bulk_line import EditBulkLineWidget
from .widget_edit_bulk_multiple import EditBulkMultipleWidget
from .widget_edit_bulk_people import EditBulkPeopleWidget

if TYPE_CHECKING:
    from music_modify.custom_types.song import Song

logger = logging.getLogger(__name__)


class EditBulkDialog(EditAbstractDialog):
    """A dialog that allows editing the tags of multiple songs at the same time."""

    def __init__(
        self,
        repository: SongRepository,
        rows: list[int],
        all_tags: list[TagInfo],
        parent: QWidget | None = None,
    ) -> None:
        """Create a dialog for bulk editing songs.

        Args:
            parent: The widget that the dialog should be displayed on
            repository: The list of songs being managed
            rows: The indexes of the songs to edit, in the `repository`
            all_tags: Tags that are available for reading and editing
        """
        super().__init__(repository, rows, parent)

        self._all_tags: list[TagInfo] = all_tags

        if len(rows) == 0:
            self.reject()
            return

        self.songs: list[Song] = []
        "The list of song objects that should be changed."
        for index in rows:
            try:
                song = repository[index]
                self.songs.append(song)
            except IndexError:
                logger.warning(f"Tried to get a song at an invalid index: {index}")

        self.setWindowTitle(f"Bulk editing {len(self.songs)} songs")

        self.setupUi()

    @override
    def _setupSongInfo(self) -> None:  # noqa: PLR0912
        self.tab_widget: QTabWidget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        simple_widget_form_layout = cast(
            QFormLayout,
            createTab(
                "Simple Tags",
                self.tab_widget,
                QFormLayout,
            ),
        )

        multi_widget_layout = createTab(
            "List Tags",
            self.tab_widget,
            QVBoxLayout,
        )

        people_widget_layout = createTab(
            "People Tags",
            self.tab_widget,
            QVBoxLayout,
        )

        people_values: dict[str, list[list[str]]] = {}
        normal_values: dict[str, set[str]] = {}

        for tag in self._all_tags:
            # Get values from all songs, and store in dicts
            in_all: bool = True
            for song in self.songs:
                current_data = song.getTag(tag.id3_key)
                if current_data is None:
                    if tag.editor_type == EditorType.PeopleValue:
                        current_data = PairedTextTagValue([])
                    else:
                        current_data = TextTagValue([])
                match current_data, tag.editor_type:
                    case PairedTextTagValue(), _:
                        people_values[tag.id3_key] = addValues(
                            current_data.value, people_values.get(tag.id3_key, [])
                        )
                    case TextTagValue(), EditorType.MultipleText:
                        # noinspection PyTypeChecker
                        normal_values[tag.id3_key] = addItemsFromList(
                            current_data.value, normal_values.get(tag.id3_key, set())
                        )
                    case TextTagValue(), EditorType.SingleText:
                        normal_values[tag.id3_key], in_all = addItemsWithCheck(
                            current_data.getDisplayValue(),
                            normal_values.get(tag.id3_key, set()),
                            in_all=in_all,
                        )
                    case _:
                        logger.warning(
                            "Unsupported editor type or tag value. "
                            + f"Editor type: {tag.editor_type}. "
                            + f"Tag Value: {type(current_data)}."
                        )

            # Create widgets and add to layouts
            match tag.editor_type:
                case EditorType.PeopleValue:
                    people_widget_layout.addWidget(
                        EditBulkPeopleWidget(
                            people_values.get(tag.id3_key, []),
                            tag,
                            self,
                        ),
                    )
                case EditorType.MultipleText:
                    multi_widget_layout.addWidget(
                        EditBulkMultipleWidget(
                            normal_values.get(tag.id3_key, set()),
                            tag,
                            self,
                        ),
                    )
                case EditorType.SingleText:
                    simple_widget_form_layout.addRow(
                        tag.display_name,
                        EditBulkLineWidget(
                            normal_values.get(tag.id3_key, set()),
                            tag,
                            self,
                            in_all=in_all,
                        ),
                    )
                case _:
                    pass

        self.resize(600, 400)

    @override
    def updateSongInfo(self) -> None:
        """Update all selected songs to have the changed data."""
        updated_songs: set[Song] = set()
        widgets = self.findChildren(EditBulkAbstractWidget)
        for widget in widgets:
            updated_songs = updated_songs | widget.updateTag(self.songs)
        if updated_songs:
            updated_indexes: list[int] = [
                self.repository.index(song) for song in updated_songs
            ]
            for song in updated_songs:
                song.save()
            self.info_updated.emit(updated_indexes)
