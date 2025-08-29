"""Tests for DragTableWidget."""

from unittest.mock import MagicMock

from PySide6.QtGui import QDropEvent, QResizeEvent
from PySide6.QtWidgets import QTableWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.edit.widget_table_drag import DragTableWidget


def _createWidget(qtbot: QtBot) -> DragTableWidget:
    table_widget = DragTableWidget()
    qtbot.addWidget(table_widget)
    return table_widget


def test_DragTableWidget_dropEvent_emits_rows_reordered(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that when dropEvent occurs, rows_reordered gets emitted."""
    table_widget = _createWidget(qtbot)

    mock_event = MagicMock(spec=QDropEvent)

    mock_super_drop = MagicMock()
    monkeypatch.setattr(QTableWidget, "dropEvent", mock_super_drop)

    with qtbot.waitSignal(table_widget.rows_reordered, timeout=1000):
        table_widget.dropEvent(mock_event)

    mock_super_drop.assert_called_once_with(mock_event)


def test_DragTableWidget_resizeEvent_calls_adjustColumnWidths(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that when resizeEvent occurs, adjustColumnWidths is called."""
    table_widget = _createWidget(qtbot)

    mock_event = MagicMock(spec=QResizeEvent)

    mock_adjust_widths = MagicMock()
    monkeypatch.setattr(table_widget, "adjustColumnWidths", mock_adjust_widths)

    mock_super_resize = MagicMock()
    monkeypatch.setattr(QTableWidget, "resizeEvent", mock_super_resize)

    table_widget.resizeEvent(mock_event)

    mock_adjust_widths.assert_called_once()
    mock_super_resize.assert_called_once_with(mock_event)
