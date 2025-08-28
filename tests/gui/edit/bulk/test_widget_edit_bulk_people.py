# pyright: reportPrivateUsage = false

from typing import cast
from unittest.mock import MagicMock

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.constants import PAIR_SEPARATOR
from music_modify.custom_types.song import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.gui.edit.bulk.widget_edit_bulk_people import (
    EditBulkPeopleWidget,
    _ActionMapping,
    _remapPeople,
    _remapRoles,
    _removePeople,
    _removeRoles,
)
from music_modify.utils.list_utils import addValues


def test_removePeopleAndRoles() -> None:
    original = [["First Role", "First Person"], ["Second Role", "Second Person"]]
    remove_people = {"First Person"}
    remove_roles = {"Second Role"}
    assert _removePeople(remove_people, original) == [["Second Role", "Second Person"]]
    assert _removeRoles(remove_roles, original) == [["First Role", "First Person"]]


def test_remapPeopleAndRoles() -> None:
    original = [["First Role", "First Person"], ["Second Role", "Second Person"]]
    replace_people = {"First Person": "Person 1", "Second Person": "Person 2"}
    replace_roles = {"First Role": "Role 1", "Second Role": "Role 2"}
    assert _remapPeople(replace_people, original) == [
        ["First Role", "Person 1"],
        ["Second Role", "Person 2"],
    ]
    assert _remapRoles(replace_roles, original) == [
        ["Role 1", "First Person"],
        ["Role 2", "Second Person"],
    ]


def test_ActionMapping_with_widget_empty_items_in_mapping(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)
    items: list[list[str]] = [["First Role", "First Person"]]

    action_mapping: _ActionMapping[list[list[str]]] = _ActionMapping(
        widget, items, addValues
    )

    song = Song()

    assert action_mapping._getSongValues(song) == []
    assert action_mapping.performChange(song)
    assert action_mapping._getSongValues(song) == [["First Role", "First Person"]]
    assert widget.items == [("First Role", "First Person")]


def test_ActionMapping_with_widget_empty_no_items_in_mapping(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)
    items: list[list[str]] = []

    action_mapping: _ActionMapping[list[list[str]]] = _ActionMapping(
        widget, items, addValues
    )

    song = Song()

    assert action_mapping._getSongValues(song) == []
    assert not action_mapping.performChange(song)
    assert action_mapping._getSongValues(song) == []
    assert widget.items == []


