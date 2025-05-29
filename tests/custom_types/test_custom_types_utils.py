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
def tags():
    return [
        SongTag(display_name="Track", id3_key="TRCK"),
        SongTag(display_name="Title", id3_key="TIT2"),
        SongTag(display_name="Artist", id3_key="TPE1"),
    ]


def test_mapTag(tags: list[SongTag]):
    result1 = mapTag("Track", tags)
    assert result1 is not None and result1.display_name == "Track"
    result2 = mapTag("Album", tags)
    assert result2 is None


def test_mapKey(tags: list[SongTag]):
    result1 = mapKey("TIT2", tags)
    assert result1 is not None and result1.display_name == "Title"
    result2 = mapKey("TIT3", tags)
    assert result2 is None


def test_mapOptionalTag(tags: list[SongTag]):
    result1 = mapOptionalTag("Sort Artist", "Artist", tags)
    assert result1 is not None and result1.display_name == "Artist"
    result2 = mapOptionalTag("Label", "Publisher", tags)
    assert result2 is None


def test_valueToString():
    separator = "; "
    string_value = "Some Title"
    list_value = ["Person 1", "Person 2"]
    people_value = [["role1", "Person 1"], ["role2", "Person 2"]]
    assert valueToString(string_value, separator) == "Some Title"
    assert valueToString(list_value, separator) == "Person 1; Person 2"
    assert valueToString(people_value, separator) == "role1:Person 1; role2:Person 2"


def test_toTag(tags: list[SongTag]):
    result1 = toTag("TIT2", tags)
    assert result1 is not None and result1.id3_key == "TIT2"
    result2 = toTag("Artist", tags)
    assert result2 is not None and result2.display_name == "Artist"
    result3 = toTag("TIPL", tags)
    assert result3 is None
