"""Tests for EditBulkLineWidget."""

from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from music_modify.custom_types import Song, TagInfo
from music_modify.custom_types.enums import EditorType
from music_modify.custom_types.tag_value.text_tag_value import TextTagValue
from music_modify.gui.edit.bulk.widget_edit_bulk_line import EditBulkLineWidget


def test_EditBulkLineWidget_init_not_in_all(qtbot: QtBot) -> None:
    """Test creating an EditBulkLineWidget where the data isn't in all songs.

    In this case, it should be added to all_items,
    but the text for the widget should be empty.
    """
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = TagInfo(
        display_name="Album", id3_key="TALB", editor_type=EditorType.SingleText
    )
    data = {"First", "Second"}

    widget = EditBulkLineWidget(data, tag, in_all=False, parent=parent)
    qtbot.addWidget(widget)
    assert "First" in widget.items
    assert "Second" in widget.items
    assert len(widget.items) == 2

    assert "First" in widget.main_widget.all_items
    assert "Second" in widget.main_widget.all_items
    assert len(widget.main_widget.all_items) == 2
    assert widget.main_widget.text() == ""

    assert hasattr(widget, "apply_checkbox")
    assert hasattr(widget, "clear_checkbox")


def test_EditBulkLineWidget_init_in_all(qtbot: QtBot) -> None:
    """Test creating an EditBulkLineWidget where the data is in all songs.

    In this case, it should be added to all_items,
    and should be the text for the widget.
    """
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = TagInfo(
        display_name="Album", id3_key="TALB", editor_type=EditorType.SingleText
    )
    data = {"First"}

    widget = EditBulkLineWidget(data, tag, in_all=True, parent=parent)
    qtbot.addWidget(widget)
    assert widget.items == ("First",)

    assert widget.main_widget.all_items == ("First",)
    assert widget.main_widget.text() == "First"

    assert hasattr(widget, "apply_checkbox")
    assert hasattr(widget, "clear_checkbox")


def _createWidget(qtbot: QtBot) -> tuple[QWidget, TagInfo, EditBulkLineWidget]:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = TagInfo(
        display_name="Album", id3_key="TALB", editor_type=EditorType.SingleText
    )
    data = {"First"}

    widget = EditBulkLineWidget(data, tag, in_all=True, parent=parent)
    qtbot.addWidget(widget)

    return parent, tag, widget


def test_EditBulkLineWidget_checkbox_switch(qtbot: QtBot) -> None:
    """Test that checking a checkbox disables the other one."""
    _, __, widget = _createWidget(qtbot)

    widget.apply_checkbox.setChecked(True)
    assert not widget.clear_checkbox.isChecked()
    assert widget.main_widget.isEnabled()

    widget.clear_checkbox.setChecked(True)
    assert not widget.apply_checkbox.isChecked()
    assert not widget.main_widget.isEnabled()

    widget.clear_checkbox.setChecked(False)
    assert not widget.clear_checkbox.isChecked()
    assert not widget.apply_checkbox.isChecked()
    assert not widget.main_widget.isEnabled()

    widget.apply_checkbox.setChecked(True)
    assert not widget.clear_checkbox.isChecked()
    assert widget.main_widget.isEnabled()


def test_EditBulkLineWidget_updateTag_no_checkbox(qtbot: QtBot) -> None:
    """Test that updateTag doesn't update the tag when not checked."""
    _, __, widget = _createWidget(qtbot)

    widget.apply_checkbox.setChecked(False)
    widget.clear_checkbox.setChecked(False)

    assert not widget.updateTag([])


def test_EditBulkLineWidget_updateTag_apply_no_songs(qtbot: QtBot) -> None:
    """Test that updateTag returns False when no songs are updated."""
    _, __, widget = _createWidget(qtbot)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    assert not widget.updateTag([])


def test_EditBulkLineWidget_updateTag_clear_no_songs(qtbot: QtBot) -> None:
    """Test that updateTag returns False when there are no songs and clear is called."""
    _, __, widget = _createWidget(qtbot)

    widget.apply_checkbox.setChecked(False)
    widget.clear_checkbox.setChecked(True)

    assert not widget.updateTag([])


def test_EditBulkLineWidget_updateTag_apply_empty_clears(qtbot: QtBot) -> None:
    """Test that updateTag clears the tag if apply is called with an empty widget."""
    _, tag, widget = _createWidget(qtbot)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag.id3_key, TextTagValue(["First"]))
    assert song.hasTag(tag.id3_key)
    widget.main_widget.setText("")

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag.id3_key) is False


def test_EditBulkLineWidget_updateTag_apply_only_space_clears(qtbot: QtBot) -> None:
    """Test that updateTag clears tag if apply called with widget having only space."""
    _, tag, widget = _createWidget(qtbot)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag.id3_key, TextTagValue(["First"]))
    assert song.hasTag(tag.id3_key)
    widget.main_widget.setText("     ")

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag.id3_key) is False


def test_EditBulkLineWidget_updateTag_apply_not_empty_sets(qtbot: QtBot) -> None:
    """Test that calling update when not empty sets the tag value."""
    _, tag, widget = _createWidget(qtbot)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag.id3_key, TextTagValue(["First"]))
    assert song.hasTag(tag.id3_key)

    new_value = "Second"
    widget.main_widget.setText(new_value)

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag.id3_key) is True
    assert song.getTag(tag.id3_key) == TextTagValue([new_value])

    assert widget.main_widget.text() == new_value


def test_EditBulkLineWidget_updateTag_apply_not_empty_sets_stripped(
    qtbot: QtBot,
) -> None:
    """Test that calling update when not empty sets the tag value without whitespace."""
    _, tag, widget = _createWidget(qtbot)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag.id3_key, TextTagValue(["First"]))
    assert song.hasTag(tag.id3_key)

    new_value = " Another      "
    widget.main_widget.setText(new_value)

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag.id3_key) is True
    assert song.getTag(tag.id3_key) == TextTagValue([new_value.strip()])

    assert widget.main_widget.text() == new_value.strip()


def test_EditBulkLineWidget_updateTag_clear(qtbot: QtBot) -> None:
    """Test that clearing works when clear checkbox checked and updating."""
    _, tag, widget = _createWidget(qtbot)

    widget.main_widget.setText("Some Value")

    widget.apply_checkbox.setChecked(False)
    widget.clear_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag.id3_key, TextTagValue(["First"]))
    assert song.hasTag(tag.id3_key)

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag.id3_key) is False

    assert widget.main_widget.text() == ""
