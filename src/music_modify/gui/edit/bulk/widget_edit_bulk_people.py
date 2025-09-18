"""Module that defines an EditBulkPeopleWidget.

This widget is used for bulk editing data,
when the tag contains (role, person) pairs.
"""

from collections.abc import Callable, Sized
import logging
from typing import override

from PySide6.QtWidgets import QFormLayout, QWidget

from music_modify.core import constants
from music_modify.custom_types import Song, TagInfo
from music_modify.custom_types.enums import PairIndex
from music_modify.custom_types.tag_value import PairedTextTagValue
from music_modify.gui.completion import EditWithComplete
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


def _removePeople(
    remove_values: set[str],
    original: list[list[str]],
) -> list[list[str]]:
    """Remove any strings from `remove_values` that appear in the people index."""
    return removeMatchingSublistPairs(
        remove_values,
        original,
        index=PairIndex.Person.value,
    )


def _removeRoles(
    remove_values: set[str],
    original: list[list[str]],
) -> list[list[str]]:
    """Remove any strings from `remove_values` that appear in the roles index."""
    return removeMatchingSublistPairs(
        remove_values,
        original,
        index=PairIndex.Role.value,
    )


def _remapPeople(
    replacements: dict[str, str],
    original: list[list[str]],
) -> list[list[str]]:
    """Replaces people index values, for the strings that are keys in replacements.

    Remap any string that appears as a key in `replacements` from the list,
    when that string appears in the people index.
    """
    return remapMatchingSublistPairs(
        replacements,
        original,
        index=PairIndex.Person.value,
    )


def _remapRoles(
    replacements: dict[str, str],
    original: list[list[str]],
) -> list[list[str]]:
    """Replaces role index values, for the strings that are keys in replacements.

    Remap any string that appears as a key in `replacements` from the list,
    when that string appears in the role index.
    """
    return remapMatchingSublistPairs(
        replacements,
        original,
        index=PairIndex.Role.value,
    )


type MapFunc[L: Sized] = Callable[[L, list[list[str]]], list[list[str]]]


