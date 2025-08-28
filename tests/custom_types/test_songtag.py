from typing import TypedDict, cast, Literal

from mutagen.id3 import ID3
import pytest

from music_modify.custom_types import constants
from music_modify.custom_types.enums import TagType
from music_modify.custom_types.songtag import SongTag


class _TestTag(TypedDict):
    single: SongTag
    multiple: SongTag
    people: SongTag


class _TestTagValue(TypedDict):
    single: list[str]
    multiple: list[str]
    people: list[list[str]]


@pytest.fixture
def single_value() -> list[str]:
    return ["Some Title"]


@pytest.fixture
def multiple_value() -> list[str]:
    return ["Some Person", "Another Person"]


@pytest.fixture
def people_value() -> list[list[str]]:
    return [["role1", "Person 1"], ["role2", "Person 2"]]


@pytest.fixture
def tag_values(
    single_value: list[str],
    multiple_value: list[str],
    people_value: list[list[str]],
) -> _TestTagValue:
    return {
        "single": single_value,
        "multiple": multiple_value,
        "people": people_value,
    }


@pytest.fixture
def single_tag() -> SongTag:
    return SongTag(id3_key="TIT2", display_name="Title")


@pytest.fixture
def multiple_tag() -> SongTag:
    return SongTag(id3_key="TCOM", display_name="Composer")


@pytest.fixture
def people_tag() -> SongTag:
    return SongTag(id3_key="TIPL", display_name="Involved People")


@pytest.fixture
def tag_types(
    single_tag: SongTag,
    multiple_tag: SongTag,
    people_tag: SongTag,
) -> _TestTag:
    return {
        "single": single_tag,
        "multiple": multiple_tag,
        "people": people_tag,
    }


def test_id3_key(single_tag: SongTag) -> None:
    assert single_tag.id3_key == "TIT2"


def test_display_name(single_tag: SongTag) -> None:
    assert single_tag.display_name == "Title"


def test_frame_type(tag_types: _TestTag) -> None:
    assert tag_types["single"].frame_type == TagType.Text
    assert tag_types["multiple"].frame_type == TagType.Text
    assert tag_types["people"].frame_type == TagType.People


def test_allow_multiple(tag_types: _TestTag) -> None:
    assert not tag_types["single"].allow_multiple
    assert tag_types["multiple"].allow_multiple
    assert not tag_types["people"].allow_multiple


def test_len(tag_types: _TestTag) -> None:
    assert len(tag_types["single"]) == 1
    assert len(tag_types["multiple"]) == 1
    assert len(tag_types["people"]) == constants.PEOPLE_COL_COUNT


def test_hasTag(tag_types: _TestTag) -> None:
    song = ID3()
    assert not tag_types["single"].hasTag(song)
    assert not tag_types["multiple"].hasTag(song)
    assert not tag_types["people"].hasTag(song)


def test_generateFrame_hasTag(single_tag: SongTag) -> None:
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.generateFrame(song)
    assert single_tag.hasTag(song)
    # Ensure that making it again doesn't lead to issues
    single_tag.generateFrame(song)


def test_setTag(tag_types: _TestTag, tag_values: _TestTagValue) -> None:
    song = ID3()
    for key in "single", "multiple", "people":
        key = cast(Literal["single", "multiple", "people"], key)
        tag_types[key].setTag(song, tag_values[key])
        assert tag_types[key].getTag(song) == tag_values[key]


def test_removeTag(single_tag: SongTag, single_value: list[str]) -> None:
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.hasTag(song)
    single_tag.removeTag(song)
    assert not single_tag.hasTag(song)


def test_getTag(
    single_tag: SongTag,
    multiple_tag: SongTag,
    single_value: list[str],
) -> None:
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.getTag(song) == single_value
    assert not multiple_tag.hasTag(song)
    assert multiple_tag.getTag(song) is None


def test_getValue(tag_types: _TestTag, tag_values: _TestTagValue) -> None:
    song = ID3()
    for key in "single", "multiple", "people":
        key = cast(Literal["single", "multiple", "people"], key)
        assert not tag_types[key].hasTag(song)
        tag_types[key].setTag(song, tag_values[key])
        if key == "single":
            assert tag_types[key].getValue(song) == tag_values[key][0]
        else:
            assert tag_types[key].getValue(song) == tag_values[key]


def test_SongTag_repr(single_tag: SongTag) -> None:
    assert repr(single_tag) == "SongTag(TIT2, Title)"
    assert repr(single_tag) == "SongTag(display_name='Title', id3_key='TIT2')"


def test_SongTag_eq(single_tag: SongTag, multiple_tag: SongTag) -> None:
    assert single_tag != multiple_tag
    assert single_tag == SongTag(id3_key="TIT2", display_name="Title")
    assert single_tag != "TIT2"


def test_SongTag_hash(single_tag: SongTag) -> None:
    assert hash(single_tag) == hash((single_tag.id3_key, single_tag.display_name))


def test_frame_type_unknown() -> None:
    invalid_tag = SongTag(id3_key="ABCD", display_name="Invalid")
    assert invalid_tag.frame_type == TagType.Text


def test_frame_type_others() -> None:
    binary_tag = SongTag(id3_key="MCDI", display_name="TOC from CD")
    assert binary_tag.frame_type == TagType.Data
    url_tag = SongTag(id3_key="WCOP", display_name="Copyright")
    assert url_tag.frame_type == TagType.Url


def test_generateFrame_custom() -> None:
    song = ID3()
    custom_tag = SongTag(id3_key="TXXX:TEMPO", display_name="Tempo")
    # Ensure this runs without errors, nothing to assert
    custom_tag.generateFrame(song)
