import logging
from typing import Callable, cast, override

from PySide6.QtWidgets import QFormLayout, QWidget

from music_modify.custom_types import Song, SongTag
from music_modify.gui.completion import EditWithComplete, createCompletionWidget
from music_modify.gui.edit.widget_edit_table import EditTableWidget
from music_modify.utils.list_utils import toPairs

from .widget_edit_bulk_abstract_group import EditBulkAbstractGroupWidget

logger = logging.getLogger(__name__)

PAIR_SEPARATOR = ": "


class EditBulkPeopleWidget(EditBulkAbstractGroupWidget):
    def __init__(self, parent: QWidget, data: list[list[str]], tag: SongTag):
        super().__init__(parent, tag)

        self.items: list[tuple[str, str]] = [(role, person) for role, person in data]
        self.setupUi()

        self.add_widget: EditTableWidget
        self.remove_pair_widget: EditWithComplete
        self.remove_role_widget: EditWithComplete
        self.remove_person_widget: EditWithComplete
        self.remap_role_widget: EditTableWidget
        self.remap_person_widget: EditTableWidget

    @override
    def createForm(self) -> QWidget:
        form_layout = QFormLayout()
        form_container: QWidget = QWidget()
        form_container.setLayout(form_layout)
        form_layout.setContentsMargins(0, 0, 0, 0)

        self.add_widget = EditTableWidget(self, [])
        form_layout.addRow("Add", self.add_widget)

        pairs = list(
            set([f"{role}{PAIR_SEPARATOR}{person}" for (role, person) in self.items])
        )
        self.remove_pair_widget = createCompletionWidget(self, tuple(pairs))
        form_layout.addRow("Remove Pair", self.remove_pair_widget)

        roles = list(set([role for (role, _) in self.items]))
        self.remove_role_widget = createCompletionWidget(self, tuple(roles))
        form_layout.addRow("Remove Role", self.remove_role_widget)

        people = list(set([person for (_, person) in self.items]))
        self.remove_person_widget = createCompletionWidget(self, tuple(people))
        form_layout.addRow("Remove Person", self.remove_person_widget)

        remap_headers = ["Old", "New"]
        self.remap_role_widget = EditTableWidget(self, [], labels=remap_headers)
        form_layout.addRow("Remap Role", self.remap_role_widget)

        self.remap_person_widget = EditTableWidget(self, [], labels=remap_headers)
        form_layout.addRow("Remap Person", self.remap_person_widget)

        return form_container

    @override
    def _resetView(self):
        pairs = list(set([f"{role}: {person}" for (role, person) in self.items]))
        self.remove_pair_widget.updateItemsCache(tuple(pairs))

        roles = list(set([role for (role, _) in self.items]))
        self.remove_role_widget.updateItemsCache(tuple(roles))

        people = list(set([person for (_, person) in self.items]))
        self.remove_person_widget.updateItemsCache(tuple(people))

        widgets = self.findChildren(EditWithComplete) + self.findChildren(
            EditTableWidget
        )
        for widget in widgets:
            widget.clear()

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
        add_items: list[list[str]] = self.add_widget.value
        remove_pairs: set[tuple[str, ...]] = {
            tuple(pair)
            for pair in toPairs(self.remove_pair_widget.values, PAIR_SEPARATOR)
        }
        remove_people: set[str] = set(self.remove_person_widget.values)
        remove_roles: set[str] = set(self.remove_role_widget.values)
        map_people: list[list[str]] = self.remap_person_widget.value
        map_roles: list[list[str]] = self.remap_role_widget.value

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

                # Update items stored as well, for after view is reset
                new_pairs = [(role, person) for role, person in new_values]
                for pair in new_pairs:
                    if pair not in self.items:
                        self.items.append(pair)
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
                            item for item in vals if tuple(item) not in remove_pairs
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
