"""Tests for string utilities."""

from music_modify.utils.string_utils import singularPlural, snakeToTitle, tableHeader


def test_snakeToTitle() -> None:
    """Test that converting snake case to title case only works on snake case text."""
    assert snakeToTitle("some_name") == "Some Name"
    assert snakeToTitle("This Word") == "This Word"


def test_tableHeader() -> None:
    """Test that all names are converted correctly, including ID3."""
    assert tableHeader("display_name") == "Display Name"
    assert tableHeader("id3_tag") == "ID3 Tag"


def test_singularPlural() -> None:
    """Test that singular items aren't pluralised, but multiple or decimal items are."""
    assert singularPlural(1, "word") == "1 word"
    assert singularPlural(2, "book") == "2 books"
    assert singularPlural(1.2, "cup") == "1.2 cups"
    assert singularPlural(0, "value") == "0 values"
