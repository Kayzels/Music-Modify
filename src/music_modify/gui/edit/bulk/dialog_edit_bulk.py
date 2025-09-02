"""Module that defines an EditBulkDialog.

This dialog allows editing the tags of multiple songs at the same time.
"""

import copy
import logging
from typing import TYPE_CHECKING, cast, override

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types.enums import EditorType
from music_modify.gui.edit.dialog_edit_abstract import EditAbstractDialog
from music_modify.gui.utils import createTab
from music_modify.models.song_repository import SongRepository
from music_modify.prefs import prefs
from music_modify.utils.list_utils import addValues

from .widget_edit_bulk_abstract import EditBulkAbstractWidget
from .widget_edit_bulk_line import EditBulkLineWidget
from .widget_edit_bulk_multiple import EditBulkMultipleWidget
from .widget_edit_bulk_people import EditBulkPeopleWidget

if TYPE_CHECKING:
    from music_modify.custom_types.song import Song
    from music_modify.custom_types.songtag import SongTag

logger = logging.getLogger(__name__)


def _addMultiValues[T](
    value: list[T] | None,
    existing: set[T],
) -> set[T]:
    """Add the values from the list to the set, if not present."""
    if value is None:
        return existing
    for item in value:
        existing.add(item)
    return existing


def _addSingleValues(
    value: str | None,
    existing: set[str],
    *,
    in_all: bool = True,
) -> tuple[set[str], bool]:
    """Finds the values in all tags, and whether it appears in every song.

    Populates `existing` with the values that are not present,
    and returns a tuple that has the values, and whether the value
    was in every song or not.
    """
    if value is None:
        return existing, False
    if len(existing) > 0 and value not in existing:
        in_all = False
    existing.add(value)
    return existing, in_all


class EditBulkDialog(EditAbstractDialog):
    """A dialog that allows editing the tags of multiple songs at the same time."""

    info_updated: Signal = Signal()
    "Signal that should be emitted whenever data changes in any of the fields."

    def __init__(
        self,
        parent: QWidget,
        repository: SongRepository,
        rows: list[int],
    ) -> None:
        """Create a dialog for bulk editing songs.

        Args:
            parent: The widget that the dialog should be displayed on
            repository: The list of songs being managed
            rows: The indexes of the songs to edit, in the `repository`
        """
        super().__init__(parent, repository, rows)

        if len(rows) == 0:
            self.reject()
            return

        self.songs: list[Song] = []
        "The list of song objects that should be changed."
        for index in rows:
            song = repository[index]
            if song is not None:
                self.songs.append(song)

        self.setWindowTitle(f"Bulk editing {len(self.songs)} songs")

        self.setupUi()

    @override
    def _setupSongInfo(self) -> None:
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

        people_values: dict[SongTag, list[list[str]]] = {}
        normal_values: dict[SongTag, set[str]] = {}

        for tag in prefs.settings.all_tags:
            # Get values from all songs, and store in dicts
            in_all: bool = True
            for song in self.songs:
                current_data = copy.deepcopy(tag.getValue(song.id3))
                match tag.editor_type:
                    case EditorType.PeopleValue:
                        people_values[tag] = addValues(
                            cast(list[list[str]] | None, current_data),
                            people_values.get(tag, []),
                        )
                    case EditorType.MultipleText:
                        normal_values[tag] = _addMultiValues(
                            cast(list[str] | None, current_data),
                            normal_values.get(tag, set()),
                        )
                    case EditorType.SingleText:
                        normal_values[tag], in_all = _addSingleValues(
                            cast(str | None, current_data),
                            normal_values.get(tag, set()),
                            in_all=in_all,
                        )
                    case _:
                        logger.warning(
                            f"editor_type had an unsupported value: {tag.editor_type}"
                        )

            # Create widgets and add to layouts
            match tag.editor_type:
                case EditorType.PeopleValue:
                    people_widget_layout.addWidget(
                        EditBulkPeopleWidget(
                            self,
                            people_values.get(tag, []),
                            tag,
                        ),
                    )
                case EditorType.MultipleText:
                    multi_widget_layout.addWidget(
                        EditBulkMultipleWidget(
                            self, normal_values.get(tag, set()), tag
                        ),
                    )
                case EditorType.SingleText:
                    simple_widget_form_layout.addRow(
                        tag.display_name,
                        EditBulkLineWidget(
                            self,
                            normal_values.get(tag, set()),
                            tag,
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
            for song in updated_songs:
                song.save()
            self.info_updated.emit()
