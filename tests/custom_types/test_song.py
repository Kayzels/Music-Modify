"""Tests for Song."""

# pyright: reportPrivateUsage = false

import logging
from pathlib import Path

from mutagen import id3
import pytest

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


def test_Song_load_with_tags(song_with_tags_path: Path) -> None:
    """Tests that loading the values from a song that has tags works."""
    song = Song()
    song.load(song_with_tags_path)
    assert song._filepath == song_with_tags_path
    assert song._id3.filename == str(song_with_tags_path)
    assert song._staged_changes == {}
    assert song._loaded_values["TIT2"] == TextTagValue(["Test Song"])


def test_Song_load_with_no_path(
    song_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Tests that loading a file that doesn't exist makes empty ID3 and logs."""
    song = Song()
    invalid_path = song_path.with_suffix(".m4a")
    with caplog.at_level(logging.ERROR):
        song.load(invalid_path)

    assert f"Error loading '{invalid_path}' for mutagen." in caplog.text
    assert caplog.records[0].levelname == "ERROR"

    assert song._filepath is None
    assert song._id3.filename is None
    assert song._staged_changes == {}
    assert song._loaded_values == {}


def test_Song_update_only_existing_and_save(song_with_tags_path: Path) -> None:
    """Tests that updating existing tags keeps the size, but changes values."""
    initial_size = song_with_tags_path.stat().st_size
    song = Song(song_with_tags_path)
    assert song._loaded_values["TIT2"] == TextTagValue(["Test Song"])
    assert song._id3["TIT2"] == id3.TIT2(id3.Encoding.UTF8, text=["Test Song"])
    song.setTag("TIT2", TextTagValue(["Changed Value"]))
    song.save()
    assert song._staged_changes == {}
    assert song._loaded_values["TIT2"] == TextTagValue(["Changed Value"])
    assert song._id3["TIT2"] == id3.TIT2(id3.Encoding.UTF8, text=["Changed Value"])
    new_size = song_with_tags_path.stat().st_size
    assert new_size == initial_size


def test_Song_update_only_existing_and_save_repeats(song_with_tags_path: Path) -> None:
    """Tests that calling save multiple times doesn't change size."""
    initial_size = song_with_tags_path.stat().st_size
    song = Song(song_with_tags_path)
    assert song._loaded_values["TIT2"] == TextTagValue(["Test Song"])
    assert song._id3["TIT2"] == id3.TIT2(id3.Encoding.UTF8, text=["Test Song"])
    for value in "Changed Value", "Another Value", "And Another":
        song.setTag("TIT2", TextTagValue([value]))
        song.setTag("TPE2", TextTagValue([value]))
        song.save()
        assert song._staged_changes == {}
        assert song._loaded_values["TIT2"] == TextTagValue([value])
        assert song._id3["TIT2"] == id3.TIT2(id3.Encoding.UTF8, text=[value])
        assert song._loaded_values["TPE2"] == TextTagValue([value])
        assert song._id3["TPE2"] == id3.TPE2(id3.Encoding.UTF8, text=[value])
        new_size = song_with_tags_path.stat().st_size
        assert new_size == initial_size


def test_Song_setTag_save_adds(song_with_tags_path: Path) -> None:
    """Test that setting a tag adds it with a valid file."""
    song = Song(song_with_tags_path)
    assert not song.hasTag("TMOO")
    assert "TMOO" not in song._id3
    song.setTag("TMOO", TextTagValue(["Some Mood"]))
    song.save()
    assert song.hasTag("TMOO")
    assert "TMOO" in song._id3
    assert song.getTag("TMOO") == TextTagValue(["Some Mood"])
    assert song._id3["TMOO"] == id3.TMOO(id3.Encoding.UTF8, text=["Some Mood"])


def test_Song_getAllTagKeys_no_change(song_with_tags_path: Path) -> None:
    """Tests getting all the tag keys with no tags added or removed."""
    id3_val = id3.ID3(song_with_tags_path)
    orig_keys = list(id3_val.keys())
    song = Song(song_with_tags_path)
    song_keys = song.getAllTagKeys()
    assert set(song_keys) == set(orig_keys)


def test_Song_getAllTagKeys_with_add_and_remove(song_with_tags_path: Path) -> None:
    """Tests getting all the tag keys when tags have been added and removed."""
    id3_val = id3.ID3(song_with_tags_path)
    orig_keys = list(id3_val.keys())
    song = Song(song_with_tags_path)
    song.setTag("TIT2", None)
    song.setTag("TMOO", TextTagValue(["Some Mood"]))
    changed_orig = set(orig_keys)
    changed_orig.discard("TIT2")
    changed_orig.add("TMOO")
    song_keys = song.getAllTagKeys()
    assert set(song_keys) == changed_orig


def test_Song_resetChanges_no_key() -> None:
    """Tests that resetting changes without an id3 key resets all."""
    song = Song()
    song.setTag("TIT2", TextTagValue(["Title"]))
    song.setTag("TPE1", TextTagValue(["Artist"]))
    assert len(song._staged_changes) > 0
    song.resetChanges()
    assert song._staged_changes == {}


def test_Song_resetChanges_with_key() -> None:
    """Tests that resetting changes without an id3 key resets all."""
    song = Song()
    song.setTag("TIT2", TextTagValue(["Title"]))
    song.setTag("TPE1", TextTagValue(["Artist"]))
    assert len(song._staged_changes) > 0
    song.resetChanges("TIT2")
    assert song._staged_changes == {"TPE1": TextTagValue(["Artist"])}
