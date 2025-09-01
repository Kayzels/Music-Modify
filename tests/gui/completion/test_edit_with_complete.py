"""Tests for EditWithComplete."""

from unittest.mock import MagicMock

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QFocusEvent, QKeyEvent
from PySide6.QtWidgets import QComboBox, QWidget
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.completion.edit_with_complete import EditWithComplete


def _createLineEdit(
    qtbot: QtBot, *, add: bool = True
) -> tuple[QWidget, EditWithComplete]:
    """Create an EditWithComplete.

    Due to some issues with tear-down with qtbot,
    pass `add=False` if not wanting to add the line edit to qtbot.
    """
    widget = QWidget()
    qtbot.addWidget(widget)
    edit = EditWithComplete(widget)
    if add:
        qtbot.addWidget(edit)
    return widget, edit


@pytest.mark.parametrize(
    "enabled",
    [
        pytest.param(True, id="enabled"),
        pytest.param(False, id="disabled"),
    ],
)
def test_EditWithComplete_showPopup_param(qtbot: QtBot, enabled: bool) -> None:
    """Tests that popup shows when enabled, and doesn't show when disabled."""
    _, edit = _createLineEdit(qtbot)

    edit.line_edit.complete = MagicMock()
    edit.disable_popup = enabled

    edit.showPopup()

    edit.line_edit.complete.assert_called_once_with(show_all=True)
    assert edit.disable_popup is enabled


def test_EditWithComplete_keyPressEvent_down_process(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that a down keyPressEvent is accepted and not forwarded."""
    _, edit = _createLineEdit(qtbot)

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
    """Test that keyPressEvents other than down are forwarded."""
    _, edit = _createLineEdit(qtbot)

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
    """Tests that setting and getting all_items works."""
    _, edit = _createLineEdit(qtbot)

    items: tuple[str, ...] = ("One", "Two")
    edit.all_items = items
    assert edit.all_items == items
    assert edit.line_edit.all_items == items


def test_EditWithComplete_setElideMode(qtbot: QtBot) -> None:
    """Tests that calling setElideMode sets elide mode for the contained line edit."""
    _, edit = _createLineEdit(qtbot)

    edit.line_edit.setElideMode = MagicMock()

    edit.setElideMode(Qt.TextElideMode.ElideMiddle)

    edit.line_edit.setElideMode.assert_called_once_with(Qt.TextElideMode.ElideMiddle)


def test_EditWithComplete_setCurrentText(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tests that setCurrentText calls on setText and selectAll."""
    _, edit = _createLineEdit(qtbot)

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
    """Tests that FocusOut events are not forwarded if eat focus is True."""
    _, edit = _createLineEdit(qtbot)

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
    """Tests that FocusOut events are forwarded if eat focus is False."""
    _, edit = _createLineEdit(qtbot, add=False)

    edit.eat_focus_out = False
    edit.line_edit.mcompleter.setVisible(True)

    super_event_filter = MagicMock()
    monkeypatch.setattr(QObject, "eventFilter", super_event_filter)

    event = QFocusEvent(QEvent.Type.FocusOut)

    __ = edit.eventFilter(edit, event)

    super_event_filter.assert_called_once_with(edit, event)


def test_EditWithComplete_eventFilter_forwarded_different_object(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tests that events are forwarded if the target object is not the completer."""
    widget, edit = _createLineEdit(qtbot, add=False)

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
    """Tests that events are forwarded when the completer is hidden."""
    _, edit = _createLineEdit(qtbot, add=False)

    edit.eat_focus_out = True
    edit.line_edit.mcompleter.setVisible(False)

    super_event_filter = MagicMock()
    monkeypatch.setattr(QObject, "eventFilter", super_event_filter)

    event = QFocusEvent(QEvent.Type.FocusOut)

    __ = edit.eventFilter(edit, event)

    super_event_filter.assert_called_once_with(edit, event)


def test_EditWithComplete_home(qtbot: QtBot) -> None:
    """Tests that home forwards to the the line edit."""
    _, edit = _createLineEdit(qtbot)

    edit.line_edit.home = MagicMock()

    edit.home(mark=True)
    edit.line_edit.home.assert_called_once_with(True)

    edit.line_edit.home.reset_mock()

    edit.home(mark=False)
    edit.line_edit.home.assert_called_once_with(False)


def test_EditWithComplete_setCursorPosition(qtbot: QtBot) -> None:
    """Tests that calling setCursorPosition forwards it to the line edit."""
    _, edit = _createLineEdit(qtbot)

    edit.line_edit.setCursorPosition = MagicMock()

    edit.setCursorPosition(5)

    edit.line_edit.setCursorPosition.assert_called_once_with(5)


def test_EditWithComplete_textChanged_property(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tests that the textChanged property is set."""
    _, edit = _createLineEdit(qtbot)

    text_changed_signal = MagicMock()
    monkeypatch.setattr(edit.line_edit, "textChanged", text_changed_signal)

    result = edit.textChanged

    assert result == text_changed_signal
