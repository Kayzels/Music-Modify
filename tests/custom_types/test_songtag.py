"""Tests for SongTag."""

from typing import Any
from unittest.mock import MagicMock

from mutagen import id3
from mutagen.id3 import ID3, Frames
import pytest
from pytest_lazy_fixtures import lf

from music_modify.custom_types import constants
from music_modify.custom_types.enums import EditorType, TagType
from music_modify.custom_types.songtag import SongTag


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
def single_tag() -> SongTag:
    """Fixture that returns a tag that stores a single value."""
    return SongTag(
        id3_key="TIT2", display_name="Title", editor_type=EditorType.SingleText
    )


@pytest.fixture
def multiple_tag() -> SongTag:
    """Fixture that returns a tag that stores multiple values."""
    return SongTag(
        id3_key="TCOM", display_name="Composer", editor_type=EditorType.MultipleText
    )


@pytest.fixture
def people_tag() -> SongTag:
    """Fixture that returns a tag that stores people values."""
    return SongTag(
        id3_key="TIPL",
        display_name="Involved People",
        editor_type=EditorType.PeopleValue,
    )


@pytest.mark.parametrize(
    ("tag", "expected"),
    [pytest.param(SongTag(display_name="Title", id3_key="TIT2"), "TIT2", id="single")],
)
def test_SongTag_id3_key(tag: SongTag, expected: str) -> None:
    """Test that the id3 property gets set correctly."""
    assert tag.id3_key == expected


@pytest.mark.parametrize(
    ("tag", "expected"),
    [pytest.param(SongTag(display_name="Title", id3_key="TIT2"), "Title", id="single")],
)
def test_SongTag_display_name(tag: SongTag, expected: str) -> None:
    """Test that the display_name property gets set correctly."""
    assert tag.display_name == expected


@pytest.mark.parametrize(
    ("id3_key", "display_name", "editor_type", "expected"),
    [
        pytest.param(
            "TIT2",
            "Title",
            None,
            EditorType.SingleText,
            id="single_no_editor_type_sent",
        ),
        pytest.param(
            "TIT2",
            "Title",
            EditorType.Automatic,
            EditorType.SingleText,
            id="single_auto_editor_type_sent",
        ),
        pytest.param(
            "TIT2",
            "Title",
            EditorType.SingleText,
            EditorType.SingleText,
            id="single_single_editor_type_sent",
        ),
        pytest.param(
            "TIT2",
            "Title",
            EditorType.MultipleText,
            EditorType.MultipleText,
            id="single_multiple_editor_type_sent_overrides_default",
        ),
        pytest.param(
            "TCOM",
            "Composer",
            None,
            EditorType.MultipleText,
            id="multiple_no_editor_type_sent",
        ),
        pytest.param(
            "TCOM",
            "Composer",
            EditorType.Automatic,
            EditorType.MultipleText,
            id="multiple_auto_editor_type_sent",
        ),
        pytest.param(
            "TCOM",
            "Composer",
            EditorType.MultipleText,
            EditorType.MultipleText,
            id="multiple_multiple_editor_type_sent",
        ),
        pytest.param(
            "TCOM",
            "Composer",
            EditorType.SingleText,
            EditorType.SingleText,
            id="multiple_single_editor_type_sent_overrides_default",
        ),
        pytest.param(
            "TIPL",
            "Involved People",
            None,
            EditorType.PeopleValue,
            id="people_no_editor_type_sent",
        ),
        pytest.param(
            "TIPL",
            "Involved People",
            EditorType.Automatic,
            EditorType.PeopleValue,
            id="people_auto_editor_type_sent",
        ),
        pytest.param(
            "TIPL",
            "Involved People",
            EditorType.PeopleValue,
            EditorType.PeopleValue,
            id="people_people_editor_type_sent",
        ),
        pytest.param(
            "TIPL",
            "Involved People",
            EditorType.MultipleText,
            EditorType.MultipleText,
            id="people_multiple_editor_type_sent_overrides_default",
        ),
    ],
)
def test_SongTag_editor_type(
    id3_key: str,
    display_name: str,
    editor_type: EditorType | None,
    expected: EditorType,
) -> None:
    """Tests that editor_type property gets set correctly."""
    if editor_type is None:
        tag = SongTag(display_name=display_name, id3_key=id3_key)
    else:
        tag = SongTag(
            display_name=display_name, id3_key=id3_key, editor_type=editor_type
        )

    assert tag.editor_type == expected


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        pytest.param(lf("single_tag"), TagType.Text, id="single_tag_text"),
        pytest.param(lf("multiple_tag"), TagType.Text, id="multiple_tag_text"),
        pytest.param(lf("people_tag"), TagType.People, id="people_tag_people"),
        pytest.param(
            SongTag(id3_key="MCDI", display_name="TOC from CD"),
            TagType.Data,
            id="data_frame",
        ),
        pytest.param(
            SongTag(id3_key="WCOP", display_name="Copyright"),
            TagType.Url,
            id="url_frame",
        ),
        pytest.param(
            SongTag(id3_key="ABCD", display_name="Invalid"),
            TagType.Text,
            id="unknown_frame_is_text",
        ),
    ],
)
def test_SongTag_frame_type(tag: SongTag, expected: TagType) -> None:
    """Test that the frame_type property gets set correctly."""
    assert tag.frame_type == expected


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        pytest.param(lf("single_tag"), 1, id="single_tag_len_1"),
        pytest.param(lf("multiple_tag"), 1, id="multiple_tag_len_1"),
        pytest.param(
            lf("people_tag"), constants.PEOPLE_COL_COUNT, id="people_tag_len_2"
        ),
    ],
)
def test_SongTag_len(tag: SongTag, expected: int) -> None:
    """Test that the length of tags gets set correctly.

    All tags except people tags should be 1, and people tags should have
    `PEOPLE_COL_COUNT`.
    """
    assert len(tag) == expected


