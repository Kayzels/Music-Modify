from unittest.mock import MagicMock

from PySide6.QtGui import QDropEvent, QResizeEvent
from PySide6.QtWidgets import QTableWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.edit.widget_table_drag import DragTableWidget


def test_DragTableWidget_dropEvent_emits_rows_reordered(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    table_widget = DragTableWidget()
    qtbot.addWidget(table_widget)

    mock_event = MagicMock(spec=QDropEvent)

    mock_super_drop = MagicMock()
    monkeypatch.setattr(QTableWidget, "dropEvent", mock_super_drop)

    with qtbot.waitSignal(table_widget.rows_reordered, timeout=1000):  # pyright: ignore[reportArgumentType]
        table_widget.dropEvent(mock_event)

    mock_super_drop.assert_called_once_with(mock_event)


def test_DragTableWidget_reszieEvent_calls_adjustColumnWidths(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    table_widget = DragTableWidget()
    qtbot.addWidget(table_widget)

    mock_event = MagicMock(spec=QResizeEvent)

    mock_adjust_widths = MagicMock()
    monkeypatch.setattr(table_widget, "adjustColumnWidths", mock_adjust_widths)

    mock_super_resize = MagicMock()
    monkeypatch.setattr(QTableWidget, "resizeEvent", mock_super_resize)

    table_widget.resizeEvent(mock_event)

    mock_adjust_widths.assert_called_once()
    mock_super_resize.assert_called_once_with(mock_event)
