"""Tests for EditBulkPeopleWidget."""

# pyright: reportPrivateUsage = false, reportUnusedParameter = false

from typing import TypedDict, cast
from unittest.mock import MagicMock

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.constants import PAIR_SEPARATOR
from music_modify.custom_types.song import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.gui.completion.edit_with_complete import EditWithComplete
from music_modify.gui.edit.bulk.widget_edit_bulk_people import (
    EditBulkPeopleWidget,
    _ActionMapping,
    _remapPeople,
    _remapRoles,
    _removePeople,
    _removeRoles,
)
from music_modify.gui.edit.widget_edit_table import EditTableWidget
from music_modify.utils.list_utils import addValues


def test_removePeopleAndRoles() -> None:
    """Tests that removing values from the lists works for roles and people."""
    original = [["First Role", "First Person"], ["Second Role", "Second Person"]]
    remove_people = {"First Person"}
    remove_roles = {"Second Role"}
    assert _removePeople(remove_people, original) == [["Second Role", "Second Person"]]
    assert _removeRoles(remove_roles, original) == [["First Role", "First Person"]]


def test_remapPeopleAndRoles() -> None:
    """Tests that remapping values from the lists works for roles and people."""
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


def _createWidget(
    qtbot: QtBot, data: list[list[str]]
) -> tuple[QWidget, SongTag, EditBulkPeopleWidget]:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Involved People", id3_key="TIPL")
    widget = EditBulkPeopleWidget(parent, data, tag)
    qtbot.addWidget(widget)

    return parent, tag, widget


class _ChangeParams(TypedDict):
    widget_items: list[list[str]]
    mapping_items: list[list[str]]
    song_items: list[list[str]] | None
    expected_before_change: list[list[str]]
    expected_perform_change: bool
    expected_after_change: list[list[str]]
    id: str


change_params: list[_ChangeParams] = [
    {
        "widget_items": [],
        "mapping_items": [["First Role", "First Person"]],
        "song_items": None,
        "expected_before_change": [],
        "expected_perform_change": True,
        "expected_after_change": [["First Role", "First Person"]],
        "id": "widget_empty_items_in_mapping_changed",
    },
    {
        "widget_items": [],
        "mapping_items": [],
        "song_items": None,
        "expected_before_change": [],
        "expected_perform_change": False,
        "expected_after_change": [],
        "id": "widget_empty_no_items_in_mapping_not_changed",
    },
    {
        "widget_items": [["First Role", "First Person"]],
        "mapping_items": [["First Role", "First Person"]],
        "song_items": [["First Role", "First Person"]],
        "expected_before_change": [["First Role", "First Person"]],
        "expected_perform_change": False,
        "expected_after_change": [["First Role", "First Person"]],
        "id": "widget_mapping_identical_not_empty_not_changed",
    },
    {
        "widget_items": [["First Role", "First Person"]],
        "mapping_items": [],
        "song_items": [["First Role", "First Person"]],
        "expected_before_change": [["First Role", "First Person"]],
        "expected_perform_change": False,
        "expected_after_change": [["First Role", "First Person"]],
        "id": "widget_not_empty_mapping_empty_not_changed",
    },
    {
        "widget_items": [["First Role", "First Person"]],
        "mapping_items": [["Second Role", "Second Person"]],
        "song_items": [["First Role", "First Person"]],
        "expected_before_change": [["First Role", "First Person"]],
        "expected_perform_change": True,
        "expected_after_change": [
            ["First Role", "First Person"],
            ["Second Role", "Second Person"],
        ],
        "id": "widget_not_empty_mapping_not_empty_diff_changed",
    },
]


