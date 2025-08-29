"""Tests for EditWidgetFactory."""

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.songtag import SongTag
from music_modify.gui.edit.widget_edit_factory import EditWidgetFactory
from music_modify.gui.edit.widget_edit_line import EditLineWidget
from music_modify.gui.edit.widget_edit_list import EditListWidget
from music_modify.gui.edit.widget_edit_table import EditTableWidget


@pytest.mark.parametrize(
    ("data", "tag", "empty_data", "expected_type"),
    [
        pytest.param(
            None,
            SongTag(display_name="Title", id3_key="TIT2"),
            "",
            EditLineWidget,
            id="line_tag_with_None",
        ),
        pytest.param(
            None,
            SongTag(display_name="Composer", id3_key="TCOM"),
            [],
            EditListWidget,
            id="list_tag_with_None",
        ),
        pytest.param(
            None,
            SongTag(display_name="Involved People", id3_key="TIPL"),
            [],
            EditTableWidget,
            id="people_tag_with_None",
        ),
        pytest.param(
            "",
            SongTag(display_name="Title", id3_key="TIT2"),
            "",
            EditLineWidget,
            id="line_tag_with_empty_value",
        ),
        pytest.param(
            [],
            SongTag(display_name="Composer", id3_key="TCOM"),
            [],
            EditListWidget,
            id="list_tag_with_empty_value",
        ),
        pytest.param(
            [],
            SongTag(display_name="Involved People", id3_key="TIPL"),
            [],
            EditTableWidget,
            id="people_tag_with_empty_value",
        ),
        pytest.param(
            "Name",
            SongTag(display_name="Title", id3_key="TIT2"),
            "",
            EditLineWidget,
            id="line_tag_with_value",
        ),
        pytest.param(
            ["First Name", "Second Name"],
            SongTag(display_name="Composer", id3_key="TCOM"),
            [],
            EditListWidget,
            id="list_tag_with_multiple_values",
        ),
        pytest.param(
            ["First Name"],
            SongTag(display_name="Composer", id3_key="TCOM"),
            [],
            EditListWidget,
            id="list_tag_with_single_value",
        ),
        pytest.param(
            [["role1", "Name 1"], ["role2", "Name 2"]],
            SongTag(display_name="Involved People", id3_key="TIPL"),
            [],
            EditTableWidget,
            id="people_tag_with_value",
        ),
    ],
)
def test_EditWidgetFactory_create_type(
    qtbot: QtBot,
    data: str | list[str] | list[list[str]] | None,
    tag: SongTag,
    empty_data: str | list[str] | list[list[str]],
    expected_type: type[EditLineWidget] | type[EditListWidget] | type[EditTableWidget],
) -> None:
    """Tests that the correct widget types are created based on the tag."""
    widget = QWidget()
    qtbot.addWidget(widget)

    created_widget = EditWidgetFactory.createWidget(widget, tag, data)
    qtbot.addWidget(created_widget)
    assert isinstance(created_widget, expected_type)
    assert created_widget.value == (data if data is not None else empty_data)
