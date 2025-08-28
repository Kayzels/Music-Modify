"""Tests for SongTag."""

from typing import TypedDict
from unittest.mock import MagicMock

from mutagen import id3
from mutagen.id3 import ID3, Frames
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
    """Fixture that returns a value for a tag that stores single values."""
    return ["Some Title"]


@pytest.fixture
def multiple_value() -> list[str]:
    """Fixture that returns a value for a tag that stores multiple values."""
    return ["Some Person", "Another Person"]


@pytest.fixture
def people_value() -> list[list[str]]:
    """Fixture that returns a value for a tag that stores people values."""
    return [["role1", "Person 1"], ["role2", "Person 2"]]


@pytest.fixture
def tag_values(
    single_value: list[str],
    multiple_value: list[str],
    people_value: list[list[str]],
) -> _TestTagValue:
    """Fixture that returns all of the value types."""
    return {
        "single": single_value,
        "multiple": multiple_value,
        "people": people_value,
    }


@pytest.fixture
def single_tag() -> SongTag:
    """Fixture that returns a tag that stores a single value."""
    return SongTag(id3_key="TIT2", display_name="Title")


@pytest.fixture
def multiple_tag() -> SongTag:
    """Fixture that returns a tag that stores multiple values."""
    return SongTag(id3_key="TCOM", display_name="Composer")


@pytest.fixture
def people_tag() -> SongTag:
    """Fixture that returns a tag that stores people values."""
    return SongTag(id3_key="TIPL", display_name="Involved People")


@pytest.fixture
def tag_types(
    single_tag: SongTag,
    multiple_tag: SongTag,
    people_tag: SongTag,
) -> _TestTag:
    """Fixture that returns all of the tag types."""
    return {
        "single": single_tag,
        "multiple": multiple_tag,
        "people": people_tag,
    }


def test_SongTag_id3_key(single_tag: SongTag) -> None:
    """Test that the id3 property gets set correctly."""
    assert single_tag.id3_key == "TIT2"


def test_SongTag_display_name(single_tag: SongTag) -> None:
    """Test that the display_name property gets set correctly."""
    assert single_tag.display_name == "Title"


def test_SongTag_frame_type(tag_types: _TestTag) -> None:
    """Test that the frame_type property gets set correctly."""
    assert tag_types["single"].frame_type == TagType.Text
    assert tag_types["multiple"].frame_type == TagType.Text
    assert tag_types["people"].frame_type == TagType.People


def test_SongTag_allow_multiple(tag_types: _TestTag) -> None:
    """Test that the allow_multiple property gets set correctly."""
    assert not tag_types["single"].allow_multiple
    assert tag_types["multiple"].allow_multiple
    assert not tag_types["people"].allow_multiple


def test_SongTag_len(tag_types: _TestTag) -> None:
    """Test that the length of tags gets set correctly.

    All tags except people tags should be 1, and people tags should have
    `PEOPLE_COL_COUNT`.
    """
    assert len(tag_types["single"]) == 1
    assert len(tag_types["multiple"]) == 1
    assert len(tag_types["people"]) == constants.PEOPLE_COL_COUNT


def test_SongTag_hasTag_empty_song_returns_False(tag_types: _TestTag) -> None:
    """Test that hasTag returns False for any tag when the song has no tags."""
    song = ID3()
    assert tag_types["single"].hasTag(song) is False
    assert tag_types["multiple"].hasTag(song) is False
    assert tag_types["people"].hasTag(song) is False


def test_SongTag_generateFrame_hasTag(
    single_tag: SongTag, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that hasTag returns True when a tag is generated."""
    song = ID3()
    assert single_tag.hasTag(song) is False
    single_tag.generateFrame(song)
    assert single_tag.hasTag(song) is True

    # Ensure that making it again doesn't re-add the tag
    mock_song_add = MagicMock()
    monkeypatch.setattr(ID3, "add", mock_song_add)
    single_tag.generateFrame(song)
    mock_song_add.assert_not_called()


def test_SongTag_setTag(tag_types: _TestTag, tag_values: _TestTagValue) -> None:
    """Test that setting values for all tag types works."""
    song = ID3()
    for key in "single", "multiple", "people":
        tag_types[key].setTag(song, tag_values[key])
        assert tag_types[key].getTag(song) == tag_values[key]


def test_SongTag_removeTag(single_tag: SongTag, single_value: list[str]) -> None:
    """Test that removing a tag from a song works."""
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.hasTag(song)
    single_tag.removeTag(song)
    assert not single_tag.hasTag(song)


def test_SongTag_getTag(
    single_tag: SongTag,
    multiple_tag: SongTag,
    single_value: list[str],
) -> None:
    """Test that getting the value for a tag type returns that value.

    Also tests that if the song doesn't have a Tag, None is returned.
    """
    song = ID3()
    assert not single_tag.hasTag(song)
    single_tag.setTag(song, single_value)
    assert single_tag.getTag(song) == single_value
    assert not multiple_tag.hasTag(song)
    assert multiple_tag.getTag(song) is None


def test_SongTag_getValue(tag_types: _TestTag, tag_values: _TestTagValue) -> None:
    """Test that getting values for a tag works when the tag is in the song."""
    song = ID3()
    for key in "single", "multiple", "people":
        assert not tag_types[key].hasTag(song)
        tag_types[key].setTag(song, tag_values[key])
        if key == "single":
            assert tag_types[key].getValue(song) == tag_values[key][0]
        else:
            assert tag_types[key].getValue(song) == tag_values[key]


def test_SongTag_repr(single_tag: SongTag) -> None:
    """Test that the string representation for a tag works correctly."""
    assert repr(single_tag) == "SongTag(display_name='Title', id3_key='TIT2')"


def test_SongTag_eq(single_tag: SongTag, multiple_tag: SongTag) -> None:
    """Test that SongTag equality works."""
    assert single_tag != multiple_tag
    assert single_tag == SongTag(id3_key="TIT2", display_name="Title")
    assert single_tag != SongTag(id3_key="TIT1", display_name="Title")
    assert single_tag != SongTag(id3_key="TIT2", display_name="Title 2")
    assert single_tag != "TIT2"


def test_SongTag_hash(single_tag: SongTag, multiple_tag: SongTag) -> None:
    """Test that hash only is the same value for tags that are the same."""
    assert hash(single_tag) == hash((single_tag.id3_key, single_tag.display_name))
    assert hash(single_tag) != hash(multiple_tag)


def test_SongTag_frame_type_unknown() -> None:
    """Test that any unknown id3_keys lead to Text frame types."""
    invalid_tag = SongTag(id3_key="ABCD", display_name="Invalid")
    assert invalid_tag.frame_type == TagType.Text


def test_SongTag_frame_type_others() -> None:
    """Test that strange id3 key tags still get the right frame type.

    These frames aren't used yet, but if the frame is known,
    we should be able to get the frame type.
    """
    binary_tag = SongTag(id3_key="MCDI", display_name="TOC from CD")
    assert binary_tag.frame_type == TagType.Data
    url_tag = SongTag(id3_key="WCOP", display_name="Copyright")
    assert url_tag.frame_type == TagType.Url


def test_SongTag_generateFrame_custom(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that generateFrame correctly creates frames for custom tags."""
    song = ID3()
    custom_tag = SongTag(id3_key="TXXX:TEMPO", display_name="Tempo")

    mock_add = MagicMock()
    monkeypatch.setattr(ID3, "add", mock_add)

    custom_tag.generateFrame(song)

    expected = Frames["TXXX"](id3.Encoding.UTF8, desc="TEMPO", text=[])

    mock_add.assert_called_with(expected)
