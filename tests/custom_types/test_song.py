"""Tests for Song."""

import logging
from pathlib import Path

from music_modify.custom_types import Song
from music_modify.custom_types.tag_value import TextTagValue

logger = logging.getLogger(__name__)


def test_Song_init_with_None() -> None:
    """Test that a Song object is created correctly when not passed a file."""
    song = Song()
    assert song.file is None
    assert song.id3 is not None
    assert song.id3.filename is None


def test_Song_init_with_file(song_path: Path) -> None:
    """Test that a Song object is created correctly when passed a file."""
    song = Song(song_path)
    assert song.file == song_path
    assert song.id3.filename == str(song_path)


def test_Song_columns_setTag_removeTag(song_path: Path) -> None:
    """Test that setting and then removing tags works."""
    song = Song(song_path)
    song.setTag("TIT2", TextTagValue(["Some Title"]))
    song.setTag("TCOM", TextTagValue(["Some Composer", "Another Composer"]))
    assert song.hasTag("TIT2")
    assert song.hasTag("TCOM")
    song.removeTag("TIT2")
    song.removeTag("TCOM")
    assert not song.hasTag("TIT2")
    assert not song.hasTag("TCOM")


def test_Song_invalid_tag() -> None:
    """Test that invalid tags work correctly.

    They should return False for hasTag and None for getTag.
    """
    song = Song()

    assert song.hasTag("ABCD") is False
    assert song.getTag("ABCD") is None


def test_Song_setTag_save_no_file() -> None:
    """Test that setting a tag and saving stores it in the ID3."""
    song = Song()
    assert not song.hasTag("TIT2")
    song.setTag("TIT2", TextTagValue(["Some Title"]))
    assert song.hasTag("TIT2")
    assert "TIT2" not in song.id3
    song.save()
    assert "TIT2" in song.id3
    assert song.id3["TIT2"].text == ["Some Title"]


def test_Song_setTag_save_removeTag_save() -> None:
    """Test that setting a tag and saving stores it, and removing it removes it."""
    song = Song()
    assert not song.hasTag("TIT2")
    song.setTag("TIT2", TextTagValue(["Some Title"]))
    assert song.hasTag("TIT2")
    assert "TIT2" not in song.id3
    song.save()
    assert "TIT2" in song.id3
    assert song.id3["TIT2"].text == ["Some Title"]
    song.removeTag("TIT2")
    assert not song.hasTag("TIT2")
    song.save()
    assert "TIT2" not in song.id3


# TODO: Tests for
# 1. loading a file with no ID3 header
# 2. loading a file that isn't found
# 3. loading a file with an ID3 header, but no tags
# 4. loading a file with an ID3 header and tags
# 5. Saving a file with file property set
# 6. reset changes
# 7. get all tag keys, with loaded and staged values
