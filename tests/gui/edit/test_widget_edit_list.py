"""Tests for EditListWidget."""

import logging

from PySide6.QtWidgets import QListWidget, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.tag_value import (
    AbstractTagValue,
    PairedTextTagValue,
    TextTagValue,
)
from music_modify.gui.edit.widget_edit_list import EditListWidget
from music_modify.gui.utils import selectRows


def test_EditListWidget_init_plain(qtbot: QtBot) -> None:
    """Test creating an EditListWidget directly."""
    widget = QWidget()
    qtbot.addWidget(widget)

    list_widget = EditListWidget(None)
    qtbot.addWidget(list_widget)
    assert list_widget.value is None
    assert list_widget.original is None
    assert isinstance(list_widget.main_widget, QListWidget)


@pytest.mark.parametrize(
    ("initial_value", "expected"),
    [
        pytest.param(None, None, id="init_None"),
        pytest.param(TextTagValue([]), None, id="init_empty"),
        pytest.param(TextTagValue(["One"]), TextTagValue(["One"]), id="init_single"),
        pytest.param(
            TextTagValue(["One", "Two"]),
            TextTagValue(["One", "Two"]),
            id="init_multiple",
        ),
        pytest.param(
            TextTagValue(["One", "Two", "Three"]),
            TextTagValue(["One", "Two", "Three"]),
            id="init_many",
        ),
        pytest.param(
            PairedTextTagValue([["One", "Two"]]),
            None,
            id="init_invalid",
        ),
    ],
)
def test_EditListWidget_init(
    qtbot: QtBot, initial_value: AbstractTagValue | None, expected: TextTagValue | None
) -> None:
    """Test creating an EditListWidget with various data inputs."""
    list_widget = EditListWidget(initial_value)
    qtbot.addWidget(list_widget)
    assert list_widget.value == expected
    assert list_widget.original == expected

    if expected is not None:
        assert list_widget.main_widget.model().rowCount() == max(len(expected.value), 1)
        for i, text in enumerate(expected.value):
            assert list_widget.main_widget.item(i).text() == text
    else:
        assert list_widget.main_widget.model().rowCount() == 1