class _ActionMapping[L: Sized]:
    """Private class that calls a function to transform the data stored in a tag."""

    __hash__ = None  # pyright: ignore[reportAssignmentType]

    def __init__(
        self,
        widget: "EditBulkPeopleWidget",
        items: L,
        func: MapFunc[L],
    ) -> None:
        """Creates an ActionMapping.

        Args:
            widget: Widget that displays the data that should be mapped
            items: Any data structure that is used by `func` to transform the data
            func: A function that transforms a list of pairs, using `items`
        """
        self.widget: EditBulkPeopleWidget = widget
        "The widget that displays the data"
        self.tag: TagInfo = self.widget.tag
        "The tag that the data should be edited for."
        self.items: L = items
        "Any data structure that is used to transform a pair"
        self.func: MapFunc[L] = func
        "Function that uses `items` to transform a pair into a new pair"

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, _ActionMapping):
            return False
        return (
            value.items == self.items
            and value.func == self.func
            and value.widget == self.widget
        )

    def _getSongValues(self, song: Song) -> list[list[str]]:
        """Get the values stored for the song, for the tag."""
        original_values = song.getTag(self.tag.id3_key)
        if original_values is None:
            return []
        if not isinstance(original_values, PairedTextTagValue):
            logger.error(
                f"Expected values ot be a PairedTextTagValue, got {type(original_values)} instead."
            )
            return []
        return original_values.value

    def performChange(self, song: Song) -> bool:
        """Call `func` on the data for the tag in the specified `song`.

        Args:
            song: The `Song` that contains the data that should be changed.
        """
        if not self.items or len(self.items) == 0:
            return False
        current_values = self._getSongValues(song)
        new_values = self.func(self.items, current_values)

        if new_values != current_values:
            song.setTag(self.tag.id3_key, PairedTextTagValue(new_values))

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
    """Widget used for bulk editing values that are [role, person] pairs."""

    def __init__(
        self,
        data: list[list[str]],
        tag: TagInfo,
        parent: QWidget | None = None,
    ) -> None:
        """Create an EditBulkPeopleWidget.

        Args:
            data: The data to be displayed.
            tag: The field in the song that should be updated.
            parent: The widget that this widget should be displayed on.
        """
        super().__init__(tag, parent)

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

        self.add_widget = EditTableWidget(PairedTextTagValue([]), self)
        form_layout.addRow("Add", self.add_widget)

        pairs = list(
            {
                f"{role}{constants.PAIR_SEPARATOR}{person}"
                for (role, person) in self.items
            },
        )
        self.remove_pair_widget = EditWithComplete(parent=self, items=tuple(pairs))
        form_layout.addRow("Remove Pair", self.remove_pair_widget)

        roles = list({role for (role, _) in self.items})
        self.remove_role_widget = EditWithComplete(parent=self, items=tuple(roles))
        form_layout.addRow("Remove Role", self.remove_role_widget)

        people = list({person for (_, person) in self.items})
        self.remove_person_widget = EditWithComplete(
            parent=self,
            items=tuple(people),
        )
        form_layout.addRow("Remove Person", self.remove_person_widget)

        remap_headers = ["Old", "New"]
        self.remap_role_widget = EditTableWidget(
            parent=self, initial_value=PairedTextTagValue([])
        )
        self.remap_role_widget.setHorizontalHeaderLabels(remap_headers)
        form_layout.addRow("Remap Role", self.remap_role_widget)

        self.remap_person_widget = EditTableWidget(
            parent=self, initial_value=PairedTextTagValue([])
        )
        self.remap_person_widget.setHorizontalHeaderLabels(remap_headers)
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

    def _createActionMapping[L: Sized](
        self,
        items: L,
        func: MapFunc[L],
    ) -> _ActionMapping[L]:
        """Creates a mapping based on the items sent, and the function."""
        return _ActionMapping(self, items, func)

    @override
    def updateTag(self, songs: list[Song]) -> set[Song]:
        checkbox_result = self._handleCheckboxes(songs)
        if checkbox_result is not None:
            return checkbox_result

        # Collect all possible changes
        add_items: list[list[str]] = (
            value.value
            if isinstance((value := self.add_widget.value), PairedTextTagValue)
            else []
        )
        remove_pairs: set[tuple[str, ...]] = {
            tuple(pair)
            for pair in toPairs(
                values=self.remove_pair_widget.values,
                separator=constants.PAIR_SEPARATOR,
            )
        }
        remove_people: set[str] = set(self.remove_person_widget.values)
        remove_roles: set[str] = set(self.remove_role_widget.values)
        # Map to dicts so it's quicker to get the changed values.
        map_people: dict[str, str] = (
            dict(value.value)
            if isinstance((value := self.remap_person_widget.value), PairedTextTagValue)
            else {}
        )
        map_roles: dict[str, str] = (
            dict(value.value)
            if isinstance((value := self.remap_role_widget.value), PairedTextTagValue)
            else {}
        )

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
            return set()

        # Store which songs were actually modified.
        modified_songs: set[Song] = set()

        mappings: list[AllowedActionMapping] = [
            self._createActionMapping(add_items, addValues),
            self._createActionMapping(remove_pairs, removePairs),
            self._createActionMapping(remove_people, _removePeople),
            self._createActionMapping(remove_roles, _removeRoles),
            self._createActionMapping(map_people, _remapPeople),
            self._createActionMapping(map_roles, _remapRoles),
        ]

        for song in songs:
            song_had_changes = False
            for mapping in mappings:
                if mapping.performChange(song):
                    song_had_changes = True
            if song_had_changes:
                modified_songs.add(song)

        if modified_songs:
            self._resetView()

        return modified_songs
