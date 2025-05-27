import pytest
from mutagen.id3 import ID3
from music_modify.custom_types.enums import TagType
from music_modify.custom_types.songtag import SongTag


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
def single_tag() -> SongTag:
    return SongTag(id3_key="TIT2", display_name="Title")


@pytest.fixture
def multiple_tag() -> SongTag:
    return SongTag(id3_key="TCOM", display_name="Composer")


@pytest.fixture
def people_tag() -> SongTag:
    return SongTag(id3_key="TIPL", display_name="Involved People")


def test_id3_key(single_tag: SongTag):
    assert single_tag.id3_key == "TIT2"


def test_display_name(single_tag: SongTag):
    assert single_tag.display_name == "Title"


def test_frame_type(single_tag: SongTag, multiple_tag: SongTag, people_tag: SongTag):
    assert single_tag.frame_type == TagType.Text
    assert multiple_tag.frame_type == TagType.Text
    assert people_tag.frame_type == TagType.People


def test_allow_multiple(
    single_tag: SongTag, multiple_tag: SongTag, people_tag: SongTag
):
    assert not single_tag.allow_multiple
    assert multiple_tag.allow_multiple
    assert not people_tag.allow_multiple


def test_len(single_tag: SongTag, multiple_tag: SongTag, people_tag: SongTag):
    assert len(single_tag) == 1
    assert len(multiple_tag) == 1
    assert len(people_tag) == 2


def test_hasTag(single_tag: SongTag, multiple_tag: SongTag, people_tag: SongTag):
    song = ID3()
    assert not single_tag.hasTag(song)
    assert not multiple_tag.hasTag(song)
    assert not people_tag.hasTag(song)


def test_generateFrame_hasTag(single_tag: SongTag):
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.generateFrame(song)
    assert single_tag.hasTag(song)


def test_setTag(
    single_tag: SongTag,
    multiple_tag: SongTag,
    people_tag: SongTag,
    single_value: list[str],
    multiple_value: list[str],
    people_value: list[list[str]],
):
    song = ID3()
    single_tag.setTag(song, single_value)
    assert single_tag.getTag(song) == single_value
    multiple_tag.setTag(song, multiple_value)
    assert multiple_tag.getTag(song) == multiple_value
    people_tag.setTag(song, people_value)
    assert people_tag.getTag(song) == people_value


def test_removeTag(single_tag: SongTag, single_value: list[str]):
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.hasTag(song)
    single_tag.removeTag(song)
    assert not single_tag.hasTag(song)


def test_getTag(single_tag: SongTag, multiple_tag: SongTag, single_value: list[str]):
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.getTag(song) == single_value
    assert not multiple_tag.hasTag(song)
    assert multiple_tag.getTag(song) is None


def test_getValue(
    single_tag: SongTag,
    multiple_tag: SongTag,
    people_tag: SongTag,
    single_value: list[str],
    multiple_value: list[str],
    people_value: list[list[str]],
):
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.getValue(song) == single_value[0]

    multiple_tag.setTag(song, multiple_value)
    assert multiple_tag.getValue(song) == multiple_value

    people_tag.setTag(song, people_value)
    assert people_tag.getValue(song) == people_value