@pytest.mark.parametrize(
    "tag",
    [
        pytest.param(lf("single_tag"), id="single_tag"),
        pytest.param(lf("multiple_tag"), id="multiple_tag"),
        pytest.param(lf("people_tag"), id="people_tag"),
    ],
)
def test_SongTag_hasTag_empty_song_returns_False(tag: SongTag) -> None:
    """Test that hasTag returns False for any tag when the song has no tags."""
    song = ID3()
    assert tag.hasTag(song) is False


@pytest.mark.parametrize(
    "tag",
    [
        pytest.param(lf("single_tag"), id="single_tag_added"),
        pytest.param(lf("multiple_tag"), id="multiple_tag_added"),
        pytest.param(lf("people_tag"), id="people_tag_added"),
    ],
)
def test_SongTag_generateFrame_hasTag(
    tag: SongTag, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that hasTag returns True when a tag is generated."""
    song = ID3()
    assert tag.hasTag(song) is False
    tag.generateFrame(song)
    assert tag.hasTag(song) is True

    # Ensure that making it again doesn't re-add the tag
    mock_song_add = MagicMock()
    monkeypatch.setattr(ID3, "add", mock_song_add)
    tag.generateFrame(song)
    mock_song_add.assert_not_called()


@pytest.mark.parametrize(
    ("tag", "value"),
    [
        pytest.param(lf("single_tag"), lf("single_value"), id="single_tag_set"),
        pytest.param(lf("multiple_tag"), lf("multiple_value"), id="multiple_tag_set"),
        pytest.param(lf("people_tag"), lf("people_value"), id="people_tag_set"),
    ],
)
def test_SongTag_setTag(tag: SongTag, value: list[str] | list[list[str]]) -> None:
    """Test that setting values for all tag types works."""
    song = ID3()
    tag.setTag(song, value)
    assert tag.getTag(song) == value


@pytest.mark.parametrize(
    ("tag", "value"),
    [
        pytest.param(lf("single_tag"), lf("single_value"), id="single_tag_removed"),
        pytest.param(
            lf("multiple_tag"), lf("multiple_value"), id="multiple_tag_removed"
        ),
        pytest.param(lf("people_tag"), lf("people_value"), id="people_tag_removed"),
    ],
)
def test_SongTag_removeTag(tag: SongTag, value: list[str]) -> None:
    """Test that removing a tag from a song works."""
    song = ID3()
    assert not tag.hasTag(song)
    tag.setTag(song, value)
    assert tag.hasTag(song)
    tag.removeTag(song)
    assert not tag.hasTag(song)


@pytest.mark.parametrize(
    "tag",
    [
        pytest.param(lf("single_tag"), id="single_tag"),
        pytest.param(lf("multiple_tag"), id="multiple_tag"),
        pytest.param(lf("people_tag"), id="people_tag"),
    ],
)
def test_SongTag_getTag_not_present_returns_None(tag: SongTag) -> None:
    """Tests that if a song doesn't have a Tag, getTag returns None."""
    song = ID3()
    assert not tag.hasTag(song)
    assert tag.getTag(song) is None


@pytest.mark.parametrize(
    ("tag", "value", "expected"),
    [
        pytest.param(
            lf("single_tag"), lf("single_value"), "Some Title", id="single_tag"
        ),
        pytest.param(
            lf("multiple_tag"),
            lf("multiple_value"),
            ["Some Person", "Another Person"],
            id="multiple_tag",
        ),
        pytest.param(
            lf("people_tag"),
            lf("people_value"),
            [["role1", "Person 1"], ["role2", "Person 2"]],
            id="people_tag",
        ),
    ],
)
def test_SongTag_getValue(
    tag: SongTag,
    value: list[str] | list[list[str]],
    expected: str | list[str] | list[list[str]],
) -> None:
    """Test that getting values for a tag works when the tag is in the song."""
    song = ID3()
    assert not tag.hasTag(song)
    tag.setTag(song, value)
    assert tag.getValue(song) == expected


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        pytest.param(
            SongTag(display_name="Title", id3_key="TIT2"),
            "SongTag(display_name='Title', id3_key='TIT2')",
            id="single_tag",
        ),
        pytest.param(
            SongTag(display_name="Composer", id3_key="TCOM"),
            "SongTag(display_name='Composer', id3_key='TCOM')",
            id="multiple_tag",
        ),
        pytest.param(
            SongTag(display_name="TIPL", id3_key="Involved People"),
            "SongTag(display_name='TIPL', id3_key='Involved People')",
            id="people_tag",
        ),
    ],
)
def test_SongTag_repr(tag: SongTag, expected: str) -> None:
    """Test that the string representation for a tag works correctly."""
    assert repr(tag) == expected


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        pytest.param(
            lf("single_tag"),
            SongTag(id3_key="TIT2", display_name="Title"),
            id="diff_object",
        ),
        pytest.param(
            lf("single_tag"),
            lf("single_tag"),
            id="same_object",
        ),
    ],
)
def test_SongTag_eq_same(tag: SongTag, expected: SongTag) -> None:
    """Test SongTag equality returns True when it has same key and display name."""
    assert tag == expected


