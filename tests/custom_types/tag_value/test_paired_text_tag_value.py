"""Tests for PairedTextTagValue."""

from mutagen import id3
import pytest

from music_modify.custom_types.tag_value import AbstractTagValue, PairedTextTagValue


@pytest.mark.parametrize(
    ("value", "id3_key", "expected_frame"),
    [
        pytest.param(
            [], "TIPL", id3.TIPL(encoding=id3.Encoding.UTF8, people=[]), id="empty_list"
        ),
        pytest.param(
            [["Single"]],
            "TMCL",
            id3.TMCL(encoding=id3.Encoding.UTF8, people=[]),
            id="invalid_not_pair",
        ),
        pytest.param(
            [["First", "Second"]],
            "TIPL",
            id3.TIPL(encoding=id3.Encoding.UTF8, people=[["First", "Second"]]),
            id="single_pair",
        ),
        pytest.param(
            [["First", "Second"], ["Third", "Fourth"]],
            "TIPL",
            id3.TMCL(
                encoding=id3.Encoding.UTF8,
                people=[["First", "Second"], ["Third", "Fourth"]],
            ),
            id="multiple_pairs",
        ),
    ],
)
def test_PairedTextTagValue_toId3Frame(
    value: list[list[str]], id3_key: str, expected_frame: id3.Frame
) -> None:
    """Tests that ID3 frames are created correctly."""
    created_value = PairedTextTagValue(value)
    created_frame = created_value.toId3Frame(id3_key)
    assert created_frame == expected_frame


def test_PairedTextTagValue_toId3Frame_not_pair_frame_ValueError() -> None:
    """Tests that trying to create a non-pair ID3 frame raises ValueError."""
    created_value = PairedTextTagValue([["First", "Second"]])
    with pytest.raises(
        ValueError,
        match="Tried to create a paired text frame with an invalid id3 key: TIT2",
    ):
        created_value.toId3Frame("TIT2")


@pytest.mark.parametrize(
    ("value", "join_character", "expected"),
    [
        pytest.param([], ", ", "", id="empty_text"),
        pytest.param(
            [["Single"]],
            ", ",
            "",
            id="invalid_not_pair",
        ),
        pytest.param(
            [["First", "Second"]],
            "; ",
            "First: Second",
            id="single_pair",
        ),
        pytest.param(
            [["First", "Second"], ["Third", "Fourth"]],
            ", ",
            "First: Second, Third: Fourth",
            id="multiple_pairs_join_comma",
        ),
        pytest.param(
            [["First", "Second"], ["Third", "Fourth"]],
            "; ",
            "First: Second; Third: Fourth",
            id="multiple_pairs_join_semicolon",
        ),
    ],
)
def test_PairedTextTagValue_getDisplayValue(
    value: list[list[str]], join_character: str, expected: str
) -> None:
    """Tests that the display value is calculated correctly."""
    AbstractTagValue.join_character = join_character
    created_value = PairedTextTagValue(value)
    assert created_value.getDisplayValue() == expected


@pytest.mark.parametrize(
    ("value", "other", "expected_result"),
    [
        pytest.param([], "", True, id="empty_list_equals_empty_string"),
        pytest.param([], None, False, id="empty_list_not_equals_None"),
        pytest.param([], [], True, id="empty_list_equals_empty_list"),
        pytest.param(
            ["Single"],
            "",
            True,
            id="invalid_list_equals_empty_string",
        ),
        pytest.param(
            ["Single"],
            [],
            True,
            id="invalid_list_equals_empty_list",
        ),
        pytest.param(
            ["Single"],
            ["Single"],
            False,
            id="invalid_list_not_equals_same_invalid_list",
        ),
        pytest.param(
            [["First", "Second"]],
            "First: Second",
            True,
            id="single_pair_equals_string_rep",
        ),
        pytest.param(
            [["First", "Second"]],
            [["First", "Second"]],
            True,
            id="single_pair_equals_pair",
        ),
        pytest.param(
            [["First", "Second"], ["Third", "Fourth"]],
            [["First", "Second"], ["Third", "Fourth"]],
            True,
            id="multiple_pair_equals_pair",
        ),
        pytest.param(
            [["First", "Second"], ["Third", "Fourth"]],
            [["First", "Second"]],
            False,
            id="multiple_pair_not_equals_single_pair",
        ),
        pytest.param(
            [], PairedTextTagValue([]), True, id="empty_equals_value_with_empty"
        ),
        pytest.param(
            [],
            PairedTextTagValue([["First", "Second"]]),
            False,
            id="empty_not_equals_value_with_other",
        ),
        pytest.param(
            [["First", "Second"]],
            PairedTextTagValue([["First", "Second"]]),
            True,
            id="pair_equal_to_value_with_pair",
        ),
        pytest.param(
            [["First", "Second"]],
            PairedTextTagValue([]),
            False,
            id="pair_not_equal_to_value_with_empty",
        ),
    ],
)
def test_TextTagValue_eq(
    value: list[list[str]],
    other: object,
    expected_result: bool,
) -> None:
    """Tests that equality checks are correct."""
    created_value = PairedTextTagValue(value)
    actual_result: bool = created_value == other
    assert actual_result == expected_result


def test_PairedTextTagValue_hash_raises_TypeError() -> None:
    """Tests that PairedTextTagValues aren't hashable."""
    created_value = PairedTextTagValue([])
    with pytest.raises(TypeError, match="TagValue objects are not hashable\\."):
        hash(created_value)
