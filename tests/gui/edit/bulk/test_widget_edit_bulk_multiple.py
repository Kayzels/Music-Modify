"""Tests for EditBulkMultipleWidget."""

# pyright: reportPrivateUsage = false, reportUnusedParameter = false

from typing import NotRequired, TypedDict
from unittest.mock import MagicMock, Mock

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.song import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.gui.edit.bulk.widget_edit_bulk_multiple import (
    EditBulkMultipleWidget,
    _MultipleLineEdit,
)


def test_MultipleLineEdit_items(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests that items are set properly for a _MultipleLineEdit."""
    text_to_split = "First, Second, Third"
    mock_prefs_settings = Mock()
    mock_prefs_settings.split_text_entered = ","
    monkeypatch.setattr("music_modify.prefs.prefs.settings", mock_prefs_settings)
    line_edit = _MultipleLineEdit(text_to_split)
    qtbot.addWidget(line_edit)
    assert line_edit.items == ["First", "Second", "Third"]


def test_EditBulkMultipleWidget_init_not_empty(qtbot: QtBot) -> None:
    """Test creating an EditBulkMultipleWidget when data is not empty."""
    parent = QWidget()
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, {"One"}, tag)
    qtbot.addWidget(widget)

    assert widget.items == ("One",)

    assert hasattr(widget, "remove_line")
    assert isinstance(widget.remove_line, QWidget)

    assert hasattr(widget, "add_line")
    assert isinstance(widget.add_line, QWidget)

    assert widget.remove_line.all_items == ("One",)


def _createWidget(
    qtbot: QtBot, items: set[str] | None = None
) -> tuple[QWidget, SongTag, EditBulkMultipleWidget]:
    if not items:
        items = set()
    parent = QWidget()
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, items, tag)
    qtbot.addWidget(widget)

    return parent, tag, widget


@pytest.mark.parametrize(
    "songs", [pytest.param([], id="empty_list"), pytest.param([Song], id="single_song")]
)
def test_EditBulkMultipleWidget_updateTag_group_box_unchecked(
    qtbot: QtBot, songs: list[Song]
) -> None:
    """Tests that updating a tag when the checkbox isn't checked makes no changes."""
    _, __, widget = _createWidget(qtbot, {"One"})

    widget.group_box.setChecked(False)

    assert not widget.updateTag(songs)


def test_EditBulkMultipleWidget_adds_to_line(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests typing a value in the lines updates line values, but not widget ones.

    The widget should only store the values actually stored in all the songs.
    If an item is typed, but the songs aren't updated,
    the widget values shouldn't change.
    """
    _, __, widget = _createWidget(qtbot, {"One"})

    widget.add_line.setText("Value to Add")
    widget.remove_line.setText("Value to Remove")

    assert widget.add_line.items == ["Value to Add"]
    assert widget.remove_line.values == ["Value to Remove"]
    assert widget.items == ("One",)


def test_EditBulkMultipleWidget_updateTag_clear_checkbox_checked(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests that tags are removed if updateTag is called with clear checked."""
    _, tag, widget = _createWidget(qtbot)

    widget.group_box.setChecked(True)

    song1 = Song()
    song1.setTag(tag, ["One Composer"])
    song2 = Song()
    song2.setTag(tag, ["One Composer", "Another Composer"])
    songs = [song1, song2]

    widget.clear_checkbox.setChecked(True)

    assert widget.updateTag(songs) == {song1, song2}
    assert not song1.hasTag(tag)
    assert not song2.hasTag(tag)


def test_EditBulkMultipleWidget_updateTag_empty_add_empty_remove(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests adding or removing empty values doesn't change the song value."""
    _, tag, widget = _createWidget(qtbot)

    widget.group_box.setChecked(True)

    song1 = Song()
    song1.setTag(tag, ["One Composer"])
    song2 = Song()
    song2.setTag(tag, ["One Composer", "Another Composer"])
    songs = [song1, song2]

    widget.add_line.setText("")
    assert len(widget.add_line.items) == 0
    widget.remove_line.setText("")
    assert len(widget.remove_line.values) == 0

    assert not widget.updateTag(songs)

    assert song1.getValue(tag) == ["One Composer"]
    assert song2.getValue(tag) == ["One Composer", "Another Composer"]


def test_EditBulkMultipleWidget_updateTag_single_song_empty_add(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests adding values to a song that doesn't have the tag at start."""
    _, tag, widget = _createWidget(qtbot)

    widget.group_box.setChecked(True)

    song1 = Song()

    assert widget.items == ()
    assert widget.remove_line.all_items == ()

    widget.add_line.setText("New Name")
    assert widget.add_line.items == ["New Name"]

    assert not song1.hasTag(tag)
    assert widget.updateTag([song1]) == {song1}

    assert song1.getValue(tag) == ["New Name"]

    assert widget.items == ("New Name",)
    assert widget.remove_line.all_items == ("New Name",)


def test_EditBulkMultipleWidget_updateTag_single_song_and_widget_same(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests that setting text for adding a value already present doesn't add it."""
    _, tag, widget = _createWidget(qtbot)

    widget.group_box.setChecked(True)

    song = Song()
    song.setTag(tag, ["Some Name", "And Another"])
    songs = [song]

    assert isinstance(song.getValue(tag), list)

    widget.add_line.setText("Some Name")
    assert widget.add_line.items == ["Some Name"]

    assert not widget.updateTag(songs)
    assert song.getValue(tag) == ["Some Name", "And Another"]


def test_EditBulkMultipleWidget_updateTag_single_widget_has_extra(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests that any items not in the song are correctly added.

    Tests that the items that are already present aren't added again,
    but when the song doesn't have one of the items, it is added.
    """
    _, tag, widget = _createWidget(qtbot)

    widget.group_box.setChecked(True)

    song = Song()
    song.setTag(tag, ["Some Name"])

    assert isinstance(song.getValue(tag), list)

    widget.add_line.setText("Some Name, And Another Name")
    assert widget.add_line.items == ["Some Name", "And Another Name"]

    assert widget.updateTag([song]) == {song}
    assert song.getValue(tag) == ["Some Name", "And Another Name"]


class _SongCase(TypedDict):
    initial_value: list[str] | None
    expected_updated: bool
    expected_final_value: list[str]
    widget_text: NotRequired[str]
    id: str


_SONG_CASES: list[_SongCase] = [
    {
        "initial_value": ["Some Name"],
        "expected_updated": True,
        "expected_final_value": ["Some Name", "Another Name"],
        "id": "first_name",
    },
    {
        "initial_value": ["Some Name", "Another Name"],
        "expected_updated": False,
        "expected_final_value": ["Some Name", "Another Name"],
        "id": "both_names",
    },
    {
        "initial_value": ["Another Name"],
        "expected_updated": True,
        "expected_final_value": ["Another Name", "Some Name"],
        "id": "last_name",
    },
    {
        "initial_value": None,
        "expected_updated": True,
        "expected_final_value": ["Some Name", "Another Name"],
        "id": "no_name",
    },
    {
        "initial_value": ["Not a Name"],
        "expected_updated": True,
        "expected_final_value": ["Not a Name", "Some Name", "Another Name"],
        "id": "other_name",
    },
]


@pytest.mark.parametrize(
    ("value", "expected_updated", "expected_value"),
    [
        pytest.param(
            case["initial_value"],
            case["expected_updated"],
            case["expected_final_value"],
            id=case["id"],
        )
        for case in _SONG_CASES
    ],
)
def test_EditBulkMultipleWidget_updateTag_songs_param(
    qtbot: QtBot,
    value: list[str] | None,
    expected_updated: bool,
    expected_value: list[str],
    mock_settings: MagicMock,
) -> None:
    """Tests that updateTag changes values that it should."""
    _, tag, widget = _createWidget(qtbot)

    widget.group_box.setChecked(True)

    song = Song()
    if value is not None:
        song.setTag(tag, value)
    songs: list[Song] = [song]

    widget.add_line.setText("Some Name, Another Name")
    assert widget.add_line.items == ["Some Name", "Another Name"]

    expected_update_result = {song} if expected_updated else set()

    assert widget.updateTag(songs) == expected_update_result
    assert song.getValue(tag) == expected_value


def test_EditBulkMultipleWidget_updateTag_multiple_add(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests adding values to multiple songs, with different conditions."""
    _, tag, widget = _createWidget(qtbot)

    widget.group_box.setChecked(True)
    songs: list[Song] = []
    expected_updated_songs: set[Song] = set()
    expected_final_values: list[list[str]] = []

    for case in _SONG_CASES:
        song = Song()
        if (value := case["initial_value"]) is not None:
            song.setTag(tag, value)
        songs.append(song)
        if case["expected_updated"]:
            expected_updated_songs.add(song)
        expected_final_values.append(case["expected_final_value"])

    widget.add_line.setText("Some Name, Another Name")
    assert widget.add_line.items == ["Some Name", "Another Name"]

    assert widget.updateTag(songs) == expected_updated_songs
    for i, song in enumerate(songs):
        assert song.getValue(tag) == expected_final_values[i]


def test_EditBulkMultipleWidget_updateTag_song_empty_remove(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests that removing tag values for songs that don't have that tag works.

    The tag shouldn't be added, and updateTag should return an empty set.
    """
    _, tag, widget = _createWidget(qtbot)

    widget.group_box.setChecked(True)

    song = Song()
    assert not song.hasTag(tag)

    widget.remove_line.setText("First Name")

    assert not widget.updateTag([song])
    assert not song.hasTag(tag)


_REMOVE_CASES: list[_SongCase] = [
    {
        "initial_value": ["Song Value"],
        "widget_text": "Line Value",
        "expected_final_value": ["Song Value"],
        "expected_updated": False,
        "id": "song_value_diff_line_value",
    },
    {
        "initial_value": ["Song Value"],
        "widget_text": "Song Value",
        "expected_final_value": [],
        "expected_updated": True,
        "id": "song_value_same_line_value_only",
    },
    {
        "initial_value": ["Song Value"],
        "widget_text": "Song Value, Extra Value",
        "expected_final_value": [],
        "expected_updated": True,
        "id": "song_value_same_line_value_line_extra",
    },
    {
        "initial_value": ["Song Value", "Extra Value"],
        "widget_text": "Song Value",
        "expected_final_value": ["Extra Value"],
        "expected_updated": True,
        "id": "song_value_same_line_value_song_extra",
    },
    {
        "initial_value": ["Song Value", "Extra Value", "Another Value", "Even More"],
        "widget_text": "Song Value, Another Value",
        "expected_final_value": ["Extra Value", "Even More"],
        "expected_updated": True,
        "id": "song_value_same_line_value_song_extra_multiple",
    },
]


@pytest.mark.parametrize(
    ("song_initial_values", "widget_text", "expected_updated", "expected_final_value"),
    [
        pytest.param(
            case["initial_value"],
            case.get("widget_text", ""),
            case["expected_updated"],
            case["expected_final_value"],
            id=case["id"],
        )
        for case in _REMOVE_CASES
    ],
)
def test_EditBulkMultipleWidget_updateTag_remove_param(
    qtbot: QtBot,
    song_initial_values: list[str],
    widget_text: str,
    expected_updated: bool,
    expected_final_value: list[str],
    mock_settings: MagicMock,
) -> None:
    """Tests removing tag values in different conditions.

    If the remove value isn't in the song, the song shouldn't be updated.

    If the remove value is the only value in the song, it should be removed
    (but not the tag).

    If the remove value is in the song, but not the only value, remove the value.
    """
    _, tag, widget = _createWidget(qtbot)

    widget.group_box.setChecked(True)

    song = Song()
    song.setTag(tag, song_initial_values)

    widget.remove_line.setText(widget_text)

    expected_updated_result = {song} if expected_updated else set()
    assert widget.updateTag([song]) == expected_updated_result
    assert song.getValue(tag) == expected_final_value


def test_EditBulkMultipleWidget_updateTag_add_remove(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Tests that both adding and removing values works if done together.

    Items should be added, and then removed.
    """
    _, tag, widget = _createWidget(qtbot, set())

    widget.group_box.setChecked(True)

    song = Song()
    song.setTag(tag, ["Song Value", "Extra Value"])

    widget.add_line.setText("New Value, And Another, Removed")
    assert widget.add_line.items == ["New Value", "And Another", "Removed"]

    widget.remove_line.setText("Song Value, Another Value, Removed")
    assert widget.remove_line.values == ["Song Value", "Another Value", "Removed"]

    assert widget.updateTag([song]) == {song}
    assert song.getValue(tag) == ["Extra Value", "New Value", "And Another"]


def test_EditBulkMultipleWidget_resetView(
    qtbot: QtBot, mock_settings: MagicMock
) -> None:
    """Test that resetView restores the original state for the widget."""
    _, tag, widget = _createWidget(qtbot, set())

    widget.group_box.setChecked(True)

    song = Song()
    song.setTag(tag, ["Song Value", "Extra Value"])

    widget.add_line.setText("Another Value")
    widget.remove_line.setText("Remove Item")

    assert len(widget.items) == 0

    widget._resetView()

    assert widget.add_line.text() == ""
    assert widget.add_line.items == []
    assert widget.remove_line.text() == ""
    assert widget.remove_line.values == []
    assert not widget.clear_checkbox.isChecked()
    assert not widget.group_box.isChecked()
