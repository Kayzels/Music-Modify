import logging
from abc import abstractmethod
from typing import Callable, cast, override

from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from music_modify.custom_types import Song, SongTag
from music_modify.gui.completion import EditWithComplete, createCompletionWidget
from music_modify.gui.meta import ABCQMeta

from .widget_edit_bulk_abstract_group import EditBulkAbstractGroupWidget

logger = logging.getLogger(__name__)

PAIR_SEPARATOR = ": "


class _AbstractPeopleWidget(QWidget, metaclass=ABCQMeta):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    @abstractmethod
    def reset(self):
        pass


class _PeopleTable(_AbstractPeopleWidget):
    def __init__(self, parent: QWidget, headers: list[str]):
        super().__init__(parent)
        self.headers: list[str] = headers

        self.setupUi()

    def setupUi(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Panel)
        frame.setLineWidth(1)
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(frame)
        layout.addLayout(frame_layout)

        self.table: QTableWidget = QTableWidget(1, len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        frame_layout.addWidget(self.table)

        # TODO: Need a way to add and remove rows

    @property
    def values(self) -> list[list[str]]:
        values: list[list[str]] = []
        for row in range(self.table.rowCount()):
            first = self.table.item(row, 0)
            if first is None:
                continue
            second = self.table.item(row, 1)
            if second is None:
                continue
            first_text = first.text().strip()
            second_text = second.text().strip()
            values.append([first_text, second_text])
        return values

    @override
    def reset(self):
        self.table.clearContents()
        self.table.setRowCount(1)


class _PeopleLine(_AbstractPeopleWidget):
    def __init__(self, parent: QWidget, data: list[str]):
        super().__init__(parent)

        self.widget: EditWithComplete = createCompletionWidget(self, tuple(data))
        self.setupUi()

    def setupUi(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.widget)
        self.setLayout(layout)

    @property
    def items(self) -> tuple[str, ...]:
        return tuple(self.widget.values)

    @items.setter
    def items(self, items: tuple[str, ...]):
        self.widget.updateItemsCache(items)

    @override
    def reset(self):
        self.widget.setText("")

    def pairs(self) -> list[list[str]]:
        values = self.items
        result: list[list[str]] = []
        for value in values:
            if not value.find(PAIR_SEPARATOR):
                continue
            parts = value.split(PAIR_SEPARATOR, 1)
            if len(parts) == 2:
                result.append(parts)
        return result


class EditBulkPeopleWidget(EditBulkAbstractGroupWidget):
    def __init__(self, parent: QWidget, data: list[list[str]], tag: SongTag):
        super().__init__(parent, tag)

        self.items: list[tuple[str, str]] = [(role, person) for role, person in data]
        self.setupUi()

        self.add_widget: _PeopleTable
        self.remove_pair_widget: _PeopleLine
        self.remove_role_widget: _PeopleLine
        self.remove_person_widget: _PeopleLine
        self.remap_role_widget: _PeopleTable
        self.remap_person_widget: _PeopleTable

    @override
    def createForm(self) -> QWidget:
        form_layout = QFormLayout()
        form_container: QWidget = QWidget()
        form_container.setLayout(form_layout)
        form_layout.setContentsMargins(0, 0, 0, 0)

        self.add_widget = _PeopleTable(self, ["Role", "Person"])
        form_layout.addRow("Add", self.add_widget)

        pairs = list(
            set([f"{role}{PAIR_SEPARATOR}{person}" for (role, person) in self.items])
        )
        self.remove_pair_widget = _PeopleLine(self, pairs)
        form_layout.addRow("Remove Pair", self.remove_pair_widget)

        roles = list(set([role for (role, _) in self.items]))
        self.remove_role_widget = _PeopleLine(self, roles)
        form_layout.addRow("Remove Role", self.remove_role_widget)

        people = list(set([person for (_, person) in self.items]))
        self.remove_person_widget = _PeopleLine(self, people)
        form_layout.addRow("Remove Person", self.remove_person_widget)

        remap_headers = ["Old", "New"]
        self.remap_role_widget = _PeopleTable(self, remap_headers)
        form_layout.addRow("Remap Role", self.remap_role_widget)

        self.remap_person_widget = _PeopleTable(self, remap_headers)
        form_layout.addRow("Remap Person", self.remap_person_widget)

        # TODO:Table Widget for reordering, with current data

        return form_container

    @override
    def _resetView(self):
        pairs = list(set([f"{role}: {person}" for (role, person) in self.items]))
        self.remove_pair_widget.items = tuple(pairs)

        roles = list(set([role for (role, _) in self.items]))
        self.remove_role_widget.items = tuple(roles)

        people = list(set([person for (_, person) in self.items]))
        self.remove_person_widget.items = tuple(people)

        widgets = self.findChildren(_AbstractPeopleWidget)
        for widget in widgets:
            widget.reset()

        self.clear_checkbox.setChecked(False)
        self.group_box.setChecked(False)

    @override
    def updateTag(self, songs: list[Song]) -> bool:
        if not self.group_box.isChecked():
            return False

        if self.clear_checkbox.isChecked():
            for song in songs:
                self.tag.removeTag(song.id3)
                song.save()
            self._resetView()
            return True

        # Collect all possible changes
        add_items: list[list[str]] = self.add_widget.values
        remove_pairs: list[list[str]] = self.remove_pair_widget.pairs()
        remove_people: tuple[str, ...] = self.remove_person_widget.items
        remove_roles: tuple[str, ...] = self.remove_role_widget.items
        map_people: list[list[str]] = self.remap_person_widget.values
        map_roles: list[list[str]] = self.remap_role_widget.values

        # If any of the above values aren't empty,
        # the user intends to make a change.
        change_attempted = any(
            [
                len(c) > 0
                for c in (
                    add_items,
                    remove_pairs,
                    remove_people,
                    remove_roles,
                    map_people,
                    map_roles,
                )
            ]
        )
        if not change_attempted:
            return False

        # Map to dicts so that it's quicker to get the changed values.
        people_replacements = {old: new for old, new in map_people}
        role_replacements = {old: new for old, new in map_roles}

        # Store whether any change is actually made.
        # Updated if a refresh is requested.
        changes_made: bool = False

        # For checking removal, use a set of tuple for matching
        remove_pairs_set: set[tuple[str, ...]] = {tuple(pair) for pair in remove_pairs}

        def _getSongValues(song: Song) -> list[list[str]]:
            original_values = self.tag.getValue(song.id3)
            if original_values is None:
                if not self.tag.hasTag(song.id3):
                    self.tag.generateFrame(song.id3)
                original_values = []
            original_values = cast(list[list[str]], original_values)
            return original_values

        def _performChange(
            song: Song, func: Callable[[list[list[str]]], list[list[str]]]
        ) -> bool:
            current_values = _getSongValues(song)
            new_values = func(current_values)

            if new_values != current_values:
                self.tag.setTag(song.id3, new_values)
                song.save()
                return True
            return False

        for song in songs:
            # Values in add_table
            if len(add_items) > 0:
                changes_made = (
                    _performChange(
                        song,
                        lambda vals: vals
                        + [item for item in add_items if item not in vals],
                    )
                    or changes_made
                )

            # Values in Remove Pair
            if len(remove_pairs) > 0:
                changes_made = (
                    _performChange(
                        song,
                        lambda vals: [
                            item for item in vals if tuple(item) not in remove_pairs_set
                        ],
                    )
                    or changes_made
                )

            # Values in Remove Person
            if len(remove_people) > 0:
                changes_made = (
                    _performChange(
                        song,
                        lambda vals: [
                            item
                            for item in vals
                            if len(item) == 2 and item[1] not in remove_people
                        ],
                    )
                    or changes_made
                )

            # Values in Remove Role
            if len(remove_roles) > 0:
                changes_made = (
                    _performChange(
                        song,
                        lambda vals: [
                            item
                            for item in vals
                            if len(item) == 2 and item[0] not in remove_roles
                        ],
                    )
                    or changes_made
                )

            # Values in Remap People
            if len(map_people) > 0:
                changes_made = (
                    _performChange(
                        song,
                        lambda vals: [
                            [item[0], people_replacements.get(item[1], item[1])]
                            for item in vals
                            if len(item) == 2
                        ],
                    )
                    or changes_made
                )

            # Values in Remap Roles
            if len(map_roles) > 0:
                changes_made = (
                    _performChange(
                        song,
                        lambda vals: [
                            [role_replacements.get(item[0], item[0]), item[1]]
                            for item in vals
                            if len(item) == 2
                        ],
                    )
                    or changes_made
                )

        if changes_made:
            self._resetView()

        return changes_made
