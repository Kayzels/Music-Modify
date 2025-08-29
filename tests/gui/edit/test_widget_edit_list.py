"""Tests for EditListWidget."""

from PySide6.QtWidgets import QListWidget, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.edit.widget_edit_list import EditListWidget
from music_modify.gui.utils import selectRows


def _createListWidget(
    qtbot: QtBot, data: list[str] | None = None
) -> tuple[QWidget, EditListWidget]:
    widget = QWidget()
    qtbot.addWidget(widget)
    list_widget = EditListWidget(widget, data=data)
    qtbot.addWidget(list_widget)
    return widget, list_widget


def test_EditListWidget_init_plain(qtbot: QtBot) -> None:
    """Test creating an EditListWidget directly."""
    widget = QWidget()
    qtbot.addWidget(widget)

    list_widget = EditListWidget(widget, None)
    qtbot.addWidget(list_widget)
    assert list_widget.value == []
    assert list_widget.original == []
    assert isinstance(list_widget.main_widget, QListWidget)


@pytest.mark.parametrize(
    "input_data",
    [
        pytest.param(None, id="init_None"),
        pytest.param([], id="init_empty"),
        pytest.param(["One"], id="init_single"),
        pytest.param(["One", "Two"], id="init_multiple"),
        pytest.param(["One", "Two", "Three"], id="init_many"),
    ],
)
def test_EditListWidget_init(qtbot: QtBot, input_data: list[str] | None) -> None:
    """Test creating an EditListWidget with various data inputs."""
    expected_internal = input_data if input_data else []
    expected_row_count = max(len(expected_internal), 1)

    _, list_widget = _createListWidget(qtbot, input_data)

    assert list_widget.value == expected_internal
    assert list_widget.original == expected_internal
    assert isinstance(list_widget.main_widget, QListWidget)
    assert list_widget.main_widget.model().rowCount() == expected_row_count

    for i in range(len(expected_internal)):
        assert list_widget.main_widget.item(i).text() == expected_internal[i]


@pytest.mark.parametrize(
    "input_data",
    [
        pytest.param(None, id="addRow_None"),
        pytest.param([], id="addRow_empty"),
        pytest.param(["One"], id="addRow_single"),
        pytest.param(["One", "Two"], id="addRow_multiple"),
    ],
)
def test_EditListWidget_addRow(qtbot: QtBot, input_data: list[str] | None) -> None:
    """Test adding a row for different stored data."""
    initial_row_count = max(len(input_data or []), 1)

    _, list_widget = _createListWidget(qtbot, input_data)

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
    _, list_widget = _createListWidget(qtbot, input_data)

    if rows:
        selectRows(list_widget.main_widget, rows)
    assert list_widget.up_button is not None
    list_widget.up_button.click()
    assert list_widget.value == expected_value


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
    _, list_widget = _createListWidget(qtbot, input_data)

    selectRows(list_widget.main_widget, rows)
    assert list_widget.down_button is not None
    list_widget.down_button.click()

    assert list_widget.value == expected_value


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
        pytest.param(["One"], [0], [], id="last_removed"),
    ],
)
def test_EditListWidget_removeRows_param(
    qtbot: QtBot, input_data: list[str], rows: list[int], expected_value: list[str]
) -> None:
    """Tests removing rows based on selection."""
    _, list_widget = _createListWidget(qtbot, input_data)

    selectRows(list_widget.main_widget, rows)
    assert list_widget.remove_button is not None
    list_widget.remove_button.click()

    assert list_widget.value == expected_value
    assert list_widget.original == input_data

    item_texts = expected_value if expected_value else [""]
    for i, text in enumerate(item_texts):
        assert list_widget.main_widget.item(i).text() == text


def test_EditListWidget_clear(qtbot: QtBot) -> None:
    """Tests clearing the widget when clear is clicked."""
    data = ["One", "Two"]
    _, list_widget = _createListWidget(qtbot, data)

    assert list_widget.value == data

    assert list_widget.clear_button is not None
    list_widget.clear_button.click()
    assert list_widget.value == []
    assert list_widget.original == data
    assert list_widget.main_widget.model().rowCount() == 1
    assert list_widget.main_widget.item(0).text() == ""


def test_EditListWidget_reset(qtbot: QtBot) -> None:
    """Tests resetting the list widget back to the original valiues."""
    data = ["One", "Two"]
    _, list_widget = _createListWidget(qtbot, data)

    assert list_widget.value == data
    assert list_widget.clear_button is not None
    list_widget.clear_button.click()
    assert list_widget.value == []
    assert list_widget.original == data
    assert list_widget.reset_button is not None
    list_widget.reset_button.click()
    assert list_widget.value == data


def test_EditListWidget_updateValue(qtbot: QtBot) -> None:
    """Test whether updating the value in the model updates the widget value."""
    data = ["One", "Two"]
    _, list_widget = _createListWidget(qtbot, data)

    assert list_widget.value == ["One", "Two"]
    list_widget.main_widget.item(0).setText("New")
    assert list_widget.value == ["New", "Two"]
    assert list_widget.original == ["One", "Two"]
