"""Tests for EditTableWidget."""

from unittest.mock import MagicMock

from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.custom_types import constants
from music_modify.gui.edit.widget_edit_table import EditTableWidget
from music_modify.gui.edit.widget_table_drag import DragTableWidget
from music_modify.gui.utils import selectRows


def _createTableWidget(
    qtbot: QtBot,
    data: list[list[str]] | None = None,
    *,
    labels: list[str] | None = None,
) -> tuple[QWidget, EditTableWidget]:
    widget = QWidget()
    qtbot.addWidget(widget)
    table_widget = EditTableWidget(widget, data=data, labels=labels)
    qtbot.addWidget(table_widget)
    return widget, table_widget


def test_EditTableWidget_init_plain(qtbot: QtBot) -> None:
    """Tests creating an EditTableWidget directly.

    This is done in case there is an issue with the _createTableWidget helper function.
    """
    widget = QWidget()
    qtbot.addWidget(widget)
    table_widget = EditTableWidget(widget, data=None)
    qtbot.addWidget(table_widget)
    assert isinstance(table_widget.main_widget, DragTableWidget)


@pytest.mark.parametrize(
    ("data", "labels"),
    [
        pytest.param(None, None, id="data_None_labels_None"),
        pytest.param([["Some Role", "Some Name"]], None, id="data_set_labels_None"),
        pytest.param([], None, id="data_empty_labels_None"),
        pytest.param(None, ["First", "Second"], id="data_None_labels_set"),
        pytest.param(
            None, ["First", "Second", "Third"], id="data_None_labels_wrong_size"
        ),
        pytest.param(
            [["Some Role", "Some Name"], ["Another Role", "Another Name"]],
            ["First", "Second"],
            id="data_set_labels_set",
        ),
        pytest.param(
            [["Some Role", "Some Name"]],
            ["First", "Second", "Third"],
            id="data_set_labels_wrong_size",
        ),
        pytest.param([], ["First", "Second"], id="data_empty_labels_set"),
        pytest.param(
            [], ["First", "Second", "Third"], id="data_empty_labels_wrong_size"
        ),
    ],
)
def test_EditTableWidget_init(
    qtbot: QtBot, data: list[list[str]] | None, labels: list[str] | None
) -> None:
    """Test creating an EditTableWidget with different data or labels."""
    expected_labels = (
        ["Role", "Person"]
        if labels is None or len(labels) != constants.PEOPLE_COL_COUNT
        else labels
    )
    expected_data = [] if data is None else data
    expected_row_count = 1 if not data else len(data)

    _, table_widget = _createTableWidget(qtbot, data=data, labels=labels)
    assert table_widget.value == expected_data
    assert table_widget.original == expected_data
    assert table_widget.labels == expected_labels
    assert isinstance(table_widget.main_widget, DragTableWidget)
    assert table_widget.main_widget.columnCount() == 2
    assert table_widget.main_widget.rowCount() == expected_row_count


@pytest.mark.parametrize(
    "data",
    [
        pytest.param(None, id="None_value"),
        pytest.param([], id="empty_value"),
        pytest.param([["Some Role", "Some Person"]], id="single_value"),
        pytest.param(
            [["Some Role", "Some Person"], ["Another Role", "Another Person"]],
            id="multiple_value",
        ),
    ],
)
def test_EditTableWidget_addRow(qtbot: QtBot, data: list[list[str]] | None) -> None:
    """Test adding a row to the widget, when there are values or not."""
    # Always have at least one row for editing
    original_row_count = max(len(data or []), 1)
    expected_row_count = original_row_count + 1

    _, table_widget = _createTableWidget(qtbot, data=data)

    assert table_widget.main_widget.rowCount() == original_row_count
    assert table_widget.add_button is not None
    table_widget.add_button.click()
    assert table_widget.main_widget.rowCount() == expected_row_count


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
    _, table_widget = _createTableWidget(qtbot, input_data)

    assert table_widget.value == input_data
    assert table_widget.original == input_data

    selectRows(table_widget.main_widget, rows)

    assert table_widget.up_button is not None
    table_widget.up_button.click()

    assert table_widget.value == expected_value
    assert table_widget.original == input_data


