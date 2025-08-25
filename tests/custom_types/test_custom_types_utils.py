import pytest

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
    return [
        SongTag(display_name="Track", id3_key="TRCK"),
        SongTag(display_name="Title", id3_key="TIT2"),
        SongTag(display_name="Artist", id3_key="TPE1"),
    ]


def test_mapTag(tags: list[SongTag]) -> None:
    result1: SongTag | None = mapTag("Track", tags)
    assert result1 is not None
    assert result1.display_name == "Track"
    result2: SongTag | None = mapTag("Album", tags)
    assert result2 is None


def test_mapKey(tags: list[SongTag]) -> None:
    result1: SongTag | None = mapKey("TIT2", tags)
    assert result1 is not None
    assert result1.display_name == "Title"
    result2: SongTag | None = mapKey("TIT3", tags)
    assert result2 is None


def test_mapOptionalTag(tags: list[SongTag]) -> None:
    result1: SongTag | None = mapOptionalTag("Sort Artist", "Artist", tags)
    assert result1 is not None
    assert result1.display_name == "Artist"
    result2: SongTag | None = mapOptionalTag("Label", "Publisher", tags)
    assert result2 is None


def test_valueToString() -> None:
    separator = "; "
    string_value = "Some Title"
    list_value: list[str] = ["Person 1", "Person 2"]
    people_value: list[list[str]] = [["role1", "Person 1"], ["role2", "Person 2"]]
    extra_people_value: list[list[str]] = [
        ["role1", "Person 1"],
        ["role2", "Person 2"],
        ["role3", "Person 3", "extra"],
    ]
    assert valueToString(string_value, separator) == "Some Title"
    assert valueToString(list_value, separator) == "Person 1; Person 2"
    assert valueToString(people_value, separator) == "role1:Person 1; role2:Person 2"
    assert (
        valueToString(extra_people_value, separator) == "role1:Person 1; role2:Person 2"
    )


def test_toTag(tags: list[SongTag]) -> None:
    result1: SongTag | None = toTag("TIT2", tags)
    assert result1 is not None
    assert result1.id3_key == "TIT2"
    result2: SongTag | None = toTag("Artist", tags)
    assert result2 is not None
    assert result2.display_name == "Artist"
    result3: SongTag | None = toTag("TIPL", tags)
    assert result3 is None


def test_toTag_existing(tags: list[SongTag]) -> None:
    created_tag: SongTag | None = toTag("TIT2", tags)
    assert created_tag is not None
    assert created_tag.id3_key == "TIT2"
    assert toTag(created_tag, tags) is created_tag
