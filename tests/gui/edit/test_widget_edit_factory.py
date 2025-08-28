from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from music_modify.custom_types.songtag import SongTag
from music_modify.gui.edit.widget_edit_factory import EditWidgetFactory
from music_modify.gui.edit.widget_edit_line import EditLineWidget
from music_modify.gui.edit.widget_edit_list import EditListWidget
from music_modify.gui.edit.widget_edit_table import EditTableWidget


def test_EditWidgetFactory_create_type_with_data(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    line_tag = SongTag(display_name="Title", id3_key="TIT2")
    line_data = "Name"
    edit_line_widget = EditWidgetFactory.createWidget(widget, line_tag, line_data)
    qtbot.addWidget(edit_line_widget)
    assert isinstance(edit_line_widget, EditLineWidget)
    assert edit_line_widget.value == "Name"

    list_tag = SongTag(display_name="Composer", id3_key="TCOM")
    list_data = ["First Name", "Second Name"]
    edit_list_widget = EditWidgetFactory.createWidget(widget, list_tag, list_data)
    qtbot.addWidget(edit_list_widget)
    assert isinstance(edit_list_widget, EditListWidget)
    assert edit_list_widget.value == ["First Name", "Second Name"]

    people_tag = SongTag(display_name="Involved People", id3_key="TIPL")
    people_data = [["role1", "Name 1"], ["role2", "Name 2"]]
    edit_people_widget = EditWidgetFactory.createWidget(widget, people_tag, people_data)
    qtbot.addWidget(edit_people_widget)
    assert isinstance(edit_people_widget, EditTableWidget)
    assert edit_people_widget.value == [["role1", "Name 1"], ["role2", "Name 2"]]


def test_EditWidgetFactory_create_type_with_None(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)

    line_tag = SongTag(display_name="Title", id3_key="TIT2")
    line_data = None
    edit_line_widget = EditWidgetFactory.createWidget(widget, line_tag, line_data)
    qtbot.addWidget(edit_line_widget)
    assert isinstance(edit_line_widget, EditLineWidget)
    assert edit_line_widget.value == ""

    list_tag = SongTag(display_name="Composer", id3_key="TCOM")
    list_data = None
    edit_list_widget = EditWidgetFactory.createWidget(widget, list_tag, list_data)
    qtbot.addWidget(edit_list_widget)
    assert isinstance(edit_list_widget, EditListWidget)
    assert edit_list_widget.value == []

    people_tag = SongTag(display_name="Involved People", id3_key="TIPL")
    people_data = None
    edit_people_widget = EditWidgetFactory.createWidget(widget, people_tag, people_data)
    qtbot.addWidget(edit_people_widget)
    assert isinstance(edit_people_widget, EditTableWidget)
    assert edit_people_widget.value == []
