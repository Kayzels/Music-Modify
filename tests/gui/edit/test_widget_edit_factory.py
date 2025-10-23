"""Tests for EditWidgetFactory."""

import logging

import pytest
from pytestqt.qtbot import QtBot

from music_modify.core.enums import EditorType
from music_modify.custom_types.tag_value import (
    AbstractTagValue,
    PairedTextTagValue,
    PictureTagValue,
    TextTagValue,
)
from music_modify.gui.edit.widget_edit_abstract import EditAbstractWidget
from music_modify.gui.edit.widget_edit_factory import EditWidgetFactory
from music_modify.gui.edit.widget_edit_image import EditImageWidget
from music_modify.gui.edit.widget_edit_line import EditLineWidget
from music_modify.gui.edit.widget_edit_list import EditListWidget
from music_modify.gui.edit.widget_edit_table import EditTableWidget


@pytest.fixture
def editor_types() -> dict[str, EditorType]:
    """Fixture that creates the mappings that are used by an EditWidgetFactory."""
    return {
        "TIT2": EditorType.SingleText,
        "TCOM": EditorType.MultipleText,
        "TIPL": EditorType.PeopleValue,
        "TPE1": EditorType.SingleText,
        "ABCD": EditorType.SingleText,
        "APIC": EditorType.Automatic,
    }


@pytest.mark.parametrize(
    ("id3_key", "current_value", "expected_widget"),
    [
        pytest.param(
            "TIT2",
            TextTagValue(["Title"]),
            EditLineWidget,
            id="single_text_normal",
        ),
        pytest.param(
            "TCOM",
            TextTagValue(["First", "Second"]),
            EditListWidget,
            id="multi_text_normal",
        ),
        pytest.param(
            "TIPL",
            PairedTextTagValue([["First", "Second"]]),
            EditTableWidget,
            id="people_tag_normal",
        ),
        pytest.param(
            "TPE1",
            TextTagValue(["First", "Second"]),
            EditListWidget,
            id="multi_with_single_editor_type",
        ),
        pytest.param(
            "TIT2",
            None,
            EditLineWidget,
            id="empty_value_single_tag",
        ),
        pytest.param(
            "TCOM",
            None,
            EditListWidget,
            id="empty_value_multiple_tag",
        ),
        pytest.param(
            "TMCL",
            None,
            EditTableWidget,
            id="empty_value_people_tag",
        ),
        pytest.param("ABCD", None, None, id="unknown_tag_makes_none"),
        pytest.param(
            "APIC",
            PictureTagValue(b"123"),
            EditImageWidget,
            id="picture_tag_makes_image_widget",
        ),
        pytest.param(
            "APIC",
            None,
            EditImageWidget,
            id="picture_tag_from_id3_makes_none",
        ),
    ],
)
def test_EditWidgetFactory_createWidget_normal(
    qtbot: QtBot,
    editor_types: dict[str, EditorType],
    id3_key: str,
    current_value: AbstractTagValue | None,
    expected_widget: type[EditAbstractWidget] | None,
) -> None:
    """Test that the correct widget types are created based on inputs."""
    EditWidgetFactory.editor_types = editor_types
    created_widget: EditAbstractWidget | None = EditWidgetFactory.createWidget(
        id3_key, current_value
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
    caplog: pytest.LogCaptureFixture,
    qtbot: QtBot,
    editor_types: dict[str, EditorType],
) -> None:
    """Test that a widget isn't created when unknown key, but this is logged."""
    EditWidgetFactory.editor_types = editor_types
    with caplog.at_level(logging.WARNING):
        created_widget: EditAbstractWidget | None = EditWidgetFactory.createWidget(
            "ABCD", None
        )
    if created_widget is not None:
        qtbot.addWidget(created_widget)
        pytest.fail("Created widget was not None.")
    assert (
        "Unable to find a valid AbstractTagValue to make a widget for ABCD."
        in caplog.text
    )
    assert caplog.records[0].levelname == "WARNING"
