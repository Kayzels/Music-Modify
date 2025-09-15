"""Tests for EditTableWidget."""

import logging

import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types.tag_value import (
    AbstractTagValue,
    PairedTextTagValue,
    TextTagValue,
)
from music_modify.gui.edit.widget_edit_table import EditTableWidget
from music_modify.gui.edit.widget_table_drag import DragTableWidget
from music_modify.gui.utils import selectRows


def test_EditTableWidget_init_plain(qtbot: QtBot) -> None:
    """Tests creating an EditTableWidget directly.

    This is done in case there is an issue with the _createTableWidget helper function.
    """
    table_widget = EditTableWidget(None)
    qtbot.addWidget(table_widget)
    assert isinstance(table_widget.main_widget, DragTableWidget)
    assert table_widget.main_widget.rowCount() == 1
    assert table_widget.value is None
    assert table_widget.original is None


@pytest.mark.parametrize(
    ("initial_value", "expected"),
    [
        pytest.param(None, None, id="initial_None"),
        pytest.param(PairedTextTagValue([]), None, id="initial_pair_empty"),
        pytest.param(
            PairedTextTagValue([["first", "second"]]),
            PairedTextTagValue([["first", "second"]]),
            id="initial_pair_value",
        ),
        pytest.param(
            PairedTextTagValue([["first", "second"], ["third", "fourth"]]),
            PairedTextTagValue([["first", "second"], ["third", "fourth"]]),
            id="initial_pair_value_multiple",
        ),
        pytest.param(TextTagValue(["Text"]), None, id="invalid_initial_value"),
    ],
)
def test_EditTableWidget_init(
    qtbot: QtBot,
    initial_value: AbstractTagValue | None,
    expected: PairedTextTagValue | None,
) -> None:
    """Tests that initial values are calculated and set correctly."""
    table_widget = EditTableWidget(initial_value)
    qtbot.addWidget(table_widget)
    assert table_widget.value == expected
    assert table_widget.original == expected
    if expected is not None:
        assert table_widget.main_widget.rowCount() == max(len(expected.value), 1)
        for row, pair in enumerate(expected.value):
            for col, text in enumerate(pair):
                item = table_widget.main_widget.item(row, col)
                assert item is not None
                assert item.text() == text
    else:
        assert table_widget.main_widget.rowCount() == 1


def test_EditTableWidget_value_set(qtbot: QtBot) -> None:
    """Tests updating the value directly."""
    data = PairedTextTagValue([["initial", "first"]])
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data
    new_value = PairedTextTagValue([["new", "second"]])
    table_widget.value = new_value
    assert table_widget.value == new_value
    for row, pair in enumerate(new_value.value):
        for col, text in enumerate(pair):
            item = table_widget.main_widget.item(row, col)
            assert item is not None
            assert item.text() == text


def test_EditTableWidget_value_None(qtbot: QtBot) -> None:
    """Tests setting the value to None directly."""
    data = PairedTextTagValue([["Original", "More"]])
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    table_widget.value = None
    assert table_widget.main_widget.rowCount() == 1
    for i in range(2):
        item = table_widget.main_widget.item(0, i)
        assert item is not None
        assert item.text() == ""
    assert table_widget.value is None


def test_EditTableWidget_value_invalid(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    """Tests that setting an invalid value logs and clears."""
    data = PairedTextTagValue([["Original", "More"]])
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)
    assert table_widget.value == data
    new_value = TextTagValue(["first", "second"])
    with caplog.at_level(logging.WARNING):
        table_widget.value = new_value

    assert table_widget.value is None
    assert table_widget.main_widget.rowCount() == 1
    for i in range(2):
        item = table_widget.main_widget.item(0, i)
        assert item is not None
        assert item.text() == ""
    assert "EditTableWidget received unexpected value type" in caplog.text


@pytest.mark.parametrize(
    "input_data",
    [
        pytest.param([], id="addRow_empty"),
        pytest.param([["first", "second"]], id="addRow_single"),
        pytest.param([["One", "Two"], ["Three", "Four"]], id="addRow_multiple"),
    ],
)
def test_EditListWidget_addRow(qtbot: QtBot, input_data: list[list[str]]) -> None:
    """Test adding a row for different stored data."""
    initial_row_count = max(len(input_data or []), 1)

    table_widget = EditTableWidget(PairedTextTagValue(input_data))
    qtbot.addWidget(table_widget)

    assert table_widget.main_widget.rowCount() == initial_row_count
    assert table_widget.add_button is not None
    table_widget.add_button.click()
    assert table_widget.main_widget.rowCount() == initial_row_count + 1


