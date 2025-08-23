# pyright: reportPrivateUsage = false

from unittest.mock import Mock

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.song import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.gui.edit.bulk.widget_edit_bulk_multiple import (
    EditBulkMultipleWidget,
    _MultipleLineEdit,
)


def test_MultipleLineEdit_items(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    text_to_split = "First, Second, Third"
    mock_prefs_settings = Mock()
    mock_prefs_settings.split_text_entered = ","
    monkeypatch.setattr("music_modify.prefs.prefs.settings", mock_prefs_settings)
    line_edit = _MultipleLineEdit(text_to_split)
    qtbot.addWidget(line_edit)
    assert line_edit.items == ["First", "Second", "Third"]


def test_EditBulkMultipleWidget_updateTag_group_box_unchecked(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag("Artist", "TPE1")
    widget = EditBulkMultipleWidget(parent, {"One"}, tag)
    qtbot.addWidget(widget)
    widget.group_box.setChecked(False)
    songs = []

    assert not widget.updateTag(songs)


def test_EditBulkMultipleWidget_adds_to_line(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag("Artist", "TPE2")
    widget = EditBulkMultipleWidget(parent, {"One"}, tag)
    qtbot.addWidget(widget)

    widget.add_line.setText("Value to Add")
    widget.remove_line.setText("Value to Remove")

    assert widget.add_line.items == ["Value to Add"]
    assert widget.remove_line.values == ["Value to Remove"]
    assert widget.items == ("One",)


def test_EditBulkMultipleWidget_init_not_empty(qtbot: QtBot) -> None:
    parent = QWidget()
    tag = SongTag("Artist", "TPE2")
    widget = EditBulkMultipleWidget(parent, {"One"}, tag)
    qtbot.addWidget(widget)

    assert widget.items == ("One",)

    assert hasattr(widget, "remove_line")
    assert isinstance(widget.remove_line, QWidget)

    assert hasattr(widget, "add_line")
    assert isinstance(widget.add_line, QWidget)

    assert widget.remove_line.all_items == ("One",)


def test_EditBulkMultipleWidget_updateTag_clear_checkbox_checked(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Artist", id3_key="TPE1")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song1 = Song()
    song1.setTag(tag, ["One Artist"])
    song2 = Song()
    song2.setTag(tag, ["One Artist", "Another Artist"])
    songs = [song1, song2]

    widget.clear_checkbox.setChecked(True)

    assert widget.updateTag(songs) is True
    assert not song1.hasTag(tag)
    assert not song2.hasTag(tag)


def test_EditBulkMultipleWidget_updateTag_empty_add_empty_remove(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Artist", id3_key="TPE1")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song1 = Song()
    song1.setTag(tag, ["One Artist"])
    song2 = Song()
    song2.setTag(tag, ["One Artist", "Another Artist"])
    songs = [song1, song2]

    widget.add_line.setText("")
    assert len(widget.add_line.items) == 0
    widget.remove_line.setText("")
    assert len(widget.remove_line.values) == 0

    assert widget.updateTag(songs) is False

    assert tag.getTag(song1.id3) == ["One Artist"]
    assert tag.getTag(song2.id3) == ["One Artist", "Another Artist"]


def test_EditBulkMultipleWidget_updateTag_single_song_empty_add(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song1 = Song()
    songs = [song1]

    assert widget.items == ()
    assert widget.remove_line.all_items == ()

    widget.add_line.setText("New Name")
    assert widget.add_line.items == ["New Name"]

    assert not tag.hasTag(song1.id3)
    assert widget.updateTag(songs) is True

    assert tag.getTag(song1.id3) == ["New Name"]

    assert widget.items == ("New Name",)
    assert widget.remove_line.all_items == ("New Name",)


def test_EditBulkMultipleWidget_updateTag_single_song_and_widget_same(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    song.setTag(tag, ["Some Name", "And Another"])
    songs = [song]

    assert isinstance(tag.getValue(song.id3), list)

    widget.add_line.setText("Some Name")
    assert widget.add_line.items == ["Some Name"]

    assert widget.updateTag(songs) is False
    assert tag.getTag(song.id3) == ["Some Name", "And Another"]


def test_EditBulkMultipleWidget_updateTag_single_widget_has_extra(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    song.setTag(tag, ["Some Name"])
    songs = [song]

    assert isinstance(tag.getValue(song.id3), list)

    widget.add_line.setText("Some Name, And Another Name")
    assert widget.add_line.items == ["Some Name", "And Another Name"]

    assert widget.updateTag(songs) is True
    assert tag.getTag(song.id3) == ["Some Name", "And Another Name"]


def test_EditBulkMultipleWidget_updateTag_multiple_add(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song1 = Song()
    song1.setTag(tag, ["Some Name"])  # First Name
    song2 = Song()
    song2.setTag(tag, ["Some Name", "Another Name"])  # Both Names
    song3 = Song()
    song3.setTag(tag, ["Another Name"])  # Last Name
    song4 = Song()  # No Name
    song5 = Song()
    song5.setTag(tag, ["Not a Name"])  # Other name
    songs = [song1, song2, song3, song4, song5]

    widget.add_line.setText("Some Name, Another Name")
    assert widget.add_line.items == ["Some Name", "Another Name"]

    assert widget.updateTag(songs) is True
    assert tag.getTag(song1.id3) == ["Some Name", "Another Name"]
    assert tag.getTag(song2.id3) == ["Some Name", "Another Name"]
    assert tag.getTag(song3.id3) == ["Another Name", "Some Name"]
    assert tag.getTag(song4.id3) == ["Some Name", "Another Name"]
    assert tag.getTag(song5.id3) == ["Not a Name", "Some Name", "Another Name"]


def test_EditBulkMultipleWidget_updateTag_song_empty_remove(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    assert not song.hasTag(tag)

    widget.remove_line.setText("First Name")
    assert widget.remove_line.values == ["First Name"]

    assert not widget.updateTag([song])
    assert not song.hasTag(tag)


def test_EditBulkMultipleWidget_updateTag_remove_song_value_diff_line_value(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    tag.setTag(song.id3, ["Song Value"])

    widget.remove_line.setText("Line Value")
    assert widget.remove_line.values == ["Line Value"]

    assert not widget.updateTag([song])
    assert tag.getValue(song.id3) == ["Song Value"]


def test_EditBulkMultipleWidget_updateTag_remove_song_value_same_line_value_only(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    tag.setTag(song.id3, ["Song Value"])

    widget.remove_line.setText("Song Value")
    assert widget.remove_line.values == ["Song Value"]

    assert widget.updateTag([song])
    assert tag.getValue(song.id3) == []


def test_EditBulkMultipleWidget_updateTag_remove_song_value_same_line_value_line_extra(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    tag.setTag(song.id3, ["Song Value"])

    widget.remove_line.setText("Song Value, Extra Value")
    assert widget.remove_line.values == ["Song Value", "Extra Value"]

    assert widget.updateTag([song])
    assert tag.getValue(song.id3) == []


def test_EditBulkMultipleWidget_updateTag_remove_song_value_same_line_value_song_extra(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    tag.setTag(song.id3, ["Song Value", "Extra Value"])

    widget.remove_line.setText("Song Value")
    assert widget.remove_line.values == ["Song Value"]

    assert widget.updateTag([song])
    assert tag.getValue(song.id3) == ["Extra Value"]


def test_EditBulkMultipleWidget_updateTag_remove_song_value_same_line_value_song_extra_multiple(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    tag.setTag(song.id3, ["Song Value", "Extra Value", "Another Value", "Even More"])

    widget.remove_line.setText("Song Value, Another Value")
    assert widget.remove_line.values == ["Song Value", "Another Value"]

    assert widget.updateTag([song])
    assert tag.getValue(song.id3) == ["Extra Value", "Even More"]


def test_EditBulkMultipleWidget_updateTag_add_remove(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    tag.setTag(song.id3, ["Song Value", "Extra Value"])

    widget.add_line.setText("New Value, And Another, Removed")
    assert widget.add_line.items == ["New Value", "And Another", "Removed"]

    widget.remove_line.setText("Song Value, Another Value, Removed")
    assert widget.remove_line.values == ["Song Value", "Another Value", "Removed"]

    assert widget.updateTag([song])
    assert tag.getValue(song.id3) == ["Extra Value", "New Value", "And Another"]


def test_EditBulkMultipleWidget_resetView(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Composer", id3_key="TCOM")
    widget = EditBulkMultipleWidget(parent, set(), tag)
    qtbot.addWidget(widget)

    widget.group_box.setChecked(True)

    song = Song()
    tag.setTag(song.id3, ["Song Value", "Extra Value"])

    widget.add_line.setText("Another Value")
    widget.remove_line.setText("Remove Item")

    assert len(widget.items) == 0

    widget._resetView()

    assert widget.add_line.text() == ""
    assert widget.add_line.items == []
    assert widget.remove_line.text() == ""
    assert widget.remove_line.values == []
    assert not widget.clear_checkbox.isChecked()
    assert not widget.group_box.isChecked()
