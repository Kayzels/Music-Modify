"""Tests for EditWidgetFactory."""

import logging

import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.enums import EditorType
from music_modify.custom_types.tag_value import (
    AbstractTagValue,
    PairedTextTagValue,
    PictureTagValue,
    TextTagValue,
)
from music_modify.gui.edit.widget_edit_abstract import EditAbstractWidget
from music_modify.gui.edit.widget_edit_factory import EditWidgetFactory
from music_modify.gui.edit.widget_edit_line import EditLineWidget
from music_modify.gui.edit.widget_edit_list import EditListWidget
from music_modify.gui.edit.widget_edit_table import EditTableWidget


@pytest.mark.parametrize(
    ("id3_key", "editor_type", "current_value", "expected_widget"),
    [
        pytest.param(
            "TIT2",
            EditorType.SingleText,
            TextTagValue(["Title"]),
            EditLineWidget,
            id="single_text_normal",
        ),
        pytest.param(
            "TCOM",
            EditorType.MultipleText,
            TextTagValue(["First", "Second"]),
            EditListWidget,
            id="multi_text_normal",
        ),
        pytest.param(
            "TIPL",
            EditorType.PeopleValue,
            PairedTextTagValue([["First", "Second"]]),
            EditTableWidget,
            id="people_tag_normal",
        ),
        pytest.param(
            "TPE1",
            EditorType.SingleText,
            TextTagValue(["First", "Second"]),
            EditListWidget,
            id="multi_with_single_editor_type",
        ),
        pytest.param(
            "TIT2",
            EditorType.SingleText,
            None,
            EditLineWidget,
            id="empty_value_single_tag",
        ),
        pytest.param(
            "TCOM",
            EditorType.MultipleText,
            None,
            EditListWidget,
            id="empty_value_multiple_tag",
        ),
        pytest.param(
            "TMCL",
            EditorType.PeopleValue,
            None,
            EditTableWidget,
            id="empty_value_people_tag",
        ),
        pytest.param(
            "ABCD", EditorType.SingleText, None, None, id="unknown_tag_makes_none"
        ),
        pytest.param(
            "APIC",
            EditorType.Automatic,
            PictureTagValue(),
            None,
            id="picture_tag_makes_none",
        ),
        pytest.param(
            "APIC",
            EditorType.Automatic,
            None,
            None,
            id="picture_tag_from_id3_makes_none",
        ),
    ],
)
def test_EditWidgetFactory_createWidget_normal(
    qtbot: QtBot,
    id3_key: str,
    editor_type: EditorType,
    current_value: AbstractTagValue | None,
    expected_widget: type[EditAbstractWidget] | None,
) -> None:
    """Test that the correct widget types are created based on inputs."""
    created_widget: EditAbstractWidget | None = EditWidgetFactory.createWidget(
        id3_key, editor_type, current_value
    )
    if created_widget is not None:
        qtbot.addWidget(created_widget)
    if expected_widget is None:
        assert created_widget is None
    else:
        assert isinstance(created_widget, expected_widget)
        assert created_widget.original == current_value
        assert created_widget.value == current_value


def test_EditWidgetFactory_createWidget_logs_when_unknown_key(
    caplog: pytest.LogCaptureFixture, qtbot: QtBot
) -> None:
    """Test that a widget isn't created when unknown key, but this is logged."""
    with caplog.at_level(logging.WARNING):
        created_widget: EditAbstractWidget | None = EditWidgetFactory.createWidget(
            "ABCD", EditorType.Automatic, None
        )
    if created_widget is not None:
        qtbot.addWidget(created_widget)
        pytest.fail("Created widget was not None.")
    assert (
        "Unable to find a valid AbstractTagValue to make a widget for ABCD."
        in caplog.text
    )
    assert caplog.records[0].levelname == "WARNING"


def test_EditWidgetFactory_createWidget_logs_when_valid_value_no_widget_type(
    caplog: pytest.LogCaptureFixture, qtbot: QtBot
) -> None:
    """Test that a widget isn't created when no known widget type for value type."""
    with caplog.at_level(logging.INFO):
        created_widget: EditAbstractWidget | None = EditWidgetFactory.createWidget(
            "APIC", EditorType.Automatic, PictureTagValue()
        )
    if created_widget is not None:
        qtbot.addWidget(created_widget)
        pytest.fail("Created widget was not None.")
    assert (
        f"TagValue instance {type(PictureTagValue())} is valid, "
        + "but no widget for this type exists yet."
        in caplog.text
    )
    assert caplog.records[0].levelname == "INFO"
