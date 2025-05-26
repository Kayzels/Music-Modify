from collections.abc import Sized
import logging
from typing import Callable, Generic, TypeVar, cast, override

from PySide6.QtWidgets import QFormLayout, QWidget

from music_modify.custom_types import Song, SongTag
from music_modify.gui.completion import EditWithComplete, createCompletionWidget
from music_modify.gui.edit.widget_edit_table import EditTableWidget
from music_modify.utils.list_utils import (
    remapMatchingSublistPairs,
    removeMatchingSublistPairs,
    toPairs,
    addValues,
    removePairs,
)

from .widget_edit_bulk_abstract_group import EditBulkAbstractGroupWidget

logger = logging.getLogger(__name__)

PAIR_SEPARATOR = ": "

L = TypeVar("L", bound=Sized)
MapFunc = Callable[[L, list[list[str]]], list[list[str]]]


class _ActionMapping(Generic[L]):
    def __init__(self, widget: "EditBulkPeopleWidget", items: L, func: MapFunc[L]):
        self.widget: "EditBulkPeopleWidget" = widget
        self.tag: SongTag = self.widget.tag
        self.items: L = items
        self.func: MapFunc[L] = func

    def _getSongValues(self, song: Song) -> list[list[str]]:
        original_values = self.tag.getValue(song.id3)
        if original_values is None:
            if not self.tag.hasTag(song.id3):
                self.tag.generateFrame(song.id3)
            original_values = []
        original_values = cast(list[list[str]], original_values)
        return original_values

    def performChange(self, song: Song) -> bool:
        if len(self.items) == 0:
            return False
        current_values = self._getSongValues(song)
        new_values = self.func(self.items, current_values)

        if new_values != current_values:
            self.tag.setTag(song.id3, new_values)
            song.save()

            new_pairs = [(role, person) for role, person in new_values]
            for pair in new_pairs:
                if pair not in self.widget.items:
                    self.widget.items.append(pair)
            return True
        return False


# Type Alias to prevent super long in-lay hint
AllowedActionMapping = (
    _ActionMapping[list[list[str]]]
    | _ActionMapping[set[tuple[str, ...]]]
    | _ActionMapping[set[str]]
    | _ActionMapping[dict[str, str]]
)


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

    def _createActionMapping(self, items: L, func: MapFunc[L]) -> _ActionMapping[L]:
        return _ActionMapping(self, items, func)

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
        # Map to dicts so it's quicker to get the changed values.
        map_people: dict[str, str] = {
            old: new for old, new in self.remap_person_widget.value
        }
        map_roles: dict[str, str] = {
            old: new for old, new in self.remap_role_widget.value
        }

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

        # Store whether any change is actually made.
        # Updated if a refresh is requested.
        changes_made: bool = False

        # Declare the functions explicitly so that it's more readable, compared to lambdas.
        def _removePeople(
            remove_values: set[str], original: list[list[str]]
        ) -> list[list[str]]:
            if len(remove_values) == 0:
                return original
            return removeMatchingSublistPairs(remove_values, original, 1)

        def _removeRoles(
            remove_values: set[str], original: list[list[str]]
        ) -> list[list[str]]:
            if len(remove_values) == 0:
                return original
            return removeMatchingSublistPairs(remove_values, original, 0)

        def _remapPeople(
            replacements: dict[str, str], original: list[list[str]]
        ) -> list[list[str]]:
            if len(replacements) == 0:
                return original
            return remapMatchingSublistPairs(replacements, original, 1)

        def _remapRoles(
            replacements: dict[str, str], original: list[list[str]]
        ) -> list[list[str]]:
            if len(replacements) == 0:
                return original
            return remapMatchingSublistPairs(replacements, original, 0)

        mappings: list[AllowedActionMapping] = [
            self._createActionMapping(add_items, addValues),
            self._createActionMapping(remove_pairs, removePairs),
            self._createActionMapping(remove_people, _removePeople),
            self._createActionMapping(remove_roles, _removeRoles),
            self._createActionMapping(map_people, _remapPeople),
            self._createActionMapping(map_roles, _remapRoles),
        ]

        for song in songs:
            for mapping in mappings:
                changes_made = mapping.performChange(song) or changes_made

        if changes_made:
            self._resetView()

        return changes_made
