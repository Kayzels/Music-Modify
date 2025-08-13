"""Moduole that contains the widget that is used for bulk editing data,
when the tag contains (role, person) pairs."""

from collections.abc import Sized
import logging
from typing import Callable, Generic, TypeVar, cast, override

from PySide6.QtWidgets import QFormLayout, QWidget

from music_modify.custom_types import Song, SongTag
from music_modify.custom_types.enums import PairIndex
from music_modify.gui.completion import EditWithComplete, createCompletionWidget
from music_modify.gui.edit.widget_edit_table import EditTableWidget
from music_modify.utils.list_utils import (
    addValues,
    remapMatchingSublistPairs,
    removeMatchingSublistPairs,
    removePairs,
    toPairs,
)

from .widget_edit_bulk_abstract_group import EditBulkAbstractGroupWidget

logger = logging.getLogger(__name__)

PAIR_SEPARATOR = ": "

L = TypeVar("L", bound=Sized)
MapFunc = Callable[[L, list[list[str]]], list[list[str]]]


class _ActionMapping(Generic[L]):
    """Private class that is used to define a function that should
    transform the data stored in a tag, in some way."""

    def __init__(
        self,
        widget: "EditBulkPeopleWidget",
        items: L,
        func: MapFunc[L],
    ) -> None:
        """
        Args:
            widget: Widget that displays the data that should be mapped
            items: Any data structure that is used by `func` to transform the data
            func: A function that transforms a list of pairs, using `items`
        """
        self.widget: "EditBulkPeopleWidget" = widget
        "The widget that displays the data"
        self.tag: SongTag = self.widget.tag
        "The tag that the data should be edited for."
        self.items: L = items
        "Any data structure that is used to transform a pair"
        self.func: MapFunc[L] = func
        "Function that uses `items` to transform a pair into a new pair"

    def _getSongValues(self, song: Song) -> list[list[str]]:
        """Get the values stored for the song, for the tag."""
        original_values = self.tag.getValue(song.id3)
        if original_values is None:
            if not self.tag.hasTag(song.id3):
                self.tag.generateFrame(song.id3)
            original_values = []
        original_values = cast(list[list[str]], original_values)
        return original_values

    def performChange(self, song: Song) -> bool:
        """Call `func` on the data for the tag in the specified `song`.

        Args:
            song: The `Song` that contains the data that should be changed.
        """
        if len(self.items) == 0:
            return False
        current_values = self._getSongValues(song)
        new_values = self.func(self.items, current_values)

        if new_values != current_values:
            self.tag.setTag(song.id3, new_values)
            song.save()

            new_pairs: list[tuple[str, str]] = [
                (role, person) for role, person in new_values
            ]
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
    def __init__(self, parent: QWidget, data: list[list[str]], tag: SongTag) -> None:
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
            {f"{role}{PAIR_SEPARATOR}{person}" for (role, person) in self.items},
        )
        self.remove_pair_widget = createCompletionWidget(
            parent=self,
            items=tuple(pairs),
        )
        form_layout.addRow("Remove Pair", self.remove_pair_widget)

        roles = list({role for (role, _) in self.items})
        self.remove_role_widget = createCompletionWidget(
            parent=self,
            items=tuple(roles),
        )
        form_layout.addRow("Remove Role", self.remove_role_widget)

        people = list({person for (_, person) in self.items})
        self.remove_person_widget = createCompletionWidget(
            parent=self,
            items=tuple(people),
        )
        form_layout.addRow("Remove Person", self.remove_person_widget)

        remap_headers = ["Old", "New"]
        self.remap_role_widget = EditTableWidget(
            parent=self,
            data=[],
            labels=remap_headers,
        )
        form_layout.addRow("Remap Role", self.remap_role_widget)

        self.remap_person_widget = EditTableWidget(
            parent=self,
            data=[],
            labels=remap_headers,
        )
        form_layout.addRow("Remap Person", self.remap_person_widget)

        return form_container

    @override
    def _resetView(self) -> None:
        pairs = tuple(
            {f"{role}: {person}" for (role, person) in self.items},
        )
        self.remove_pair_widget.updateItemsCache(pairs)

        roles = tuple({role for (role, _) in self.items})
        self.remove_role_widget.updateItemsCache(roles)

        people = tuple({person for (_, person) in self.items})
        self.remove_person_widget.updateItemsCache(people)

        widgets: list[EditTableWidget | EditWithComplete] = self.findChildren(
            EditWithComplete,
        ) + self.findChildren(EditTableWidget)
        for widget in widgets:
            widget.clear()

        self.clear_checkbox.setChecked(False)
        self.group_box.setChecked(False)

    def _createActionMapping(self, items: L, func: MapFunc[L]) -> _ActionMapping[L]:
        """Creates a mapping based on the items sent, and the function"""
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
            for pair in toPairs(
                values=self.remove_pair_widget.values,
                separator=PAIR_SEPARATOR,
            )
        }
        remove_people: set[str] = set(self.remove_person_widget.values)
        remove_roles: set[str] = set(self.remove_role_widget.values)
        # Map to dicts so it's quicker to get the changed values.
        map_people: dict[str, str] = dict(self.remap_person_widget.value)
        map_roles: dict[str, str] = dict(self.remap_role_widget.value)

        # If any of the above values aren't empty,
        # the user intends to make a change.
        change_attempted = any(
            len(c) > 0
            for c in (
                add_items,
                remove_pairs,
                remove_people,
                remove_roles,
                map_people,
                map_roles,
            )
        )
        if not change_attempted:
            return False

        # Store whether any change is actually made.
        # Updated if a refresh is requested.
        changes_made: bool = False

        # Declare the functions explicitly so that it's more readable,
        # compared to lambdas.
        def _removePeople(
            remove_values: set[str],
            original: list[list[str]],
        ) -> list[list[str]]:
            """Remove any string that appears in `remove_values` from the list,
            when that string appears in the people index."""
            if len(remove_values) == 0:
                return original
            return removeMatchingSublistPairs(
                remove_values,
                original,
                index=PairIndex.Person.value,
            )

        def _removeRoles(
            remove_values: set[str],
            original: list[list[str]],
        ) -> list[list[str]]:
            """Remove any string that appears in `remove_values` from the list,
            when that string appears in the roles index."""
            if len(remove_values) == 0:
                return original
            return removeMatchingSublistPairs(
                remove_values,
                original,
                index=PairIndex.Role.value,
            )

        def _remapPeople(
            replacements: dict[str, str],
            original: list[list[str]],
        ) -> list[list[str]]:
            """Remap any string that appears as a key in `replacements` from the list,
            when that string appears in the people index."""
            if len(replacements) == 0:
                return original
            return remapMatchingSublistPairs(
                replacements,
                original,
                index=PairIndex.Person.value,
            )

        def _remapRoles(
            replacements: dict[str, str],
            original: list[list[str]],
        ) -> list[list[str]]:
            """Remap any string that appears as a key in `replacements` from the list,
            when that string appears in the roles index."""
            if len(replacements) == 0:
                return original
            return remapMatchingSublistPairs(
                replacements,
                original,
                index=PairIndex.Role.value,
            )

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