@pytest.mark.parametrize(
    ("change_param"),
    [
        pytest.param(change_param, id=change_param["id"])
        for change_param in change_params
    ],
)
def test_ActionMapping_performChange_param(
    qtbot: QtBot, change_param: _ChangeParams, mock_settings: MagicMock
) -> None:
    """Tests how performChange works based on different inputs.

    If widget is empty, but mapping has items, add to song and widget.
    If widget and mapping empty, no change.
    If widget and mapping match, no change.
    If widget not empty, but mapping has no items, no change.
    If widget not empty, and mapping not empty, should change.
    """
    widget_items = change_param["widget_items"]
    song_items = change_param["song_items"]
    mapping_items = change_param["mapping_items"]
    expected_before_change = change_param["expected_before_change"]
    expected_perform_change = change_param["expected_perform_change"]
    expected_after_change = change_param["expected_after_change"]

    _, tag, widget = _createWidget(qtbot, widget_items)

    song = Song()
    if song_items is not None:
        song.setTag(tag, song_items)

    action_mapping: _ActionMapping[list[list[str]]] = _ActionMapping(
        widget, mapping_items, addValues
    )

    assert action_mapping._getSongValues(song) == expected_before_change
    assert action_mapping.performChange(song) is expected_perform_change
    assert action_mapping._getSongValues(song) == expected_after_change
    assert widget.items == [tuple(item) for item in expected_after_change]


def test_ActionMapping_eq(qtbot: QtBot) -> None:
    """Test that _ActionMapping equality works properly.

    A mapping is the same if it has the same widget, function, and data.
    """
    _, __, widget1 = _createWidget(qtbot, [])
    __, ___, widget2 = _createWidget(qtbot, [])
    assert widget1 != widget2

    func1 = addValues

    def func2[T](_: list[T] | None, original: list[T]) -> list[T]:
        return original

    # Same widgets, same data, same func
    mapping1 = _ActionMapping(widget1, [], func1)
    mapping2 = _ActionMapping(widget1, [], func1)
    assert mapping1 == mapping2

    # Test that returns False for other types.
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
    """Test that calling _createActionMapping makes the right _ActionMapping."""
    widget_data: list[list[str]] = []
    _, __, widget = _createWidget(qtbot, widget_data)

    func = addValues

    mapping_external = _ActionMapping(widget, widget_data, func)
    mapping_internal = widget._createActionMapping(widget_data, func)
    assert mapping_external == mapping_internal


def test_EditBulkPeopleWidget_updateTag_unchecked(qtbot: QtBot) -> None:
    """Test that updateTag isn't called if the update box isn't checked."""
    widget_data = []
    _, __, widget = _createWidget(qtbot, widget_data)

    songs = []

    widget.group_box.setChecked(False)
    assert widget.updateTag(songs) == set()