@pytest.mark.parametrize(
    ("tag", "other"),
    [
        pytest.param(
            SongTag(id3_key="TIT2", display_name="Title"),
            "TIT1",
            id="diff_type",
        ),
        pytest.param(
            SongTag(id3_key="TIT2", display_name="Title"),
            SongTag(id3_key="TIT1", display_name="Title"),
            id="same_type_diff_key",
        ),
        pytest.param(
            SongTag(id3_key="TIT2", display_name="Title"),
            SongTag(id3_key="TIT2", display_name="Title1"),
            id="same_type_diff_name",
        ),
        pytest.param(
            SongTag(id3_key="TIT2", display_name="Title"),
            SongTag(id3_key="TIT1", display_name="Title1"),
            id="same_type_diff_key_and_name",
        ),
    ],
)
def test_SongTag_eq_diff(tag: SongTag, other: Any) -> None:  # noqa: ANN401
    """Test that SongTag equality returns False in different cases."""
    assert tag != other


@pytest.mark.parametrize(
    ("tag", "other"),
    [
        pytest.param(lf("single_tag"), lf("multiple_tag"), id="diff_tags"),
        pytest.param(lf("single_tag"), 5, id="diff_types"),
    ],
)
def test_SongTag_hash(tag: SongTag, other: Any) -> None:  # noqa: ANN401
    """Test that hash only is the same value for tags that are the same."""
    assert hash(tag) == hash((tag.id3_key, tag.display_name))
    assert hash(tag) != hash(other)


def test_SongTag_generateFrame_custom(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that generateFrame correctly creates frames for custom tags."""
    song = ID3()
    custom_tag = SongTag(id3_key="TXXX:TEMPO", display_name="Tempo")

    mock_add = MagicMock()
    monkeypatch.setattr(ID3, "add", mock_add)

    custom_tag.generateFrame(song)

    expected = Frames["TXXX"](id3.Encoding.UTF8, desc="TEMPO", text=[])

    mock_add.assert_called_with(expected)