@pytest.mark.parametrize(
    ("input_data", "rows", "expected_value"),
    [
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
            ],
            [1],
            [
                ["Second Role", "Second Person"],
                ["First Role", "First Person"],
            ],
            id="single_valid_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
            ],
            [0],
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
            ],
            id="single_top_not_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
            ],
            [1, 2],
            [
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
                ["First Role", "First Person"],
            ],
            id="contiguous_valid_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
            ],
            [0, 1],
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
            ],
            id="contiguous_top_not_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
                ["Fourth Role", "Fourth Person"],
            ],
            [1, 3],
            [
                ["Second Role", "Second Person"],
                ["First Role", "First Person"],
                ["Fourth Role", "Fourth Person"],
                ["Third Role", "Third Person"],
            ],
            id="separate_valid_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
                ["Fourth Role", "Fourth Person"],
            ],
            [0, 2],
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
                ["Fourth Role", "Fourth Person"],
            ],
            id="separate_top_not_moved",
        ),
    ],
)
def test_EditTableWidget_moveRowsUp(
    qtbot: QtBot,
    input_data: list[list[str]],
    rows: list[int],
    expected_value: list[list[str]],
) -> None:
    """Test that moving rows up works correctly based on selection.

    If the top is selected, rows shouldn't move.
    If the rows are separate, they should move individually.
    If contiguous, they should move together.
    If none selected, they shouldn't move.
    """
    data = PairedTextTagValue(input_data)
    expected = PairedTextTagValue(expected_value)
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data
    assert table_widget.original == data

    selectRows(table_widget.main_widget, rows)

    assert table_widget.up_button is not None
    table_widget.up_button.click()

    assert table_widget.value == expected
    assert table_widget.original == data


def test_EditTableWidget_moveRows_no_selection(qtbot: QtBot) -> None:
    """Tests moving rows with no selection."""
    data = PairedTextTagValue(
        [
            ["First Role", "First Person"],
            ["Second Role", "Second Person"],
            ["Third Role", "Third Person"],
        ]
    )
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data
    assert table_widget.up_button is not None
    table_widget.up_button.click()
    assert table_widget.value == data


@pytest.mark.parametrize(
    ("input_data", "rows", "expected_value"),
    [
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
            ],
            [0],
            [
                ["Second Role", "Second Person"],
                ["First Role", "First Person"],
            ],
            id="single_valid_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
            ],
            [1],
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
            ],
            id="single_bottom_not_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
            ],
            [0, 1],
            [
                ["Third Role", "Third Person"],
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
            ],
            id="contiguous_valid_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
            ],
            [1, 2],
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
            ],
            id="contiguous_bottom_not_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
                ["Fourth Role", "Fourth Person"],
            ],
            [0, 2],
            [
                ["Second Role", "Second Person"],
                ["First Role", "First Person"],
                ["Fourth Role", "Fourth Person"],
                ["Third Role", "Third Person"],
            ],
            id="separate_valid_moved",
        ),
        pytest.param(
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
                ["Fourth Role", "Fourth Person"],
            ],
            [1, 3],
            [
                ["First Role", "First Person"],
                ["Second Role", "Second Person"],
                ["Third Role", "Third Person"],
                ["Fourth Role", "Fourth Person"],
            ],
            id="separate_bottom_not_moved",
        ),
    ],
)
def test_EditTableWidget_moveRowsDown(
    qtbot: QtBot,
    input_data: list[list[str]],
    rows: list[int],
    expected_value: list[list[str]],
) -> None:
    """Test that moving rows down works correctly based on selection.

    If the bottom is selected, rows shouldn't move.
    If the rows are separate, they should move individually.
    If contiguous, they should move together.
    If none selected, they shouldn't move.
    """
    data = PairedTextTagValue(input_data)
    expected = PairedTextTagValue(expected_value)
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data
    assert table_widget.original == data

    selectRows(table_widget.main_widget, rows)

    assert table_widget.down_button is not None
    table_widget.down_button.click()

    assert table_widget.value == expected
    assert table_widget.original == data


def test_EditTableWidget_removeRows(qtbot: QtBot) -> None:
    """Tests removing row when multiple rows are selected."""
    data = PairedTextTagValue(
        [
            ["First Role", "First Person"],
            ["Second Role", "Second Person"],
            ["Third Role", "Third Person"],
        ]
    )
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data

    selectRows(table_widget.main_widget, [0, 1])
    assert table_widget.remove_button is not None
    table_widget.remove_button.click()

    assert table_widget.value == PairedTextTagValue([["Third Role", "Third Person"]])
    assert table_widget.original == data
    first_item = table_widget.main_widget.item(0, 0)
    assert first_item is not None
    assert first_item.text() == "Third Role"

    second_item = table_widget.main_widget.item(0, 1)
    assert second_item is not None
    assert second_item.text() == "Third Person"


def test_EditTableWidget_removeRow_no_selection(qtbot: QtBot) -> None:
    """Tests that no rows are removed if none are selected."""
    data = PairedTextTagValue(
        [["First Role", "First Person"], ["Second Role", "Second Person"]]
    )
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)
    assert table_widget.value == data

    assert table_widget.remove_button is not None
    table_widget.remove_button.click()
    assert table_widget.value == data


