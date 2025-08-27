from unittest.mock import MagicMock

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QFocusEvent, QKeyEvent
from PySide6.QtWidgets import QComboBox, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.completion.edit_with_complete import EditWithComplete


def test_EditWithComplete_showPopup_disabled(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    edit.line_edit.complete = MagicMock()
    edit.disable_popup = True

    edit.showPopup()

    edit.line_edit.complete.assert_called_once_with(show_all=True)
    assert edit.disable_popup is True


def test_EditWithComplete_showPopup_enabled(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    edit.line_edit.complete = MagicMock()
    edit.disable_popup = False

    edit.showPopup()

    edit.line_edit.complete.assert_called_once_with(show_all=True)
    assert edit.disable_popup is False


def test_EditWithComplete_keyPressEvent_down_process(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    edit.disable_popup = False

    mock_super_event = MagicMock()
    monkeypatch.setattr(QComboBox, "keyPressEvent", mock_super_event)

    edit.showPopup = MagicMock()

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_Down, Qt.KeyboardModifier.NoModifier
    )
    assert not edit.line_edit.text()

    edit.keyPressEvent(event)

    assert event.isAccepted()
    edit.showPopup.assert_called_once()
    mock_super_event.assert_not_called()


def test_EditWithComplete_keyPressEvent_other_forwarded(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    mock_super_event = MagicMock()
    monkeypatch.setattr(QComboBox, "keyPressEvent", mock_super_event)

    edit.showPopup = MagicMock()

    event = QKeyEvent(
        QEvent.Type.KeyPress, Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier
    )

    edit.keyPressEvent(event)

    edit.showPopup.assert_not_called()
    mock_super_event.assert_called_once_with(event)


def test_EditWithComplete_all_items(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    items: tuple[str, ...] = ("One", "Two")
    edit.all_items = items
    assert edit.all_items == items
    assert edit.line_edit.all_items == items


def test_EditWithComplete_setElideMode(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    edit.line_edit.setElideMode = MagicMock()

    edit.setElideMode(Qt.TextElideMode.ElideMiddle)

    edit.line_edit.setElideMode.assert_called_once_with(Qt.TextElideMode.ElideMiddle)


def test_EditWithComplete_setCurrentText(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    super_set_current = MagicMock()
    monkeypatch.setattr(QComboBox, "setCurrentText", super_set_current)

    edit.setText = MagicMock()
    edit.selectAll = MagicMock()

    edit.setCurrentText("Some text")

    edit.setText.assert_called_once_with("Some text")
    edit.selectAll.assert_called_once()
    super_set_current.assert_not_called()


def test_EditWithComplete_eventFilter_not_forwarded(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    edit.eat_focus_out = True
    edit.line_edit.mcompleter.setVisible(True)

    super_event_filter = MagicMock()
    monkeypatch.setattr(QObject, "eventFilter", super_event_filter)

    event = QFocusEvent(QEvent.Type.FocusOut)

    result = edit.eventFilter(edit, event)

    assert result is True
    super_event_filter.assert_not_called()


def test_EditWithComplete_eventFilter_forwarded_eat_focus_out_false(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)

    edit.eat_focus_out = False
    edit.line_edit.mcompleter.setVisible(True)

    super_event_filter = MagicMock()
    monkeypatch.setattr(QObject, "eventFilter", super_event_filter)

    event = QFocusEvent(QEvent.Type.FocusOut)

    _ = edit.eventFilter(edit, event)

    super_event_filter.assert_called_once_with(edit, event)


def test_EditWithComplete_eventFilter_forwarded_different_object(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    edit.eat_focus_out = True
    edit.line_edit.mcompleter.setVisible(True)

    super_event_filter = MagicMock()
    monkeypatch.setattr(QObject, "eventFilter", super_event_filter)

    event = QFocusEvent(QEvent.Type.FocusOut)

    _ = edit.eventFilter(widget, event)

    super_event_filter.assert_called_once_with(widget, event)


def test_EditWithComplete_eventFilter_forwarded_completer_hidden(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)

    edit.eat_focus_out = True
    edit.line_edit.mcompleter.setVisible(False)

    super_event_filter = MagicMock()
    monkeypatch.setattr(QObject, "eventFilter", super_event_filter)

    event = QFocusEvent(QEvent.Type.FocusOut)

    _ = edit.eventFilter(edit, event)

    super_event_filter.assert_called_once_with(edit, event)


def test_EditWithComplete_home(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    edit.line_edit.home = MagicMock()

    edit.home(mark=True)
    edit.line_edit.home.assert_called_once_with(True)  # noqa: FBT003

    edit.line_edit.home.reset_mock()

    edit.home(mark=False)
    edit.line_edit.home.assert_called_once_with(False)  # noqa: FBT003


def test_EditWithComplete_setCursorPosition(qtbot: QtBot) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    edit.line_edit.setCursorPosition = MagicMock()

    edit.setCursorPosition(5)

    edit.line_edit.setCursorPosition.assert_called_once_with(5)


def test_EditWithComplete_textChanged_property(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    qtbot.addWidget(edit)

    text_changed_signal = MagicMock()
    monkeypatch.setattr(edit.line_edit, "textChanged", text_changed_signal)

    result = edit.textChanged

    assert result == text_changed_signal