def test_ActionMapping_with_widget_mapping_items_identical_not_empty(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    song = Song()
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    original_data = [["First Role", "First Person"]]
    song.setTag("TIPL", original_data)
    widget = EditBulkPeopleWidget(parent, original_data, tag)
    qtbot.addWidget(widget)

    action_mapping: _ActionMapping[list[list[str]]] = _ActionMapping(
        widget, original_data, addValues
    )

    assert action_mapping._getSongValues(song) == original_data
    assert not action_mapping.performChange(song)
    assert action_mapping._getSongValues(song) == original_data
    assert widget.items == [("First Role", "First Person")]


def test_ActionMapping_with_widget_not_empty_mapping_items_empty(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    song = Song()
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    original_data = [["First Role", "First Person"]]
    song.setTag("TIPL", original_data)
    widget = EditBulkPeopleWidget(parent, original_data, tag)
    qtbot.addWidget(widget)

    action_mapping: _ActionMapping[list[list[str]]] = _ActionMapping(
        widget, [], addValues
    )

    assert action_mapping._getSongValues(song) == original_data
    assert not action_mapping.performChange(song)
    assert action_mapping._getSongValues(song) == original_data
    assert widget.items == [("First Role", "First Person")]


def test_ActionMapping_eq(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget1 = EditBulkPeopleWidget(parent, [], tag)
    widget2 = EditBulkPeopleWidget(parent, [], tag)
    assert widget1 != widget2

    func1 = addValues

    def func2[T](_: list[T] | None, original: list[T]) -> list[T]:
        return original

    # Same widgets, same data, same func
    mapping1 = _ActionMapping(widget1, [], func1)
    mapping2 = _ActionMapping(widget1, [], func1)
    assert mapping1 == mapping2
    assert mapping1 != widget1

    # Same widgets, same data, different func
    mapping1 = _ActionMapping(widget1, [], func1)
    mapping2 = _ActionMapping(widget2, [], func2)
    assert mapping1 != mapping2

    # Same widgets, different data, same func
    mapping1 = _ActionMapping(widget1, [], func1)
    mapping2 = _ActionMapping(widget1, [["One", "Two"]], func1)
    assert mapping1 != mapping2

    # Same widgets, different data, differnt func
    mapping1 = _ActionMapping(widget1, [], func1)
    mapping2 = _ActionMapping(widget1, [["One", "Two"]], func2)
    assert mapping1 != mapping2

    # Different widgets, same data, same func
    mapping1 = _ActionMapping(widget1, [], func1)
    mapping2 = _ActionMapping(widget2, [], func1)
    assert mapping1 != mapping2

    # Different widgets, same data, different func
    mapping1 = _ActionMapping(widget1, [], func1)
    mapping2 = _ActionMapping(widget2, [], func2)
    assert mapping1 != mapping2

    # Different widgets, different data, same func
    mapping1 = _ActionMapping(widget1, [], func1)
    mapping2 = _ActionMapping(widget2, [["One", "Two"]], func1)
    assert mapping1 != mapping2

    # Different widgets, different data, different func
    mapping1 = _ActionMapping(widget1, [["Three", "Four"]], func1)
    mapping2 = _ActionMapping(widget2, [["One", "Two"]], func2)
    assert mapping1 != mapping2


def test_EditBulkPeopleWidget_createActionMapping(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)
    items: list[list[str]] = []
    func = addValues

    mapping_external = _ActionMapping(widget, items, func)
    mapping_internal = widget._createActionMapping(items, func)
    assert mapping_external == mapping_internal


def test_EditBulkPeopleWidget_updateTag_unchecked(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    items = []
    songs = []
    widget = EditBulkPeopleWidget(parent, items, tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(False)
    assert not widget.updateTag(songs)


def test_EditBulkPeopleWidget_updateTag_clear_checkbox_checked(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    initial_data = [["Role 1", "Person 1"]]
    widget = EditBulkPeopleWidget(parent, initial_data, tag)
    qtbot.addWidget(widget)

    song1 = Song()
    song1.setTag(tag, initial_data)
    song2 = Song()
    song2.setTag(tag, initial_data)
    songs = [song1, song2]

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(True)

    assert widget.updateTag(songs) == {song1, song2}

    assert song1.getValue(tag) is None
    assert song2.getValue(tag) is None


def test_EditBulkPeopleWidget_updateTag_no_changes_attempted(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)

    song = Song()
    assert not song.hasTag(tag)
    songs = [song]

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    widget.add_widget.value = []
    widget.remove_pair_widget.setText("")
    assert widget.remove_pair_widget.values == []
    widget.remove_person_widget.setText("")
    assert widget.remove_person_widget.values == []
    widget.remove_role_widget.setText("")
    assert widget.remove_role_widget.values == []
    widget.remap_person_widget.value = []
    widget.remap_role_widget.value = []

    assert not widget.updateTag(songs)
    assert not song.hasTag(tag)
    assert song.getValue(tag) is None


def test_EditBulkPeopleWidget_updateTag_add_items_no_overlap(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)

    song1 = Song()
    song2 = Song()
    songs = [song1, song2]

    add_items = [["Role A", "Person A"], ["Role B", "Person B"]]
    widget.add_widget.value = add_items

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert widget.updateTag(songs) == {song1, song2}

    assert song1.getValue(tag) == add_items
    assert song2.getValue(tag) == add_items

    assert widget.items == [("Role A", "Person A"), ("Role B", "Person B")]


def test_EditBulkPeopleWidget_updateTag_add_items_mixed_overlap(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)

    add_items = [["RoleA", "PersonA"], ["RoleB", "PersonB"], ["RoleC", "PersonC"]]

    song1 = Song()  # Has all items
    song1.setTag(tag, add_items)

    song2 = Song()  # Has some items
    song2.setTag(tag, [["RoleA", "PersonA"]])

    song3 = Song()  # Has no items
    song3.setTag(tag, [])

    song4 = Song()  # Has extra items
    song4.setTag(tag, [["RoleE", "PersonE"]])

    songs = [song1, song2, song3, song4]

    widget.add_widget.value = add_items

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert widget.updateTag(songs) == {song2, song3, song4}

    assert song1.getValue(tag) == add_items
    assert song2.getValue(tag) == add_items
    assert song3.getValue(tag) == add_items
    assert song4.getValue(tag) == [["RoleE", "PersonE"], *add_items]

    expected_widget_items = [
        ("RoleA", "PersonA"),
        ("RoleB", "PersonB"),
        ("RoleC", "PersonC"),
        ("RoleE", "PersonE"),
    ]
    assert widget.items == expected_widget_items


def test_EditBulkPeopleWidget_updateTag_remove_pairs_no_overlap(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    initial_data = [["RoleX", "PersonY"]]
    widget = EditBulkPeopleWidget(parent, initial_data, tag)
    qtbot.addWidget(widget)

    song = Song()
    song.setTag(tag, initial_data)
    songs = [song]

    remove_pairs = ["RoleA" + PAIR_SEPARATOR + "PersonA"]
    widget.remove_pair_widget.setText("RoleA" + PAIR_SEPARATOR + "PersonA")
    assert widget.remove_pair_widget.values == remove_pairs

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert not widget.updateTag(songs)

    assert song.getValue(tag) == initial_data


def test_EditBulkPeopleWidget_updateTag_remove_pairs_mixed_overlap(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)

    pairs_to_remove = [
        "RoleA" + PAIR_SEPARATOR + "PersonA",
        "RoleB" + PAIR_SEPARATOR + "PersonB",
    ]

    song1 = Song()  # Has all pairs to remove + one extra
    song1.setTag(
        tag, [["RoleA", "PersonA"], ["RoleB", "PersonB"], ["RoleC", "PersonC"]]
    )

    song2 = Song()  # Has some pairs to remove + one extra
    song2.setTag(tag, [["RoleA", "PersonA"], ["RoleD", "PersonE"]])

    song3 = Song()  # Has none of the pairs to remove + one extra
    song3.setTag(tag, [["RoleX", "PersonY"]])

    songs = [song1, song2, song3]

    widget.remove_pair_widget.setText(",".join(pairs_to_remove))
    assert widget.remove_pair_widget.values == pairs_to_remove

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert widget.updateTag(songs) == {song1, song2}

    assert song1.getValue(tag) == [["RoleC", "PersonC"]]
    assert song2.getValue(tag) == [["RoleD", "PersonE"]]
    assert song3.getValue(tag) == [["RoleX", "PersonY"]]


def test_EditBulkPeopleWidget_updateTag_remove_roles_no_overlap(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    initial_data = [["RoleX", "PersonY"]]
    widget = EditBulkPeopleWidget(parent, initial_data, tag)
    qtbot.addWidget(widget)

    song = Song()
    song.setTag(tag, initial_data)
    songs = [song]

    remove_roles = ["RoleA"]
    widget.remove_role_widget.setText(",".join(remove_roles))
    assert widget.remove_role_widget.values == remove_roles

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert not widget.updateTag(songs)

    assert song.getValue(tag) == initial_data


def test_EditBulkPeopleWidget_updateTag_remove_roles_mixed_overlap(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)

    roles_to_remove = ["RoleA", "RoleB"]

    song1 = Song()  # Has all roles to remove + one extra
    song1.setTag(
        tag, [["RoleA", "Person1"], ["RoleB", "Person2"], ["RoleC", "Person3"]]
    )

    song2 = Song()  # Has some roles to remove + one extra
    song2.setTag(tag, [["RoleA", "Person4"], ["RoleD", "Person5"]])

    song3 = Song()  # Has none of the roles to remove + one extra
    song3.setTag(tag, [["RoleX", "PersonY"]])

    songs = [song1, song2, song3]

    widget.remove_role_widget.setText(",".join(roles_to_remove))
    assert widget.remove_role_widget.values == roles_to_remove

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert widget.updateTag(songs) == {song1, song2}

    assert song1.getValue(tag) == [["RoleC", "Person3"]]
    assert song2.getValue(tag) == [["RoleD", "Person5"]]
    assert song3.getValue(tag) == [["RoleX", "PersonY"]]


def test_EditBulkPeopleWidget_updateTag_remove_people_no_overlap(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    initial_data = [["RoleX", "PersonY"]]
    widget = EditBulkPeopleWidget(parent, initial_data, tag)
    qtbot.addWidget(widget)

    song = Song()
    song.setTag(tag, initial_data)
    songs = [song]

    remove_people = ["PersonA"]
    widget.remove_person_widget.setText(",".join(remove_people))
    assert widget.remove_person_widget.values == remove_people

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert not widget.updateTag(songs)

    assert song.getValue(tag) == initial_data


def test_EditBulkPeopleWidget_updateTag_remove_people_mixed_overlap(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)

    people_to_remove = ["PersonA", "PersonB"]

    song1 = Song()  # Has all people to remove + one extra
    song1.setTag(
        tag, [["Role1", "PersonA"], ["Role2", "PersonB"], ["Role3", "PersonC"]]
    )

    song2 = Song()  # Has some people to remove + one extra
    song2.setTag(tag, [["Role4", "PersonA"], ["Role5", "PersonD"]])

    song3 = Song()  # Has none of the people to remove + one extra
    song3.setTag(tag, [["RoleX", "PersonY"]])

    songs = [song1, song2, song3]

    widget.remove_person_widget.setText(",".join(people_to_remove))
    assert widget.remove_person_widget.values == people_to_remove

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert widget.updateTag(songs) == {song1, song2}

    assert song1.getValue(tag) == [["Role3", "PersonC"]]
    assert song2.getValue(tag) == [["Role5", "PersonD"]]
    assert song3.getValue(tag) == [["RoleX", "PersonY"]]


def test_EditBulkPeopleWidget_updateTag_remap_roles_mixed_overlap(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)

    role_replacements = [["OldRole1", "NewRole1"], ["OldRole2", "NewRole2"]]

    song1 = Song()  # Has all roles to remap
    song1.setTag(
        tag,
        [["OldRole1", "PersonA"], ["OldRole2", "PersonB"], ["RoleX", "PersonY"]],
    )

    song2 = Song()  # Has some roles to remap
    song2.setTag(tag, [["OldRole1", "PersonC"], ["RoleZ", "PersonW"]])

    song3 = Song()  # Has none of the roles to remap
    song3.setTag(tag, [["RoleA", "PersonF"]])

    songs = [song1, song2, song3]

    widget.remap_role_widget.value = role_replacements

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert widget.updateTag(songs) == {song1, song2}

    assert song1.getValue(tag) == [
        ["NewRole1", "PersonA"],
        ["NewRole2", "PersonB"],
        ["RoleX", "PersonY"],
    ]
    assert song2.getValue(tag) == [["NewRole1", "PersonC"], ["RoleZ", "PersonW"]]
    assert song3.getValue(tag) == [["RoleA", "PersonF"]]


def test_EditBulkPeopleWidget_updateTag_remap_people_mixed_overlap(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, [], tag)
    qtbot.addWidget(widget)

    person_replacements = [["OldPerson1", "NewPerson1"], ["OldPerson2", "NewPerson2"]]

    song1 = Song()  # Has all people to remap
    song1.setTag(
        tag,
        [["RoleA", "OldPerson1"], ["RoleB", "OldPerson2"], ["RoleC", "PersonX"]],
    )

    song2 = Song()  # Has some people to remap
    song2.setTag(tag, [["RoleD", "OldPerson1"], ["RoleE", "PersonY"]])

    song3 = Song()  # Has none of the people to remap
    song3.setTag(tag, [["RoleF", "PersonZ"]])

    songs = [song1, song2, song3]

    widget.remap_person_widget.value = person_replacements

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert widget.updateTag(songs) == {song1, song2}

    assert song1.getValue(tag) == [
        ["RoleA", "NewPerson1"],
        ["RoleB", "NewPerson2"],
        ["RoleC", "PersonX"],
    ]
    assert song2.getValue(tag) == [["RoleD", "NewPerson1"], ["RoleE", "PersonY"]]
    assert song3.getValue(tag) == [["RoleF", "PersonZ"]]


def test_EditBulkPeopleWidget_updateTag_multiple_actions(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    initial_widget_items = [
        ["ExistingRole", "ExistingPerson"],
        ["RoleToRemove", "PersonToRemove"],
    ]
    widget = EditBulkPeopleWidget(parent, initial_widget_items, tag)
    qtbot.addWidget(widget)

    song = Song()
    # Initial state of song: contains an existing item, one to be removed by pair,
    # one by role, one by person,
    # one whose role will be remapped, one whose person will be remapped.
    song.setTag(
        tag,
        [
            ["ExistingRole", "ExistingPerson"],
            ["RoleToRemove", "PersonToRemove"],
            ["RoleToDelete", "SomePerson"],
            ["SomeRole", "PersonToDelete"],
            ["OldRole", "SomeOtherPerson"],
            ["AnotherRole", "OldPerson"],
            ["StaticRole", "StaticPerson"],
        ],
    )

    # Set up actions
    widget.add_widget.value = [["NewRole", "NewPerson"]]
    widget.remove_pair_widget.setText(
        "RoleToRemove" + PAIR_SEPARATOR + "PersonToRemove"
    )
    assert widget.remove_pair_widget.values == [
        "RoleToRemove" + PAIR_SEPARATOR + "PersonToRemove"
    ]
    widget.remove_role_widget.setText("RoleToDelete")
    assert widget.remove_role_widget.values == ["RoleToDelete"]
    widget.remove_person_widget.setText("PersonToDelete")
    assert widget.remove_person_widget.values == ["PersonToDelete"]
    widget.remap_role_widget.value = [["OldRole", "RemappedRole"]]
    widget.remap_person_widget.value = [["OldPerson", "RemappedPerson"]]

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    assert widget.updateTag([song]) == {song}

    # Order of operations: addValues, removePairs, _removePeople, _removeRoles,
    # _remapPeople, _remapRoles
    # The list_utils functions can reorder.
    final_song_tags = cast(list[list[str]], song.getValue(tag))
    assert set(map(tuple, final_song_tags)) == {
        ("ExistingRole", "ExistingPerson"),
        ("NewRole", "NewPerson"),
        ("RemappedRole", "SomeOtherPerson"),  # Remap role
        ("AnotherRole", "RemappedPerson"),  # Remap person
        ("StaticRole", "StaticPerson"),
    }


def test_EditBulkPeopleWidget_resetView(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    initial_widget_data = [["Role1", "Person1"], ["Role2", "Person2"]]
    widget = EditBulkPeopleWidget(parent, initial_widget_data, tag)
    qtbot.addWidget(widget)

    # Manually populate some values to be cleared
    widget.add_widget.value = [["TempRole", "TempPerson"]]
    widget.remove_pair_widget.setText("Role1" + PAIR_SEPARATOR + "Person1")
    assert widget.remove_pair_widget.values == ["Role1" + PAIR_SEPARATOR + "Person1"]
    widget.remove_role_widget.setText("Role1")
    assert widget.remove_role_widget.values == ["Role1"]
    widget.remove_person_widget.setText("Person1")
    assert widget.remove_person_widget.values == ["Person1"]
    widget.remap_role_widget.value = [["R1", "R2"]]
    widget.remap_person_widget.value = [["P1", "P2"]]

    # Set checkboxes to True to ensure they are reset to False
    widget.clear_checkbox.setChecked(True)
    widget.group_box.setChecked(True)

    mock_add_clear = MagicMock()
    monkeypatch.setattr(widget.add_widget, "clear", mock_add_clear)

    mock_remove_pair_update_cache = MagicMock()
    monkeypatch.setattr(
        widget.remove_pair_widget, "updateItemsCache", mock_remove_pair_update_cache
    )
    mock_remove_pair_clear = MagicMock()
    monkeypatch.setattr(widget.remove_pair_widget, "clear", mock_remove_pair_clear)

    mock_remove_role_update_cache = MagicMock()
    monkeypatch.setattr(
        widget.remove_role_widget, "updateItemsCache", mock_remove_role_update_cache
    )
    mock_remove_role_clear = MagicMock()
    monkeypatch.setattr(widget.remove_role_widget, "clear", mock_remove_role_clear)

    mock_remove_person_update_cache = MagicMock()
    monkeypatch.setattr(
        widget.remove_person_widget, "updateItemsCache", mock_remove_person_update_cache
    )
    mock_remove_person_clear = MagicMock()
    monkeypatch.setattr(widget.remove_person_widget, "clear", mock_remove_person_clear)

    mock_remap_role_clear = MagicMock()
    monkeypatch.setattr(widget.remap_role_widget, "clear", mock_remap_role_clear)

    mock_remap_person_clear = MagicMock()
    monkeypatch.setattr(widget.remap_person_widget, "clear", mock_remap_person_clear)

    # Call the method
    widget._resetView()

    # Assertions for updateItemsCache calls
    expected_pairs = tuple(
        {f"{role}{PAIR_SEPARATOR}{person}" for (role, person) in initial_widget_data}
    )
    mock_remove_pair_update_cache.assert_called_once_with(expected_pairs)

    expected_roles = tuple({role for (role, _) in initial_widget_data})
    mock_remove_role_update_cache.assert_called_once_with(expected_roles)

    expected_people = tuple({person for (_, person) in initial_widget_data})
    mock_remove_person_update_cache.assert_called_once_with(expected_people)

    # Assertions for clear() calls
    mock_add_clear.assert_called_once()
    mock_remove_pair_clear.assert_called_once()
    mock_remove_role_clear.assert_called_once()
    mock_remove_person_clear.assert_called_once()
    mock_remap_role_clear.assert_called_once()
    mock_remap_person_clear.assert_called_once()

    # Assert checkboxes are reset
    assert not widget.clear_checkbox.isChecked()
    assert not widget.group_box.isChecked()