def test_EditTableWidget_removeRow_last_remaining(qtbot: QtBot) -> None:
    """Tests that the row is cleared when there's one left, but the row stays."""
    data = PairedTextTagValue([["First Role", "First Person"]])
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data

    selectRows(table_widget.main_widget, [0])
    assert table_widget.remove_button is not None
    table_widget.remove_button.click()

    assert table_widget.value is None
    assert table_widget.original == data

    assert table_widget.main_widget.rowCount() == 1
    first_item = table_widget.main_widget.item(0, 0)
    assert first_item is not None
    assert first_item.text() == ""
    second_item = table_widget.main_widget.item(0, 1)
    assert second_item is not None
    assert second_item.text() == ""


def test_EditTableWidget_clear(qtbot: QtBot) -> None:
    """Tests that data is cleared from the widget when clear is clicked."""
    data = PairedTextTagValue(
        [["First Role", "First Person"], ["Second Role", "Second Person"]]
    )
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data

    assert table_widget.clear_button is not None
    table_widget.clear_button.click()
    assert table_widget.value is None
    assert table_widget.main_widget.rowCount() == 1
    first_item = table_widget.main_widget.item(0, 0)
    assert first_item is not None
    assert first_item.text() == ""
    second_item = table_widget.main_widget.item(0, 1)
    assert second_item is not None
    assert second_item.text() == ""
    assert table_widget.original == data


def test_EditTableWidget_reset(qtbot: QtBot) -> None:
    """Tests that data is reset when reset button is clicked."""
    data = PairedTextTagValue(
        [
            ["First Role", "First Person"],
            ["Second Role", "Second Person"],
            ["Third Role", "Third Person"],
        ]
    )
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data
    assert table_widget.clear_button is not None
    table_widget.clear_button.click()
    assert table_widget.value is None
    assert table_widget.original == data
    assert table_widget.reset_button is not None
    table_widget.reset_button.click()
    assert table_widget.value == data


def test_EditTableWidget_update_existing(qtbot: QtBot) -> None:
    """Tests that existing values are updated if changed."""
    data = PairedTextTagValue(
        [
            ["First Role", "First Person"],
            ["Second Role", "Second Person"],
            ["Third Role", "Third Person"],
        ]
    )
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data

    first_row_person = table_widget.main_widget.item(0, 1)
    assert first_row_person is not None
    first_row_person.setText("New Person")
    assert table_widget.value == PairedTextTagValue(
        [
            ["First Role", "New Person"],
            ["Second Role", "Second Person"],
            ["Third Role", "Third Person"],
        ]
    )
    assert table_widget.original == data

    first_row_role = table_widget.main_widget.item(0, 0)
    assert first_row_role is not None
    first_row_role.setText("New Role")
    assert table_widget.value == PairedTextTagValue(
        [
            ["New Role", "New Person"],
            ["Second Role", "Second Person"],
            ["Third Role", "Third Person"],
        ]
    )
    assert table_widget.original == data

    second_row_role = table_widget.main_widget.item(1, 0)
    assert second_row_role is not None
    second_row_role.setText("New Role")
    assert table_widget.value == PairedTextTagValue(
        [
            ["New Role", "New Person"],
            ["New Role", "Second Person"],
            ["Third Role", "Third Person"],
        ]
    )
    assert table_widget.original == data


def test_EditTableWidget_update_add_new(qtbot: QtBot) -> None:
    """Tests that adding new values updates correctly."""
    data = PairedTextTagValue(
        [
            ["First Role", "First Person"],
            ["Second Role", "Second Person"],
            ["Third Role", "Third Person"],
        ]
    )
    table_widget = EditTableWidget(data)
    qtbot.addWidget(table_widget)

    assert table_widget.value == data

    assert table_widget.add_button is not None
    table_widget.add_button.click()
    assert table_widget.main_widget.rowCount() == len(data.value) + 1
    last_row_role = table_widget.main_widget.item(len(data.value), 0)
    assert last_row_role is not None
    last_row_role.setText("Extra Role")
    assert table_widget.value == data
    last_row_person = table_widget.main_widget.item(len(data.value), 1)
    assert last_row_person is not None
    last_row_person.setText("Extra Person")
    assert table_widget.value == PairedTextTagValue(
        [
            ["First Role", "First Person"],
            ["Second Role", "Second Person"],
            ["Third Role", "Third Person"],
            ["Extra Role", "Extra Person"],
        ]
    )
    assert table_widget.original == data


def test_EditTableWidget_isModified(qtbot: QtBot) -> None:
    """Tests that isModified calculates the correct values."""
    initial = PairedTextTagValue([["initial", "first"]])
    second = PairedTextTagValue([["second", "third"]])

    table_widget = EditTableWidget(initial)
    qtbot.addWidget(table_widget)
    assert table_widget.isModified() is False
    table_widget.value = second
    assert table_widget.isModified() is True
    table_widget.value = initial
    assert table_widget.isModified() is False
    table_widget.value = None
    assert table_widget.isModified() is True
