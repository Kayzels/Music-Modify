"""Tests for RowOperationMixin."""
# pyright: reportPrivateUsage = false

import logging
from typing import override

from PySide6.QtWidgets import QToolButton, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.core.enums import EditButton, RowDirection
from music_modify.gui.mixins.row_operation_mixin import RowOperationMixin


class _OperationWidget(QWidget, RowOperationMixin):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    @override
    def _moveRows(self, direction: RowDirection) -> None:
        pass

    @override
    def _addRow(self) -> None:
        pass

    @override
    def _removeRow(self) -> None:
        pass


def test_RowOperationMixin_createOperationButton_missing_order(qtbot: QtBot) -> None:
    """Test that an exception is raised when a button is missing in order."""
    widget = _OperationWidget()
    qtbot.addWidget(widget)

    order: tuple[EditButton, EditButton, EditButton, EditButton] = (
        EditButton.Up,
        EditButton.Add,
        EditButton.Remove,
        EditButton.Reset,
    )

    expected_exception_message = f"Missing required button in order: {EditButton.Down}"

    with pytest.raises(Exception, match=expected_exception_message) as exc_info:
        _ = widget.createOperationButtons(widget, order=order)

    assert str(exc_info.value) == expected_exception_message


@pytest.mark.parametrize(
    ("button_type", "button_name"),
    [
        pytest.param(EditButton.Up, "up_button", id="up_button"),
        pytest.param(EditButton.Down, "down_button", id="down_button"),
        pytest.param(EditButton.Add, "add_button", id="add_button"),
        pytest.param(EditButton.Remove, "remove_button", id="remove_button"),
    ],
)
def test_RowOperationMixin_createOperationButton_sets_attributes_individual(
    qtbot: QtBot, button_type: EditButton, button_name: str
) -> None:
    """Test that createOperationButtons creates attributes with single calls."""
    widget = _OperationWidget()
    qtbot.addWidget(widget)

    assert not hasattr(widget, button_name)
    _ = widget.createOperationButtons(widget, button_type)
    assert hasattr(widget, button_name)
    assert isinstance(getattr(widget, button_name), QToolButton)


def test_RowOperationMixin_createOperationButton_sets_attributes_multiple(
    qtbot: QtBot,
) -> None:
    """Test that createOperationButtons creates attributes with multiple calls."""
    widget = _OperationWidget()
    qtbot.addWidget(widget)

    assert not hasattr(widget, "up_button")
    assert not hasattr(widget, "down_button")
    assert not hasattr(widget, "remove_button")
    assert not hasattr(widget, "add_button")
    _ = widget.createOperationButtons(
        widget, EditButton.Up | EditButton.Down | EditButton.Remove | EditButton.Add
    )
    assert hasattr(widget, "up_button")
    assert hasattr(widget, "down_button")
    assert hasattr(widget, "remove_button")
    assert hasattr(widget, "add_button")
    assert isinstance(widget.up_button, QToolButton)
    assert isinstance(widget.down_button, QToolButton)
    assert isinstance(widget.remove_button, QToolButton)
    assert isinstance(widget.add_button, QToolButton)


def test_RowOperationMixin_createOperationButton_custom_order(
    qtbot: QtBot,
) -> None:
    """Test that createOperationButtons creates buttons in custom order."""
    widget = _OperationWidget()
    qtbot.addWidget(widget)

    new_buttons = widget.createOperationButtons(
        widget,
        order=(EditButton.Add, EditButton.Remove, EditButton.Down, EditButton.Up),
    )
    assert new_buttons[0] == widget.add_button
    assert new_buttons[1] == widget.remove_button
    assert new_buttons[2] == widget.down_button
    assert new_buttons[3] == widget.up_button


def test_RowOperationMixin_non_single_flag_raises_error(qtbot: QtBot) -> None:
    """Test calling methods expecting single flags with multiple raises exceptions."""
    widget = _OperationWidget()
    qtbot.addWidget(widget)
    composite_flag = EditButton.Add | EditButton.Remove
    temp_button = QToolButton(widget)

    expected_exception_message = "button_type must be a single EditButton flag."

    # Test _createSignalConnection
    with pytest.raises(ValueError, match=expected_exception_message) as exc_info:
        widget._createSignalConnection(temp_button, composite_flag)
    assert str(exc_info.value) == expected_exception_message

    # Test _setAttribute
    with pytest.raises(ValueError, match=expected_exception_message) as exc_info:
        widget._setAttribute(temp_button, composite_flag)
    assert str(exc_info.value) == expected_exception_message

    # Test _setIcon
    with pytest.raises(ValueError, match=expected_exception_message) as exc_info:
        widget._setIcon(temp_button, composite_flag)
    assert str(exc_info.value) == expected_exception_message


def test_RowOperationMixin_createSignalConnection_log_invalid_type(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    """Test trying to create a connection for invalid button sends log message."""
    widget = _OperationWidget()
    qtbot.addWidget(widget)

    unused_flag = EditButton.Reset
    temp_button = QToolButton(widget)

    expected_message = f"Invalid button type called: {unused_flag}. No action taken."

    with caplog.at_level(logging.INFO):
        widget._createSignalConnection(temp_button, unused_flag)

    assert expected_message in caplog.text
    assert caplog.records[0].levelname == "INFO"
    assert caplog.records[0].message == expected_message


def test_RowOperationMixin_setAttribute_log_invalid_type(
    qtbot: QtBot, caplog: pytest.LogCaptureFixture
) -> None:
    """Test trying to set an attribute for invalid button sends log message."""
    widget = _OperationWidget()
    qtbot.addWidget(widget)

    unused_flag = EditButton.Clear
    temp_button = QToolButton(widget)

    expected_message = f"Invalid button type called: {unused_flag}. No action taken."

    with caplog.at_level(logging.INFO):
        widget._setAttribute(temp_button, unused_flag)

    assert expected_message in caplog.text
    assert caplog.records[0].levelname == "INFO"
    assert caplog.records[0].message == expected_message