def test_EditListWidget_value_set(qtbot: QtBot) -> None:
    """Tests updating the value directly."""
    data = TextTagValue(["First", "Second"])
    list_widget = EditListWidget(data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == data
    new_value = TextTagValue(["New Value", "Another"])
    list_widget.value = new_value
    assert list_widget.value == new_value
    for i, text in enumerate(new_value.value):
        assert list_widget.main_widget.item(i).text() == text


def test_EditListWidget_value_None(qtbot: QtBot) -> None:
    """Tests setting the value to None directly."""
    data = TextTagValue(["Original", "More"])
    list_widget = EditListWidget(data)
    qtbot.addWidget(list_widget)

    list_widget.value = None
    assert list_widget.main_widget.model().rowCount() == 1
    assert list_widget.main_widget.item(0).text() == ""
    assert list_widget.value is None


def test_EditLineWidget_value_invalid(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    """Tests that setting an invalid value logs and clears."""
    data = TextTagValue(["Original", "More"])
    list_widget = EditListWidget(data)
    qtbot.addWidget(list_widget)
    assert list_widget.value == data
    new_value = PairedTextTagValue([["first", "second"]])
    with caplog.at_level(logging.WARNING):
        list_widget.value = new_value

    assert list_widget.value is None
    assert "EditListWidget received unexpected value type" in caplog.text


@pytest.mark.parametrize(
    "input_data",
    [
        pytest.param([], id="addRow_empty"),
        pytest.param(["One"], id="addRow_single"),
        pytest.param(["One", "Two"], id="addRow_multiple"),
    ],
)
def test_EditListWidget_addRow(qtbot: QtBot, input_data: list[str]) -> None:
    """Test adding a row for different stored data."""
    initial_row_count = max(len(input_data or []), 1)

    list_widget = EditListWidget(TextTagValue(input_data))
    qtbot.addWidget(list_widget)

    assert list_widget.main_widget.model().rowCount() == initial_row_count
    assert list_widget.add_button is not None
    list_widget.add_button.click()
    assert list_widget.main_widget.model().rowCount() == initial_row_count + 1


@pytest.mark.parametrize(
    ("input_data", "rows", "expected_value"),
    [
        pytest.param(["One", "Two"], None, ["One", "Two"], id="not_selected_not_moved"),
        pytest.param(["One", "Two"], [1], ["Two", "One"], id="single_valid_moved"),
        pytest.param(["One", "Two"], [0], ["One", "Two"], id="single_top_not_moved"),
        pytest.param(
            ["One", "Two", "Three"],
            [1, 2],
            ["Two", "Three", "One"],
            id="contiguous_valid_moved",
        ),
        pytest.param(
            ["One", "Two", "Three"],
            [0, 1],
            ["One", "Two", "Three"],
            id="contiguous_top_not_moved",
        ),
        pytest.param(
            ["One", "Two", "Three", "Four"],
            [1, 3],
            ["Two", "One", "Four", "Three"],
            id="separate_valid_moved",
        ),
        pytest.param(
            ["One", "Two", "Three", "Four"],
            [0, 2],
            ["One", "Two", "Three", "Four"],
            id="separate_top_not_moved",
        ),
    ],
)
def test_EditListWidget_moveRowsUp(
    qtbot: QtBot,
    input_data: list[str],
    rows: list[int] | None,
    expected_value: list[str],
) -> None:
    """Test that moving rows up works correctly based on selection.

    If the top is selected, rows shouldn't move.
    If the rows are separate, they should move individually.
    If contiguous, they should move together.
    If none selected, they shouldn't move.
    """
    list_widget = EditListWidget(TextTagValue(input_data))
    qtbot.addWidget(list_widget)
    expected = TextTagValue(expected_value)

    if rows:
        selectRows(list_widget.main_widget, rows)
    assert list_widget.up_button is not None
    list_widget.up_button.click()
    assert list_widget.value == expected


@pytest.mark.parametrize(
    ("input_data", "rows", "expected_value"),
    [
        pytest.param(["One", "Two"], [], ["One", "Two"], id="not_selected_not_moved"),
        pytest.param(["One", "Two"], [0], ["Two", "One"], id="single_valid_moved"),
        pytest.param(["One", "Two"], [1], ["One", "Two"], id="single_bottom_not_moved"),
        pytest.param(
            ["One", "Two", "Three"],
            [0, 1],
            ["Three", "One", "Two"],
            id="contiguous_valid_moved",
        ),
        pytest.param(
            ["One", "Two", "Three"],
            [1, 2],
            ["One", "Two", "Three"],
            id="contiguous_bottom_not_moved",
        ),
        pytest.param(
            ["One", "Two", "Three", "Four"],
            [0, 2],
            ["Two", "One", "Four", "Three"],
            id="separate_valid_moved",
        ),
        pytest.param(
            ["One", "Two", "Three", "Four"],
            [1, 3],
            ["One", "Two", "Three", "Four"],
            id="separate_bottom_not_moved",
        ),
    ],
)
def test_EditListWidget_moveRowsDown(
    qtbot: QtBot,
    input_data: list[str],
    rows: list[int],
    expected_value: list[str],
) -> None:
    """Test that moving rows down works correctly based on selection.

    If the top bottom selected, rows shouldn't move.
    If the rows are separate, they should move individually.
    If contiguous, they should move together.
    If none selected, they shouldn't move.
    """
    list_widget = EditListWidget(TextTagValue(input_data))
    qtbot.addWidget(list_widget)
    expected = TextTagValue(expected_value)

    selectRows(list_widget.main_widget, rows)
    assert list_widget.down_button is not None
    list_widget.down_button.click()

    assert list_widget.value == expected


@pytest.mark.parametrize(
    ("input_data", "rows", "expected_value"),
    [
        pytest.param(
            ["One", "Two", "Three"],
            [],
            ["One", "Two", "Three"],
            id="none_selected_none_removed",
        ),
        pytest.param(
            ["One", "Two", "Three"],
            [0, 1],
            ["Three"],
            id="multiple_contiguous_selected",
        ),
        pytest.param(
            ["One", "Two", "Three"], [0, 2], ["Two"], id="multiple_separate_selected"
        ),
        pytest.param(["One"], [0], None, id="last_removed"),
    ],
)
def test_EditListWidget_removeRows_param(
    qtbot: QtBot,
    input_data: list[str],
    rows: list[int],
    expected_value: list[str] | None,
) -> None:
    """Tests removing rows based on selection."""
    list_widget = EditListWidget(TextTagValue(input_data))
    qtbot.addWidget(list_widget)
    expected = TextTagValue(expected_value) if expected_value is not None else None

    selectRows(list_widget.main_widget, rows)
    assert list_widget.remove_button is not None
    list_widget.remove_button.click()

    assert list_widget.value == expected
    assert list_widget.original == input_data

    item_texts = expected_value if expected_value else [""]
    for i, text in enumerate(item_texts):
        assert list_widget.main_widget.item(i).text() == text


def test_EditListWidget_clear(qtbot: QtBot) -> None:
    """Tests clearing the widget when clear is clicked."""
    data = TextTagValue(["One", "Two"])
    list_widget = EditListWidget(data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == data

    assert list_widget.clear_button is not None
    list_widget.clear_button.click()
    assert list_widget.value is None
    assert list_widget.original == data
    assert list_widget.main_widget.model().rowCount() == 1
    assert list_widget.main_widget.item(0).text() == ""


def test_EditListWidget_reset(qtbot: QtBot) -> None:
    """Tests resetting the list widget back to the original values."""
    data = TextTagValue(["One", "Two"])
    list_widget = EditListWidget(data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == data
    assert list_widget.clear_button is not None
    list_widget.clear_button.click()
    assert list_widget.value is None
    assert list_widget.original == data
    assert list_widget.reset_button is not None
    list_widget.reset_button.click()
    assert list_widget.value == data


def test_EditListWidget_updateValue(qtbot: QtBot) -> None:
    """Test whether updating the value in the model updates the widget value."""
    data = TextTagValue(["One", "Two"])
    list_widget = EditListWidget(data)
    qtbot.addWidget(list_widget)

    assert list_widget.value == data
    list_widget.main_widget.item(0).setText("New")
    assert list_widget.value == TextTagValue(["New", "Two"])
    assert list_widget.original == TextTagValue(["One", "Two"])


def test_EditListWidget_isModified(qtbot: QtBot) -> None:
    """Tests that isModified calculates the correct values."""
    initial = TextTagValue(["initial", "first"])
    second = TextTagValue(["second", "third"])

    list_widget = EditListWidget(initial)
    qtbot.addWidget(list_widget)
    assert list_widget.isModified() is False
    list_widget.value = second
    assert list_widget.isModified() is True
    list_widget.value = initial
    assert list_widget.isModified() is False
    list_widget.value = None
    assert list_widget.isModified() is True
