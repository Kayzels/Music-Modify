from music_modify.utils import snakeToTitle, tableHeader

def test_snakeToTitle():
    assert snakeToTitle("some_name") == "Some Name"
    assert snakeToTitle("This Word") == "This Word"

def test_tableHeader():
    assert tableHeader("display_name") == "Display Name"
    assert tableHeader("id3_tag") == "ID3 Tag"