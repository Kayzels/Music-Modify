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


def test_mapTag(tags: list[SongTag]) -> None:
    """Test that mapTag returns a SongTag if it exists, or returns None."""
    result1: SongTag | None = mapTag("Track", tags)
    assert result1 is not None
    assert result1.display_name == "Track"
    result2: SongTag | None = mapTag("Album", tags)
    assert result2 is None


def test_mapKey(tags: list[SongTag]) -> None:
    """Test that mapKey returns a SongTag if it exists, or returns None."""
    result1: SongTag | None = mapKey("TIT2", tags)
    assert result1 is not None
    assert result1.display_name == "Title"
    result2: SongTag | None = mapKey("TIT3", tags)
    assert result2 is None


def test_mapOptionalTag_no_fallback(tags: list[SongTag]) -> None:
    """Test that mapOptionalTag just returns the tag without fallback, if it exists."""
    result: SongTag | None = mapOptionalTag("Artist", "Album Artist", tags)
    assert result is not None
    assert result.display_name == "Artist"

    result1: SongTag | None = mapOptionalTag("Sort Artist", "Artist", tags)
    assert result1 is not None
    assert result1.display_name == "Artist"
    result2: SongTag | None = mapOptionalTag("Label", "Publisher", tags)
    assert result2 is None


def test_mapOptionalTag_fallback_exists(tags: list[SongTag]) -> None:
    """Test that mapOptionalTag uses optional_name as fallback, when found."""
    result: SongTag | None = mapOptionalTag("Sort Artist", "Artist", tags)
    assert result is not None
    assert result.display_name == "Artist"


def test_mapOptionalTag_fallback_not_exists(tags: list[SongTag]) -> None:
    """Test that mapOptionalTag returns None when fallback not found."""
    result: SongTag | None = mapOptionalTag("Label", "Publisher", tags)
    assert result is None


def test_valueToString_empty() -> None:
    """Tests that the empty string is returned when given empty values."""
    separator = "; "
    assert valueToString(None, separator) == ""
    assert valueToString("", separator) == ""


def test_valueToString_single() -> None:
    """Tests that if only a single value exists, no separator is added."""
    separator = "; "
    value = "Some Title"
    assert valueToString(value, separator) == "Some Title"


def test_valueToString_list_one_item() -> None:
    """Tests that lists with only one item are converted without separators."""
    separator = "; "
    value = ["List Value"]
    assert valueToString(value, separator) == "List Value"


def test_valueToString_list_multiple_items() -> None:
    """Tests that lists with multiple items are converted with separators."""
    separator = "; "
    value: list[str] = ["Person 1", "Person 2"]
    assert valueToString(value, separator) == "Person 1; Person 2"


def test_valueToString_people_valid() -> None:
    """Tests that people values of the correct length are converted with separators."""
    separator = "; "
    value: list[list[str]] = [["role1", "Person 1"], ["role2", "Person 2"]]
    assert valueToString(value, separator) == "role1:Person 1; role2:Person 2"


def test_valueToString_people_invalid() -> None:
    """Tests that people values of the incorrect length are ignored."""
    separator = "; "
    value: list[list[str]] = [
        ["role1", "Person 1"],
        ["role2", "Person 2"],
        ["role3", "Person 3", "extra"],
    ]
    assert valueToString(value, separator) == "role1:Person 1; role2:Person 2"


def test_toTag_string_id3(tags: list[SongTag]) -> None:
    """Tests that tags are created from an id3 key string, when valid."""
    result: SongTag | None = toTag("TIT2", tags)
    assert result is not None
    assert result.id3_key == "TIT2"


def test_toTag_string_display_name(tags: list[SongTag]) -> None:
    """Tests that tags are created from a display name string, when valid."""
    result: SongTag | None = toTag("Artist", tags)
    assert result is not None
    assert result.display_name == "Artist"


def test_toTag_string_not_found(
    tags: list[SongTag], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tests that None is returned when a Tag cannot be found or created."""
    mock_map_key = MagicMock(return_value=None)
    mock_map_tag = MagicMock(return_value=None)
    monkeypatch.setattr(utils, "mapKey", mock_map_key)
    monkeypatch.setattr(utils, "mapTag", mock_map_tag)

    result: SongTag | None = toTag("TIPL", tags)

    assert result is None
    mock_map_key.assert_called_once()
    mock_map_tag.assert_called_once()


def test_toTag_from_existing(
    tags: list[SongTag], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tests that an existing tag is just returned if already existing."""
    created_tag: SongTag | None = toTag("TIT2", tags)
    assert created_tag is not None

    mock_map_key = MagicMock()
    mock_map_tag = MagicMock()
    monkeypatch.setattr(utils, "mapKey", mock_map_key)
    monkeypatch.setattr(utils, "mapTag", mock_map_tag)

    assert toTag(created_tag, tags) is created_tag

    mock_map_key.assert_not_called()
    mock_map_tag.assert_not_called()
