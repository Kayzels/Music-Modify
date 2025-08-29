"""Tests for EditLineWidget."""

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.edit.widget_edit_line import EditLineWidget


def _createLineWidget(
    qtbot: QtBot, data: str | None = None
) -> tuple[QWidget, EditLineWidget]:
    widget = QWidget()
    qtbot.addWidget(widget)
    line_edit = EditLineWidget(widget, data)
    qtbot.addWidget(line_edit)
    return widget, line_edit


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param(None, "", id="init_None"),
        pytest.param("Name", "Name", id="init_value"),
    ],
)
def test_EditLineWidget_init_param(
    qtbot: QtBot, data: str | None, expected: str
) -> None:
    """Tests creating an EditLineWidget based on data type."""
    _, line_edit = _createLineWidget(qtbot, data)
    assert line_edit.value == expected
    assert line_edit.original == expected


def test_EditLineWidget_update_from_widget(qtbot: QtBot) -> None:
    """Tests updating the value by changing the displayed text."""
    data = "Name"
    new_value = "New Value"
    _, line_edit = _createLineWidget(qtbot, data)

    assert line_edit.value == data
    assert line_edit.original == data

    line_edit.main_widget.setText(new_value)
    line_edit.main_widget.editingFinished.emit()

    assert line_edit.value == new_value
    assert line_edit.original == data


def test_EditLineWidget_value_set(qtbot: QtBot) -> None:
    """Tests updating the value directly."""
    data = "Original"
    _, line_edit = _createLineWidget(qtbot, data)

    assert line_edit.value == data
    line_edit.value = "New Value"
    assert line_edit.value == "New Value"


def test_EditLineWidget_clear(qtbot: QtBot) -> None:
    """Tests clearing the value from the widget."""
    data = "Name"
    _, line_edit = _createLineWidget(qtbot, data)

    assert line_edit.value == data
    assert line_edit.original == data

    line_edit.clear()

    assert line_edit.value == ""
    assert line_edit.main_widget.text() == ""
    assert line_edit.original == data


def test_EditLineWidget_reset(qtbot: QtBot) -> None:
    """Tests resetting, clearing, and then resetting the value."""
    data = "Name"
    new_value = "New Value"
    _, line_edit = _createLineWidget(qtbot, data)

    assert line_edit.value == data
    assert line_edit.original == data

    line_edit.main_widget.setText(new_value)
    line_edit.main_widget.editingFinished.emit()
    assert line_edit.value == new_value
    assert line_edit.original == data

    line_edit.reset()
    assert line_edit.value == data
    assert line_edit.main_widget.text() == data
    assert line_edit.original == data

    line_edit.clear()
    assert line_edit.value == ""
    assert line_edit.main_widget.text() == ""
    assert line_edit.original == data

    line_edit.reset()
    assert line_edit.value == data
    assert line_edit.main_widget.text() == data
