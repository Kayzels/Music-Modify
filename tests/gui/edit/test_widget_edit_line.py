"""Tests for EditLineWidget."""

import logging

import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.tag_value import (
    AbstractTagValue,
    PairedTextTagValue,
    TextTagValue,
)
from music_modify.gui.edit.widget_edit_line import EditLineWidget


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param(None, None, id="init_None"),
        pytest.param(TextTagValue([]), None, id="init_text_empty"),
        pytest.param(
            TextTagValue(["Word"]), TextTagValue(["Word"]), id="init_text_has_value"
        ),
        pytest.param(PairedTextTagValue([]), None, id="init_not_text_value"),
    ],
)
def test_EditLineWidget_init_param(
    qtbot: QtBot, data: AbstractTagValue | None, expected: TextTagValue | None
) -> None:
    """Tests creating an EditLineWidget based on data type."""
    line_edit = EditLineWidget(data)
    qtbot.addWidget(line_edit)
    assert line_edit.value == expected
    assert line_edit.original == expected


def test_EditLineWidget_update_from_widget(qtbot: QtBot) -> None:
    """Tests updating the value by changing the displayed text."""
    data = TextTagValue(["Name"])
    new_value = "New Value"
    line_edit = EditLineWidget(data)
    qtbot.addWidget(line_edit)

    assert line_edit.value == data
    assert line_edit.original == data

    line_edit.main_widget.setText(new_value)

    assert line_edit.value == TextTagValue([new_value])
    assert line_edit.original == data


def test_EditLineWidget_value_set(qtbot: QtBot) -> None:
    """Tests updating the value directly."""
    data = TextTagValue(["Original"])
    line_edit = EditLineWidget(data)
    qtbot.addWidget(line_edit)

    assert line_edit.value == data
    new_value = TextTagValue(["New Value"])
    line_edit.value = new_value
    assert line_edit.value == new_value


def test_EditLineWidget_value_None(qtbot: QtBot) -> None:
    """Tests setting the value to None directly."""
    data = TextTagValue(["Original"])
    line_edit = EditLineWidget(data)
    qtbot.addWidget(line_edit)

    line_edit.value = None
    assert line_edit.main_widget.text() == ""
    assert line_edit.value is None


def test_EditLineWidget_value_invalid(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    """Tests that setting an invalid value logs and clears."""
    data = TextTagValue(["Original"])
    line_edit = EditLineWidget(data)
    qtbot.addWidget(line_edit)
    assert line_edit.value == data
    new_value = PairedTextTagValue([["first", "second"]])
    with caplog.at_level(logging.WARNING):
        line_edit.value = new_value

    assert line_edit.value is None
    assert "EditLineWidget received unexpected value type" in caplog.text


def test_EditLineWidget_clear(qtbot: QtBot) -> None:
    """Tests clearing the value from the widget."""
    data = TextTagValue(["Name"])
    line_edit = EditLineWidget(data)
    qtbot.addWidget(line_edit)

    assert line_edit.value == data
    assert line_edit.original == data

    line_edit.clear()

    assert line_edit.value is None
    assert line_edit.main_widget.text() == ""
    assert line_edit.original == data


def test_EditLineWidget_reset(qtbot: QtBot) -> None:
    """Tests resetting, clearing, and then resetting the value."""
    data = TextTagValue(["Name"])
    line_edit = EditLineWidget(data)
    qtbot.addWidget(line_edit)
    new_value = TextTagValue(["New Value"])

    assert line_edit.value == data
    assert line_edit.original == data

    line_edit.main_widget.setText(new_value.value[0])
    assert line_edit.value == new_value
    assert line_edit.original == data

    line_edit.reset()
    assert line_edit.value == data
    assert line_edit.main_widget.text() == data.value[0]
    assert line_edit.original == data

    line_edit.clear()
    assert line_edit.value is None
    assert line_edit.main_widget.text() == ""
    assert line_edit.original == data

    line_edit.reset()
    assert line_edit.value == data
    assert line_edit.main_widget.text() == data.value[0]


def test_EditLineWidget_isModified(qtbot: QtBot) -> None:
    """Tests that isModified calculates the correct values."""
    initial = TextTagValue(["initial"])
    second = TextTagValue(["second"])

    line_edit = EditLineWidget(initial)
    qtbot.addWidget(line_edit)
    assert line_edit.isModified() is False
    line_edit.value = second
    assert line_edit.isModified() is True
    line_edit.value = initial
    assert line_edit.isModified() is False
    line_edit.value = None
    assert line_edit.isModified() is True