def test_EditBulkPeopleWidget_updateTag_clear_checkbox_checked(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Test that values are cleared when updateTag is called with clear checked."""
    initial_data = [["Role 1", "Person 1"]]
    _, tag, widget = _createWidget(qtbot, initial_data)

    song1 = Song()
    song1.setTag(tag, initial_data)
    song2 = Song()
    song2.setTag(tag, initial_data)
    songs = [song1, song2]

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(True)

    assert song1.getValue(tag) is not None
    assert song2.getValue(tag) is not None

    assert widget.updateTag(songs) == {song1, song2}

    assert song1.getValue(tag) is None
    assert song2.getValue(tag) is None


def test_EditBulkPeopleWidget_updateTag_no_changes_attempted(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests that updateTag isn't called when there are no changes."""
    widget_data = []
    _, tag, widget = _createWidget(qtbot, widget_data)

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


def _set_widget_value(
    widget: QWidget, value: str | list[str] | list[list[str]]
) -> None:
    if isinstance(widget, EditWithComplete):
        value_to_set: str = ""
        if isinstance(value, str):
            value_to_set = value
        elif len(value) > 0 and isinstance(value[0], str):
            value = cast(list[str], value)
            value_to_set = ", ".join(value)
        widget.setText(value_to_set)
    elif isinstance(widget, EditTableWidget) and isinstance(value, list):
        if len(value) > 0 and not isinstance(value[0], list):
            return
        value = cast(list[list[str]], value)
        widget.value = value


class _SongInfo(TypedDict):
    items: list[list[str]]
    updated: bool
    expected_items: list[list[str]]
    id: str


_add_items = [["RoleA", "PersonA"], ["RoleB", "PersonB"], ["RoleC", "PersonC"]]
_add_info: list[_SongInfo] = [
    {
        "items": _add_items,
        "updated": False,
        "expected_items": _add_items,
        "id": "all_items",
    },
    {
        "items": [["RoleA", "PersonA"]],
        "updated": True,
        "expected_items": _add_items,
        "id": "some_items",
    },
    {
        "items": [],
        "updated": True,
        "expected_items": _add_items,
        "id": "no_items",
    },
    {
        "items": [["RoleE", "PersonE"]],
        "updated": True,
        "expected_items": [["RoleE", "PersonE"], *_add_items],
        "id": "extra_items",
    },
]


_remove_pairs_items = [
    "RoleA" + PAIR_SEPARATOR + "PersonA",
    "RoleB" + PAIR_SEPARATOR + "PersonB",
]
_remove_pairs_info: list[_SongInfo] = [
    {
        "items": [["RoleA", "PersonA"], ["RoleB", "PersonB"], ["RoleC", "PersonC"]],
        "updated": True,
        "expected_items": [["RoleC", "PersonC"]],
        "id": "all_extra",
    },
    {
        "items": [["RoleA", "PersonA"], ["RoleD", "PersonD"]],
        "updated": True,
        "expected_items": [["RoleD", "PersonD"]],
        "id": "some_extra",
    },
    {
        "items": [["RoleX", "PersonY"]],
        "updated": False,
        "expected_items": [["RoleX", "PersonY"]],
        "id": "none_extra",
    },
]


_remove_roles_items = ["RoleA", "RoleB"]
_remove_roles_info: list[_SongInfo] = [
    {
        "items": [["RoleA", "Person1"], ["RoleB", "Person2"], ["RoleC", "Person3"]],
        "updated": True,
        "expected_items": [["RoleC", "Person3"]],
        "id": "all_roles_and_extra",
    },
    {
        "items": [["RoleA", "Person1"], ["RoleD", "Person4"]],
        "updated": True,
        "expected_items": [["RoleD", "Person4"]],
        "id": "some_roles_and_extra",
    },
    {
        "items": [["RoleX", "PersonY"]],
        "updated": False,
        "expected_items": [["RoleX", "PersonY"]],
        "id": "no_roles_and_extra",
    },
]


_remove_people_items = ["PersonA", "PersonB"]
_remove_people_info: list[_SongInfo] = [
    {
        "items": [["Role1", "PersonA"], ["Role2", "PersonB"], ["Role3", "PersonC"]],
        "updated": True,
        "expected_items": [["Role3", "PersonC"]],
        "id": "all_roles_and_extra",
    },
    {
        "items": [["Role1", "PersonA"], ["Role4", "PersonD"]],
        "updated": True,
        "expected_items": [["Role4", "PersonD"]],
        "id": "some_roles_and_extra",
    },
    {
        "items": [["RoleX", "PersonY"]],
        "updated": False,
        "expected_items": [["RoleX", "PersonY"]],
        "id": "no_roles_and_extra",
    },
]


_replace_roles_items = [["OldRole1", "NewRole1"], ["OldRole2", "NewRole2"]]
_replace_roles_info: list[_SongInfo] = [
    {
        "items": [
            ["OldRole1", "PersonA"],
            ["OldRole2", "PersonB"],
            ["RoleX", "PersonY"],
        ],
        "updated": True,
        "expected_items": [
            ["NewRole1", "PersonA"],
            ["NewRole2", "PersonB"],
            ["RoleX", "PersonY"],
        ],
        "id": "has_all",
    },
    {
        "items": [
            ["OldRole1", "PersonC"],
            ["RoleZ", "PersonW"],
        ],
        "updated": True,
        "expected_items": [
            ["NewRole1", "PersonC"],
            ["RoleZ", "PersonW"],
        ],
        "id": "has_some",
    },
    {
        "items": [
            ["RoleA", "PersonF"],
        ],
        "updated": False,
        "expected_items": [
            ["RoleA", "PersonF"],
        ],
        "id": "has_none",
    },
]


_replace_people_items = [["OldPerson1", "NewPerson1"], ["OldPerson2", "NewPerson2"]]
_replace_people_songs: list[_SongInfo] = [
    {
        "items": [
            ["RoleA", "OldPerson1"],
            ["RoleB", "OldPerson2"],
            ["RoleC", "PersonX"],
        ],
        "updated": True,
        "expected_items": [
            ["RoleA", "NewPerson1"],
            ["RoleB", "NewPerson2"],
            ["RoleC", "PersonX"],
        ],
        "id": "has_all",
    },
    {
        "items": [["RoleD", "OldPerson1"], ["RoleE", "PersonY"]],
        "updated": True,
        "expected_items": [["RoleD", "NewPerson1"], ["RoleE", "PersonY"]],
        "id": "has_some",
    },
    {
        "items": [
            ["RoleA", "PersonF"],
        ],
        "updated": False,
        "expected_items": [
            ["RoleA", "PersonF"],
        ],
        "id": "has_none",
    },
]


_bulk_param_definitions: list[
    tuple[str, list[str] | list[list[str]], list[_SongInfo], str]
] = [
    ("add_widget", _add_items, _add_info, "add_items"),
    ("remove_pair_widget", _remove_pairs_items, _remove_pairs_info, "remove_pairs"),
    ("remove_role_widget", _remove_roles_items, _remove_roles_info, "remove_roles"),
    (
        "remove_person_widget",
        _remove_people_items,
        _remove_people_info,
        "remove_people",
    ),
    ("remap_role_widget", _replace_roles_items, _replace_roles_info, "replace_roles"),
    (
        "remap_person_widget",
        _replace_people_items,
        _replace_people_songs,
        "replace_people",
    ),
]


@pytest.mark.parametrize(
    ("widget_name", "widget_items", "song_infos"),
    [
        pytest.param(widget_name, widget_items, song_infos, id=group_id)
        for widget_name, widget_items, song_infos, group_id in _bulk_param_definitions
    ],
)
def test_EditBulkPeopleWidget_updateTag_multiple_param(
    qtbot: QtBot,
    widget_name: str,
    widget_items: list[str] | list[list[str]],
    song_infos: list[_SongInfo],
    mock_settings: MagicMock,
) -> None:
    """Test updating tag based on the widget details."""
    widget_data = []
    _, tag, widget = _createWidget(qtbot, widget_data)

    songs: list[Song] = []
    expected_updated_songs: set[Song] = set()
    expected_song_values: list[list[list[str]]] = []
    for info in song_infos:
        song = Song()
        song.setTag(tag, info["items"])
        songs.append(song)
        if info["updated"]:
            expected_updated_songs.add(song)
        expected_song_values.append(info["expected_items"])

    _set_widget_value(getattr(widget, widget_name), widget_items)
    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)
    actual_updated_songs = widget.updateTag(songs)

    assert actual_updated_songs == expected_updated_songs

    for i, song in enumerate(songs):
        assert song.getValue(tag) == expected_song_values[i]


