"""Tests for utilities related to custom types."""

from unittest.mock import MagicMock

import pytest

from music_modify.custom_types import utils
from music_modify.custom_types.songtag import SongTag
from music_modify.custom_types.utils import (
    mapKey,
    mapOptionalTag,
    mapTag,
    toTag,
    valueToString,
)


@pytest.fixture
def tags() -> list[SongTag]:
    """Fixture that creates a list of SongTag."""
    return [
        SongTag(display_name="Track", id3_key="TRCK"),
        SongTag(display_name="Title", id3_key="TIT2"),
        SongTag(display_name="Artist", id3_key="TPE1"),
    ]


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param(
            "Track", SongTag(display_name="Track", id3_key="TRCK"), id="existing_tag"
        ),
        pytest.param("Album", None, id="not_found"),
    ],
)
def test_mapTag(name: str, expected: SongTag | None, tags: list[SongTag]) -> None:
    """Test that mapTag returns a SongTag if it exists, or returns None."""
    assert mapTag(name, tags) == expected


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        pytest.param(
            "TIT2", SongTag(display_name="Title", id3_key="TIT2"), id="existing_tag"
        ),
        pytest.param("TIT3", None, id="not_found"),
    ],
)
def test_mapKey(key: str, expected: SongTag | None, tags: list[SongTag]) -> None:
    """Test that mapKey returns a SongTag if it exists, or returns None."""
    assert mapKey(key, tags) == expected


@pytest.mark.parametrize(
    ("tag_name", "optional_name", "expected"),
    [
        pytest.param(
            "Artist",
            "Album Artist",
            SongTag(display_name="Artist", id3_key="TPE1"),
            id="found_tag_name",
        ),
        pytest.param(
            "Sort Artist",
            "Artist",
            SongTag(display_name="Artist", id3_key="TPE1"),
            id="found_optional_name",
        ),
        pytest.param(
            "Label",
            "Publisher",
            None,
            id="not_found_tag",
        ),
    ],
)
def test_mapOptionalTag(
    tag_name: str, optional_name: str, expected: SongTag | None, tags: list[SongTag]
) -> None:
    """Test that mapOptionalTag finds tags if their name or optional_name exist."""
    assert mapOptionalTag(tag_name, optional_name, tags) == expected


@pytest.mark.parametrize(
    ("value", "separator", "expected"),
    [
        pytest.param(None, "; ", "", id="None_value"),
        pytest.param("", "; ", "", id="empty_value"),
        pytest.param("Some Title", "; ", "Some Title", id="single_value"),
        pytest.param(["List Value"], "; ", "List Value", id="list_value_single"),
        pytest.param(
            ["Person 1", "Person 2"],
            "; ",
            "Person 1; Person 2",
            id="list_value_multiple",
        ),
        pytest.param(
            [["role1", "Person 1"], ["role2", "Person 2"]],
            "; ",
            "role1:Person 1; role2:Person 2",
            id="people_value_valid",
        ),
        pytest.param(
            [
                ["role1", "Person 1"],
                ["role2", "Person 2"],
                ["role3", "Person 3", "extra"],
            ],
            "; ",
            "role1:Person 1; role2:Person 2",
            id="people_value_invalid_wrong_length_ignored",
        ),
    ],
)
def test_valueToString(
    value: str | list[str] | list[list[str]] | None, separator: str, expected: str
) -> None:
    """Tests that the value is converted correctly to a string in different cases."""
    assert valueToString(value, separator) == expected


@pytest.mark.parametrize(
    (
        "to_tag_value",
        "expected_tag",
        "map_key_return",
        "map_tag_return",
        "expected_map_key_call",
        "expected_map_tag_call",
    ),
    [
        pytest.param(
            "TIT2",
            SongTag(display_name="Title", id3_key="TIT2"),
            SongTag(display_name="Title", id3_key="TIT2"),
            None,
            True,
            False,
            id="string_id3_key_found",
        ),
        pytest.param(
            "Artist",
            SongTag(display_name="Artist", id3_key="TPE1"),
            None,
            SongTag(display_name="Artist", id3_key="TPE1"),
            True,
            True,
            id="string_display_name_found",
        ),
        pytest.param(
            "TIPL",
            None,
            None,
            None,
            True,
            True,
            id="string_not_found",
        ),
        pytest.param(
            SongTag(display_name="Title", id3_key="TIT2"),
            SongTag(display_name="Title", id3_key="TIT2"),
            SongTag(display_name="Title", id3_key="TIT2"),
            SongTag(display_name="Title", id3_key="TIT2"),
            False,
            False,
            id="from_existing_in_list",
        ),
        pytest.param(
            SongTag(display_name="Involved People", id3_key="TIPL"),
            None,
            None,
            None,
            False,
            False,
            id="from_existing_not_in_list",
        ),
    ],
)
def test_toTag(
    to_tag_value: str | SongTag,
    map_key_return: SongTag | None,
    map_tag_return: SongTag | None,
    expected_tag: SongTag | None,
    expected_map_tag_call: bool,
    expected_map_key_call: bool,
    tags: list[SongTag],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Tests that tags are created from id3 keys, display names, or existing tags.

    Args:
        to_tag_value: The value that should be passed to toTag
        map_key_return: The value that the mock mapKey method should return
        map_tag_return: The value that the mock mapTag method should return
        expected_tag: The expected result of the toTag method
        expected_map_tag_call: Whether mapTag is expected to be called
        expected_map_key_call: Whether mapKey is expected to be called
        tags: The list of SongTags to consider for generating tags
        monkeypatch: Used for patching and mocking methods
    """
    mock_map_tag = MagicMock(return_value=map_tag_return)
    mock_map_key = MagicMock(return_value=map_key_return)
    monkeypatch.setattr(utils, "mapKey", mock_map_key)
    monkeypatch.setattr(utils, "mapTag", mock_map_tag)

    created_tag = toTag(to_tag_value, tags)
    assert created_tag == expected_tag

    if expected_map_key_call:
        mock_map_key.assert_called_once()
    else:
        mock_map_key.assert_not_called()

    if expected_map_tag_call:
        mock_map_tag.assert_called_once()
    else:
        mock_map_tag.assert_not_called()
