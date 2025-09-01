"""Tests for string utilities."""

import pytest

from music_modify.utils.string_utils import singularPlural, snakeToTitle, tableHeader


@pytest.mark.parametrize(
    ("original", "expected"),
    [
        pytest.param("some_word", "Some Word", id="has_snake_case"),
        pytest.param("this word", "This Word", id="lower_not_snake"),
        pytest.param("This word", "This Word", id="capitalized_not_snake"),
        pytest.param("This Word", "This Word", id="already_title"),
    ],
)
def test_snakeToTitle(original: str, expected: str) -> None:
    """Test that converting snake case to title case only works on snake case text."""
    assert snakeToTitle(original) == expected


@pytest.mark.parametrize(
    ("original", "expected"),
    [
        pytest.param("display_name", "Display Name", id="not_id3"),
        pytest.param("id3_tag", "ID3 Tag", id="has_id3"),
    ],
)
def test_tableHeader(original: str, expected: str) -> None:
    """Test that all names are converted correctly, including ID3."""
    assert tableHeader(original) == expected


@pytest.mark.parametrize(
    ("num", "word", "expected"),
    [
        pytest.param(1, "word", "1 word", id="single_int"),
        pytest.param(1.0, "word", "1 word", id="single_float_trailing_zero"),
        pytest.param(2, "book", "2 books", id="multiple_int"),
        pytest.param(2.0, "book", "2 books", id="multiple_int_trailing_zero"),
        pytest.param(1.2, "cup", "1.2 cups", id="float_pluralized_no_trailing_zero"),
        pytest.param(0, "value", "0 values", id="zero_pluralized"),
    ],
)
def test_singularPlural(num: float, word: str, expected: str) -> None:
    """Test that singular items aren't pluralised, but multiple or decimal items are."""
    assert singularPlural(num, word) == expected
