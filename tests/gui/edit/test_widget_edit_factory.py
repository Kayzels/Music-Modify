"""Tests for EditWidgetFactory."""

from unittest.mock import MagicMock

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.enums import EditorType
from music_modify.custom_types.songtag import SongTag
from music_modify.gui.edit.widget_edit_factory import EditWidgetFactory
from music_modify.gui.edit.widget_edit_line import EditLineWidget
from music_modify.gui.edit.widget_edit_list import EditListWidget
from music_modify.gui.edit.widget_edit_table import EditTableWidget


@pytest.mark.parametrize(
    ("data", "tag", "expected_data", "expected_type"),
    [
        pytest.param(
            None,
            SongTag(
                display_name="Title", id3_key="TIT2", editor_type=EditorType.SingleText
            ),
            "",
            EditLineWidget,
            id="line_tag_with_None",
        ),
        pytest.param(
            None,
            SongTag(
                display_name="Composer",
                id3_key="TCOM",
                editor_type=EditorType.MultipleText,
            ),
            [],
            EditListWidget,
            id="list_tag_with_None",
        ),
        pytest.param(
            None,
            SongTag(
                display_name="Involved People",
                id3_key="TIPL",
                editor_type=EditorType.PeopleValue,
            ),
            [],
            EditTableWidget,
            id="people_tag_with_None",
        ),
        pytest.param(
            "",
            SongTag(display_name="Title", id3_key="TIT2"),
            "",
            EditLineWidget,
            id="line_tag_auto_with_empty_value",
        ),
        pytest.param(
            [],
            SongTag(display_name="Composer", id3_key="TCOM"),
            [],
            EditListWidget,
            id="list_tag_auto_with_empty_value",
        ),
        pytest.param(
            [],
            SongTag(display_name="Involved People", id3_key="TIPL"),
            [],
            EditTableWidget,
            id="people_tag_auto_with_empty_value",
        ),
        pytest.param(
            "Name",
            SongTag(
                display_name="Title", id3_key="TIT2", editor_type=EditorType.SingleText
            ),
            "Name",
            EditLineWidget,
            id="line_tag_with_value",
        ),
        pytest.param(
            ["First Name", "Second Name"],
            SongTag(
                display_name="Composer",
                id3_key="TCOM",
                editor_type=EditorType.MultipleText,
            ),
            ["First Name", "Second Name"],
            EditListWidget,
            id="list_tag_with_multiple_values",
        ),
        pytest.param(
            ["First Name"],
            SongTag(
                display_name="Composer",
                id3_key="TCOM",
                editor_type=EditorType.MultipleText,
            ),
            ["First Name"],
            EditListWidget,
            id="list_tag_with_single_value",
        ),
        pytest.param(
            [["role1", "Name 1"], ["role2", "Name 2"]],
            SongTag(
                display_name="Involved People",
                id3_key="TIPL",
                editor_type=EditorType.PeopleValue,
            ),
            [["role1", "Name 1"], ["role2", "Name 2"]],
            EditTableWidget,
            id="people_tag_with_value",
        ),
        pytest.param(
            "First Name",
            SongTag(
                display_name="Composer",
                id3_key="TCOM",
                editor_type=EditorType.MultipleText,
            ),
            ["First Name"],
            EditListWidget,
            id="list_tag_with_string_value",
        ),
    ],
)
def test_EditWidgetFactory_createWidget_normal(
    qtbot: QtBot,
    data: str | list[str] | list[list[str]] | None,
    tag: SongTag,
    expected_data: str | list[str] | list[list[str]],
    expected_type: type[EditLineWidget] | type[EditListWidget] | type[EditTableWidget],
) -> None:
    """Tests that the correct widget types are created based on the tag."""
    widget = QWidget()
    qtbot.addWidget(widget)

    created_widget = EditWidgetFactory.createWidget(widget, tag, data)
    qtbot.addWidget(created_widget)
    assert isinstance(created_widget, expected_type)
    assert created_widget.value == expected_data


def test_EditWidgetFactory_createWidget_unsupported_type_raises_error() -> None:
    """Test createWidget raises ValueError when SongTag has unsupported EditorType."""
    mock_parent = MagicMock(spec=QWidget)

    mock_tag = MagicMock(spec=SongTag)
    mock_tag.editor_type = EditorType.Automatic

    with pytest.raises(
        ValueError,
        match=f"editor_type had an unsupported value: {EditorType.Automatic}",
    ):
        EditWidgetFactory.createWidget(mock_parent, mock_tag, None)
