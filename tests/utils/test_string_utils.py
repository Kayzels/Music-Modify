from music_modify.utils.string_utils import singularPlural, snakeToTitle, tableHeader


def test_snakeToTitle() -> None:
    assert snakeToTitle("some_name") == "Some Name"
    assert snakeToTitle("This Word") == "This Word"


def test_tableHeader() -> None:
    assert tableHeader("display_name") == "Display Name"
    assert tableHeader("id3_tag") == "ID3 Tag"


def test_singularPlural() -> None:
    assert singularPlural(1, "word") == "1 word"
    assert singularPlural(2, "book") == "2 books"
    assert singularPlural(1.2, "cup") == "1.2 cups"
    assert singularPlural(0, "value") == "0 values"
