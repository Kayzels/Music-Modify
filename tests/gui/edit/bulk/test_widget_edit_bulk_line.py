from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from music_modify.custom_types.song import Song
from music_modify.custom_types.songtag import SongTag
from music_modify.gui.edit.bulk.widget_edit_bulk_line import EditBulkLineWidget


def test_EditBulkLineWidget_init_not_in_all(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First", "Second"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=False)
    qtbot.addWidget(widget)
    assert "First" in widget.items
    assert "Second" in widget.items
    assert len(widget.items) == 2  # noqa: PLR2004

    assert "First" in widget.main_widget.all_items
    assert "Second" in widget.main_widget.all_items
    assert len(widget.main_widget.all_items) == 2  # noqa: PLR2004
    assert widget.main_widget.text() == ""

    assert hasattr(widget, "apply_checkbox")
    assert hasattr(widget, "clear_checkbox")


def test_EditBulkLineWidget_init_in_all(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)
    assert widget.items == ("First",)

    assert widget.main_widget.all_items == ("First",)
    assert widget.main_widget.text() == "First"

    assert hasattr(widget, "apply_checkbox")
    assert hasattr(widget, "clear_checkbox")


def test_EditBulkLineWidget_checkbox_switch(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)

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
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)

    widget.apply_checkbox.setChecked(False)
    widget.clear_checkbox.setChecked(False)

    assert not widget.updateTag([])


def test_EditBulkLineWidget_updateTag_apply_no_songs(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    assert not widget.updateTag([])


def test_EditBulkLineWidget_updateTag_clear_no_songs(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)

    widget.apply_checkbox.setChecked(False)
    widget.clear_checkbox.setChecked(True)

    assert not widget.updateTag([])


def test_EditBulkLineWidget_updateTag_apply_empty_clears(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag, ["First"])
    assert song.hasTag(tag)
    widget.main_widget.setText("")

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag) is False


def test_EditBulkLineWidget_updateTag_apply_only_space_clears(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag, ["First"])
    assert song.hasTag(tag)
    widget.main_widget.setText("     ")

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag) is False


def test_EditBulkLineWidget_updateTag_apply_not_empty_sets(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag, ["First"])
    assert song.hasTag(tag)

    new_value = "Second"
    widget.main_widget.setText(new_value)

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag) is True
    assert song.getValue(tag) == new_value

    assert widget.main_widget.text() == new_value


def test_EditBulkLineWidget_updateTag_apply_not_empty_sets_stripped(
    qtbot: QtBot,
) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)

    widget.clear_checkbox.setChecked(False)
    widget.apply_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag, ["First"])
    assert song.hasTag(tag)

    new_value = " Another      "
    widget.main_widget.setText(new_value)

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag) is True
    assert song.getValue(tag) == new_value.strip()

    assert widget.main_widget.text() == new_value.strip()


def test_EditBulkLineWidget_updateTag_clear(qtbot: QtBot) -> None:
    parent = QWidget()
    qtbot.addWidget(parent)
    tag = SongTag(display_name="Album", id3_key="TALB")
    data = {"First"}

    widget = EditBulkLineWidget(parent, data, tag, in_all=True)
    qtbot.addWidget(widget)

    widget.main_widget.setText("Some Value")

    widget.apply_checkbox.setChecked(False)
    widget.clear_checkbox.setChecked(True)

    song = Song()
    song.setTag(tag, ["First"])
    assert song.hasTag(tag)

    assert widget.updateTag([song]) == {song}
    assert song.hasTag(tag) is False

    assert widget.main_widget.text() == ""
