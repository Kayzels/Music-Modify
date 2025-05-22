import copy
import logging
from typing import cast, override

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types.enums import TagType
from music_modify.custom_types.song import Song
from music_modify.gui.edit.dialog_edit_abstract import EditAbstractDialog
from music_modify.models.song_repository import SongRepository
from music_modify.prefs import prefs

from .widget_edit_bulk_abstract import EditBulkAbstractWidget
from .widget_edit_bulk_line import EditBulkLineWidget
from .widget_edit_bulk_multiple import EditBulkMultipleWidget
from .widget_edit_bulk_people import EditBulkPeopleWidget

logger = logging.getLogger(__name__)


class EditBulkDialog(EditAbstractDialog):
    """A dialog that allows editing the tags of multiple songs at the same time."""

    info_updated: Signal = Signal()

    def __init__(
        self, parent: QWidget, repository: SongRepository, rows: list[int]
    ) -> None:
        super().__init__(parent, repository, rows)

        self.songs: list[Song] = [
            song for index in rows if (song := repository.getSong(index)) is not None
        ]

        self.setWindowTitle(f"Bulk editing {len(self.songs)} songs")

        self.setupUi()

    @override
    def _setupSongInfo(self) -> None:
        self.tab_widget: QTabWidget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        simple_page = QWidget()
        multiple_page = QWidget()
        people_page = QWidget()

        simple_widget_form_layout = QFormLayout()
        simple_page.setLayout(simple_widget_form_layout)
        simple_scroll_area = QScrollArea()
        simple_scroll_area.setWidgetResizable(True)
        simple_scroll_area.setWidget(simple_page)
        self.tab_widget.addTab(simple_scroll_area, "Simple Tags")

        multi_widget_layout = QVBoxLayout()
        multiple_page.setLayout(multi_widget_layout)
        multi_scroll_area = QScrollArea()
        multi_scroll_area.setWidgetResizable(True)
        multi_scroll_area.setWidget(multiple_page)
        self.tab_widget.addTab(multi_scroll_area, "List Tags")

        people_widget_layout = QVBoxLayout()
        people_page.setLayout(people_widget_layout)
        people_scroll_area = QScrollArea()
        people_scroll_area.setWidgetResizable(True)
        people_scroll_area.setWidget(people_page)
        self.tab_widget.addTab(people_scroll_area, "People Tags")

        for tag in prefs.settings.all_tags:
            if tag.frame_type == TagType.People:
                items: list[list[str]] = []
                for song in self.songs:
                    current_data = copy.deepcopy(tag.getValue(song.id3))
                    if current_data is not None:
                        current_data = cast(list[list[str]], current_data)
                        for item in current_data:
                            if item not in items:
                                items.append(item)
                widget = EditBulkPeopleWidget(self, items, tag)
                people_widget_layout.addWidget(widget)
            elif tag.allow_multiple:
                tag_items: set[str] = set()
                for song in self.songs:
                    current_data = copy.deepcopy(tag.getValue(song.id3))
                    if current_data is not None:
                        current_data = cast(list[str], current_data)
                        for item in current_data:
                            tag_items.add(item)
                widget = EditBulkMultipleWidget(self, tag_items, tag)
                multi_widget_layout.addWidget(widget)
            else:
                tag_items = set()
                in_all: bool = True
                for song in self.songs:
                    current_data = copy.deepcopy(tag.getValue(song.id3))
                    if current_data is not None:
                        current_data = cast(str, current_data)
                        if len(tag_items) > 0 and current_data not in tag_items:
                            in_all = False
                        tag_items.add(current_data)
                    else:
                        in_all = False
                widget = EditBulkLineWidget(self, tag_items, tag=tag, in_all=in_all)
                simple_widget_form_layout.addRow(tag.display_name, widget)

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
        return


# PERF: Reset after calling Apply, so not doing the change twice?
# TODO: Should redraw after Apply, to reflect new values
