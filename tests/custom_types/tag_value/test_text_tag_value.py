"""Tests for TextTagValue."""

from mutagen import id3
import pytest

from music_modify.custom_types.tag_value import AbstractTagValue, TextTagValue


@pytest.mark.parametrize(
    ("value", "id3_key", "expected_frame"),
    [
        pytest.param(
            [], "TIT2", id3.TIT2(encoding=id3.Encoding.UTF8, text=[]), id="empty_text"
        ),
        pytest.param(
            ["Single"],
            "TPE1",
            id3.TPE1(encoding=id3.Encoding.UTF8, text=["Single"]),
            id="single_text",
        ),
        pytest.param(
            ["First", "Second"],
            "TCOM",
            id3.TCOM(encoding=id3.Encoding.UTF8, text=["First", "Second"]),
            id="multiple_text",
        ),
        pytest.param(
            [id3.ID3TimeStamp("2000")],
            "TDRC",
            id3.TDRC(encoding=id3.Encoding.UTF8, text=["2000"]),
            id="timestamp",
        ),
        pytest.param(
            ["Single"],
            "TXXX:test",
            id3.TXXX(encoding=id3.Encoding.UTF8, text=["Single"], desc="test"),
            id="txxx_frame",
        ),
    ],
)
def test_TextTagValue_toId3Frame_valid(
    value: list[str | id3.ID3TimeStamp], id3_key: str, expected_frame: id3.Frame
) -> None:
    """Tests that ID3 frames are created correctly."""
    created_value = TextTagValue(value)
    created_frame = created_value.toId3Frame(id3_key)
    assert created_frame == expected_frame


def test_TextTagValue_toId3Frame_txxx_ValueError() -> None:
    """Tests trying to create a TXXX frame with a missing desc raises ValueError."""
    created_value = TextTagValue(["Test"])
    with pytest.raises(
        ValueError, match="Cannot create a TXXX frame without a desc\\."
    ):
        created_value.toId3Frame("TXXX")
    with pytest.raises(
        ValueError, match="Cannot create a TXXX frame without a desc\\."
    ):
        created_value.toId3Frame("TXXX:")


def test_TextTagValue_toId3Frame_not_text_frame_ValueError() -> None:
    """Tests that trying to create a non-text ID3 frame raises ValueError."""
    created_value = TextTagValue(["Test"])
    with pytest.raises(
        ValueError, match="Tried to create a text frame with an invalid id3 key: TIPL"
    ):
        created_value.toId3Frame("TIPL")


@pytest.mark.parametrize(
    ("value", "join_character", "expected"),
    [
        pytest.param([], ", ", "", id="empty_text"),
        pytest.param(
            ["Single"],
            "; ",
            "Single",
            id="single_text",
        ),
        pytest.param(
            ["First", "Second"],
            "; ",
            "First; Second",
            id="multiple_text_split_semicolon",
        ),
        pytest.param(
            ["First", "Second"],
            ", ",
            "First, Second",
            id="multiple_text_split_comma",
        ),
        pytest.param(
            [id3.ID3TimeStamp("2000")],
            ", ",
            "2000",
            id="timestamp",
        ),
    ],
)
def test_TextTagValue_getDisplayValue(
    value: list[str | id3.ID3TimeStamp], join_character: str, expected: str
) -> None:
    """Tests that the display value is calculated correctly."""
    AbstractTagValue.join_character = join_character
    created_value = TextTagValue(value)
    assert created_value.getDisplayValue() == expected


@pytest.mark.parametrize(
    ("value", "other", "expected_result"),
    [
        pytest.param([], "", True, id="empty_list_equals_empty_string"),
        pytest.param([], None, False, id="empty_list_not_equals_None"),
        pytest.param([], [], True, id="empty_list_equals_empty_list"),
        pytest.param(
            ["Single"],
            "Single",
            True,
            id="single_list_equals_string",
        ),
        pytest.param(
            ["Single"],
            ["Single"],
            True,
            id="single_list_equals_single_list",
        ),
        pytest.param(
            ["Single"],
            ["Single", "Other"],
            False,
            id="single_list_not_equals_multiple_list",
        ),
        pytest.param(
            ["First", "Second"],
            "First, Second",
            True,
            id="multiple_list_equals_string",
        ),
        pytest.param(
            ["First", "Second"],
            ["First", "Second"],
            True,
            id="multiple_list_equals_multiple_list",
        ),
        pytest.param(
            ["First", "Second"],
            [["First", "Second"]],
            False,
            id="multiple_list_not_equals_nested_list",
        ),
        pytest.param(
            [id3.ID3TimeStamp("2000")],
            "2000",
            True,
            id="timestamp_equals_str",
        ),
        pytest.param(
            [id3.ID3TimeStamp("2000")],
            id3.ID3TimeStamp("2000"),
            True,
            id="timestamp_equals_loose_timestamp",
        ),
        pytest.param(
            [id3.ID3TimeStamp("2000")],
            [id3.ID3TimeStamp("2000")],
            True,
            id="timestamp_equals_listed_timestamp",
        ),
        pytest.param(
            [id3.ID3TimeStamp("2000")],
            id3.ID3TimeStamp("1999"),
            False,
            id="timestamp_not_equals_diff_timestamp",
        ),
        pytest.param(["Text"], TextTagValue(["Text"]), True, id="tag_value_equal"),
        pytest.param(
            ["Text"], TextTagValue(["Text", "Other"]), False, id="tag_value_diff"
        ),
    ],
)
def test_TextTagValue_eq(
    value: list[str | id3.ID3TimeStamp],
    other: object,
    expected_result: bool,
) -> None:
    """Tests that equality checks are correct."""
    created_value = TextTagValue(value)
    actual_result: bool = created_value == other
    assert actual_result == expected_result


def test_TextTagValue_hash_raises_TypeError() -> None:
    """Tests that TextTagValues aren't hashable."""
    created_value = TextTagValue(["Test"])
    with pytest.raises(TypeError, match="TagValue objects are not hashable\\."):
        hash(created_value)