def test_EditTableWidget_moveRows_no_selection(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tests moving rows with no selection."""
    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    _, table_widget = _createTableWidget(qtbot, data)

    mock_take_item = MagicMock()
    mock_remove_row = MagicMock()
    mock_insert_row = MagicMock()
    mock_set_item = MagicMock()

    monkeypatch.setattr(table_widget.main_widget, "takeItem", mock_take_item)
    monkeypatch.setattr(table_widget.main_widget, "removeRow", mock_remove_row)
    monkeypatch.setattr(table_widget.main_widget, "insertRow", mock_insert_row)
    monkeypatch.setattr(table_widget.main_widget, "setItem", mock_set_item)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    # Ensure that nothing breaks when nothing selected and trying to move rows
    assert table_widget.up_button is not None
    table_widget.up_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.down_button is not None
    table_widget.down_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    mock_take_item.assert_not_called()
    mock_remove_row.assert_not_called()
    mock_insert_row.assert_not_called()
    mock_set_item.assert_not_called()


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
    _, table_widget = _createTableWidget(qtbot, input_data)

    assert table_widget.value == input_data
    assert table_widget.original == input_data

    selectRows(table_widget.main_widget, rows)

    assert table_widget.down_button is not None
    table_widget.down_button.click()

    assert table_widget.value == expected_value
    assert table_widget.original == input_data


def test_EditTableWidget_removeRows(qtbot: QtBot) -> None:
    """Tests removing row when multiple rows are selected."""
    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    _, table_widget = _createTableWidget(qtbot, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    selectRows(table_widget.main_widget, [0, 1])
    assert table_widget.remove_button is not None
    table_widget.remove_button.click()

    assert table_widget.value == [["Third Role", "Third Person"]]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    first_item = table_widget.main_widget.item(0, 0)
    assert first_item is not None
    assert first_item.text() == "Third Role"

    second_item = table_widget.main_widget.item(0, 1)
    assert second_item is not None
    assert second_item.text() == "Third Person"


def test_EditTableWidget_removeRow_no_selection(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tests that no rows are removed if none are selected."""
    data = [["First Role", "First Person"], ["Second Role", "Second Person"]]
    _, table_widget = _createTableWidget(qtbot, data)

    mock_remove_row = MagicMock()
    monkeypatch.setattr(table_widget.main_widget, "removeRow", mock_remove_row)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    assert table_widget.remove_button is not None
    table_widget.remove_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    mock_remove_row.assert_not_called()


def test_EditTableWidget_removeRow_last_remaining(qtbot: QtBot) -> None:
    """Tests that the row is cleared when there's one left, but the row stays."""
    data = [["First Role", "First Person"]]
    _, table_widget = _createTableWidget(qtbot, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
    ]

    selectRows(table_widget.main_widget, [0])
    assert table_widget.remove_button is not None
    table_widget.remove_button.click()

    assert table_widget.value == []
    assert table_widget.original == [["First Role", "First Person"]]

    assert table_widget.main_widget.rowCount() == 1
    first_item = table_widget.main_widget.item(0, 0)
    assert first_item is not None
    assert first_item.text() == ""
    second_item = table_widget.main_widget.item(0, 1)
    assert second_item is not None
    assert second_item.text() == ""


def test_EditTableWidget_clear(qtbot: QtBot) -> None:
    """Tests that data is cleared from the widget when clear is clicked."""
    data = [["First Role", "First Person"], ["Second Role", "Second Person"]]
    _, table_widget = _createTableWidget(qtbot, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]

    assert table_widget.clear_button is not None
    table_widget.clear_button.click()
    assert table_widget.value == []
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
    ]


def test_EditTableWidget_reset(qtbot: QtBot) -> None:
    """Tests that data is reset when reset button is clicked."""
    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    _, table_widget = _createTableWidget(qtbot, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.clear_button is not None
    table_widget.clear_button.click()
    assert table_widget.value == []
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.reset_button is not None
    table_widget.reset_button.click()
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]


def test_EditTableWidget_update_existing(qtbot: QtBot) -> None:
    """Tests that existing values are updated if changed."""
    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    _, table_widget = _createTableWidget(qtbot, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    first_row_person = table_widget.main_widget.item(0, 1)
    assert first_row_person is not None
    first_row_person.setText("New Person")
    assert table_widget.value == [
        ["First Role", "New Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    first_row_role = table_widget.main_widget.item(0, 0)
    assert first_row_role is not None
    first_row_role.setText("New Role")
    assert table_widget.value == [
        ["New Role", "New Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    second_row_role = table_widget.main_widget.item(1, 0)
    assert second_row_role is not None
    second_row_role.setText("New Role")
    assert table_widget.value == [
        ["New Role", "New Person"],
        ["New Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]


def test_EditTableWidget_update_add_new(qtbot: QtBot) -> None:
    """Tests that adding new values updates correctly."""
    data = [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    _, table_widget = _createTableWidget(qtbot, data)

    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]

    assert table_widget.add_button is not None
    table_widget.add_button.click()
    assert table_widget.main_widget.rowCount() == 4
    last_row_role = table_widget.main_widget.item(3, 0)
    assert last_row_role is not None
    last_row_role.setText("Extra Role")
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
    last_row_person = table_widget.main_widget.item(3, 1)
    assert last_row_person is not None
    last_row_person.setText("Extra Person")
    assert table_widget.value == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
        ["Extra Role", "Extra Person"],
    ]
    assert table_widget.original == [
        ["First Role", "First Person"],
        ["Second Role", "Second Person"],
        ["Third Role", "Third Person"],
    ]
