"""Module that defines the dialog that allows
editing the tags of multiple songs at the same time."""

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

from music_modify.custom_types.enums import TagType
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
    """Get the values that appear for all single tag values,
    and whether the value appears in every song, or not."""
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
        super().__init__(parent, repository, rows)

        self.songs: list[Song] = [
            song for index in rows if (song := repository.getSong(index)) is not None
        ]
        "The list of song objects that should be changed."

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
                if tag.frame_type == TagType.People:
                    people_values[tag] = addValues(
                        cast(list[list[str]] | None, current_data),
                        people_values.get(tag, []),
                    )
                    continue
                if tag.allow_multiple:
                    normal_values[tag] = _addMultiValues(
                        cast(list[str] | None, current_data),
                        normal_values.get(tag, set()),
                    )
                    continue
                normal_values[tag], in_all = _addSingleValues(
                    cast(str | None, current_data),
                    normal_values.get(tag, set()),
                    in_all=in_all,
                )

            # Create widgets and add to layouts
            if tag.frame_type == TagType.People:
                people_widget_layout.addWidget(
                    EditBulkPeopleWidget(
                        self,
                        people_values[tag],
                        tag,
                    ),
                )
                continue
            if tag.allow_multiple:
                multi_widget_layout.addWidget(
                    EditBulkMultipleWidget(self, normal_values[tag], tag),
                )
                continue
            simple_widget_form_layout.addRow(
                tag.display_name,
                EditBulkLineWidget(
                    self,
                    normal_values[tag],
                    tag,
                    in_all=in_all,
                ),
            )

        self.resize(600, 400)

    @override
    def updateSongInfo(self) -> None:
        """Update all selected songs to have the changed data."""

        changed: bool = False
        widgets = self.findChildren(EditBulkAbstractWidget)
        for widget in widgets:
            # Needs to be in this order to avoid short-circuiting if an earlier
            # tag has changed.
            changed = widget.updateTag(self.songs) or changed
        if changed:
            for song in self.songs:
                song.save()
            self.info_updated.emit()