@pytest.mark.parametrize(
    ("widget_name", "widget_items", "info"),
    [
        pytest.param(
            widget_name, widget_items, song_info, id=f"{group_id}_{song_info['id']}"
        )
        for widget_name, widget_items, song_info_list, group_id in _bulk_param_definitions
        for song_info in song_info_list
    ],
)
def test_EditBulkPeopleWidget_updateTag_single_param(
    qtbot: QtBot,
    widget_name: str,
    widget_items: list[str] | list[list[str]],
    info: _SongInfo,
    mock_settings: MagicMock,
) -> None:
    """Tests updating tags for a single song, based on the widget details."""
    widget_data = []
    _, tag, widget = _createWidget(qtbot, widget_data)

    song = Song()
    song.setTag(tag, info["items"])

    expected_update_result: set[Song] = {song} if info["updated"] else set()

    _set_widget_value(getattr(widget, widget_name), widget_items)

    widget.group_box.setChecked(True)
    widget.clear_checkbox.setChecked(False)

    actual_update_result = widget.updateTag([song])

    assert actual_update_result == expected_update_result

    assert song.getValue(tag) == info["expected_items"]


def test_EditBulkPeopleWidget_updateTag_multiple_actions(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests calling updateTag with multiple fields filled."""
    initial_widget_items = [
        ["ExistingRole", "ExistingPerson"],
        ["RoleToRemove", "PersonToRemove"],
    ]
    _, tag, widget = _createWidget(qtbot, initial_widget_items)

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
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, mock_settings: MagicMock
) -> None:
    """Tests that the people widget re-displays the original values on reset."""
    initial_widget_data = [["Role1", "Person1"], ["Role2", "Person2"]]
    _, __, widget = _createWidget(qtbot, initial_widget_data)

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
