import logging
from pathlib import Path
from music_modify.custom_types import Song
from music_modify.prefs import prefs

logger = logging.getLogger(__name__)


def test_song_init():
    song = Song()
    assert song.file is None
    info = ["" for _ in range(len(prefs.settings.table_tags))]
    assert song.display_info == info


def test_song_init_file():
    song_path = Path("tests/test_song.mp3").absolute()
    song = Song(song_path)
    assert song.file == Path("tests/test_song.mp3").absolute()


def test_columns_set_updated_removed():
    song_path = Path("tests/test_song.mp3").absolute()
    song = Song(song_path)
    song.setTag("TIT2", ["Some Title"])
    song.setTag("TPE2", ["Some Artist"])
    assert song.hasTag("TIT2")
    assert song.hasTag("TPE2")
    song.updateInfo()
    expected_output: list[str] = []
    for col in prefs.settings.table_tags:
        if col.id3_key == "TIT2":
            logger.info("ID3 key was TIT2")
            expected_output.append("Some Title")
        elif col.id3_key == "TPE2":
            logger.info("ID3 key was TPE2")
            expected_output.append("Some Artist")
        else:
            expected_output.append("")
    assert song.display_info == expected_output
    song.removeTag("TIT2")
    song.removeTag("TPE2")
    assert not song.hasTag("TIT2")
    assert not song.hasTag("TPE2")
