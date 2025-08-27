from typing import cast
from unittest.mock import MagicMock, Mock

from PySide6.QtCore import QEvent, QModelIndex, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
import pytest
from pytestqt.qtbot import QtBot

from music_modify.gui.completion._complete_line_edit import EnLineEdit
from music_modify.gui.completion._completer import Completer
from music_modify.prefs import prefs


def test_EnLineEdit_init(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    assert line_edit.no_popup is False
    assert line_edit.multiple is True


def test_EnLineEdit_all_items(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    line_edit.all_items = ("One",)
    assert line_edit.all_items == ("One",)


def test_EnLineEdit_disable_popup(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    line_edit.disable_popup = True
    assert line_edit.disable_popup is True


def test_EnLineEdit_setElideMode(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    line_edit.mcompleter.setTextElideMode = MagicMock()

    line_edit.setElideMode(Qt.TextElideMode.ElideMiddle)
    line_edit.mcompleter.setTextElideMode.assert_called_once_with(
        Qt.TextElideMode.ElideMiddle
    )


def test_EnLineEdit_updateItemsCache(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    items: tuple[str, ...] = ("Item A", "Item B", "Item C")
    line_edit.updateItemsCache(items)
    assert line_edit.all_items == items


def test_EnLineEdit_event_shortcutOverride_controlKey(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    # Mock the super QLineEdit event call
    mock_super_event = MagicMock(return_value=True)
    monkeypatch.setattr(QLineEdit, "event", mock_super_event)

    # Create a mock QKeyEvent
    mock_key_event = MagicMock(spec=QKeyEvent)
    mock_key_event.type.return_value = QEvent.Type.ShortcutOverride
    mock_key_event.key.return_value = Qt.Key.Key_Left
    mock_key_event.modifiers.return_value = Qt.KeyboardModifier.ControlModifier
    mock_key_event.accept = MagicMock()

    # Call the event method
    result = line_edit.event(mock_key_event)

    # Assert that event.accept() was called
    mock_key_event.accept.assert_called_once()
    # Also ensure that super().event was called as well, which is default True
    assert result is True


def test_EnLineEdit_event_shortcutOverride_noControlKey(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    # Mock the super QLineEdit event call
    mock_super_event = MagicMock(return_value=True)
    monkeypatch.setattr(QLineEdit, "event", mock_super_event)

    # Create a mock QKeyEvent without ControlModifier
    mock_key_event = MagicMock(spec=QKeyEvent)
    mock_key_event.type.return_value = QEvent.Type.ShortcutOverride
    mock_key_event.key.return_value = Qt.Key.Key_Left
    mock_key_event.modifiers.return_value = (
        Qt.KeyboardModifier.ShiftModifier
    )  # Not Control
    mock_key_event.accept = MagicMock()

    # Call the event method
    result = line_edit.event(mock_key_event)

    # Assert that event.accept() was NOT called
    mock_key_event.accept.assert_not_called()
    # And that the super().event result is returned (which typically is True for a handled event)
    assert result is True


def test_EnLineEdit_event_otherEventType(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    # Mock the super QLineEdit event call
    mock_super_event = MagicMock(return_value=True)
    monkeypatch.setattr(QLineEdit, "event", mock_super_event)

    # Create a mock QEvent of a different type
    mock_event = MagicMock(spec=QEvent)
    mock_event.type.return_value = QEvent.Type.MouseMove
    mock_event.accept = MagicMock()  # This should not be called by our logic

    # Call the event method
    result = line_edit.event(mock_event)

    # Assert that event.accept() was NOT called by our specific logic
    mock_event.accept.assert_not_called()
    # And that the super().event result is returned
    assert result is True


def test_EnLineEdit_event_attributeError(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    mock_super_event = MagicMock(return_value=True)
    monkeypatch.setattr(QLineEdit, "event", mock_super_event)

    # Create a mock event that will raise AttributeError when key() or modifiers() is accessed
    # to simulate the scenario where cast(QKeyEvent, event) might fail or the object lacks expected attributes.
    mock_bad_event = MagicMock(spec=QEvent)
    mock_bad_event.type.return_value = QEvent.Type.ShortcutOverride
    # This will ensure accessing 'key' or 'modifiers' on the cast event raises AttributeError
    type(mock_bad_event).key = MagicMock(
        side_effect=AttributeError("Mock AttributeError for key")
    )
    type(mock_bad_event).modifiers = MagicMock(
        side_effect=AttributeError("Mock AttributeError for modifiers")
    )
    mock_bad_event.accept = MagicMock()

    # The AttributeError should be caught internally, and super().event should still be called.
    result = line_edit.event(mock_bad_event)

    mock_bad_event.accept.assert_not_called()  # Should not be called because of the error before it.
    mock_super_event.assert_called_once_with(mock_bad_event)
    assert result is True


def test_EnLineEdit_complete_noItems(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    # Mock mcompleter and its components
    line_edit.mcompleter = MagicMock(spec=Completer)
    line_edit.mcompleter.complete_model = MagicMock()
    line_edit.mcompleter.complete_model.current_items = []  # No items
    line_edit.mcompleter.hide = MagicMock()
    line_edit.mcompleter.popup = MagicMock()

    line_edit.complete()

    line_edit.mcompleter.hide.assert_called_once()
    line_edit.mcompleter.popup.assert_not_called()


def test_EnLineEdit_complete_withItems_default(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    # Mock mcompleter and its components
    line_edit.mcompleter = MagicMock(spec=Completer)
    line_edit.mcompleter.complete_model = MagicMock()
    line_edit.mcompleter.complete_model.current_items = ["Item 1"]  # Has items
    line_edit.mcompleter.hide = MagicMock()
    line_edit.mcompleter.popup = MagicMock()
    line_edit.mcompleter.scrollToItem = MagicMock()
    line_edit.setFocus = MagicMock()

    line_edit.complete()

    line_edit.mcompleter.hide.assert_not_called()
    line_edit.mcompleter.popup.assert_called_once_with(select_first=True)
    cast(Mock, line_edit.setFocus).assert_called_once_with(
        Qt.FocusReason.OtherFocusReason
    )
    line_edit.mcompleter.scrollToItem.assert_called_once_with(None)


def test_EnLineEdit_complete_showAll(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    # Mock mcompleter and its components
    line_edit.mcompleter = MagicMock(spec=Completer)
    line_edit.mcompleter.complete_model = MagicMock()
    line_edit.mcompleter.complete_model.current_items = ["Item 1"]  # Has items
    line_edit.mcompleter.complete_model.current_prefix = "it"
    line_edit.mcompleter.hide = MagicMock()
    line_edit.mcompleter.popup = MagicMock()
    line_edit.mcompleter.setCompletionPrefix = MagicMock()
    line_edit.mcompleter.scrollToItem = MagicMock()
    line_edit.setFocus = MagicMock()

    line_edit.complete(show_all=True)

    line_edit.mcompleter.setCompletionPrefix.assert_called_once_with("")
    line_edit.mcompleter.hide.assert_not_called()
    line_edit.mcompleter.popup.assert_called_once_with(select_first=True)
    line_edit.setFocus.assert_called_once_with(Qt.FocusReason.OtherFocusReason)
    line_edit.mcompleter.scrollToItem.assert_called_once_with("it")


def test_EnLineEdit_complete_selectFirstFalse(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    # Mock mcompleter and its components
    line_edit.mcompleter = MagicMock(spec=Completer)
    line_edit.mcompleter.complete_model = MagicMock()
    line_edit.mcompleter.complete_model.current_items = ["Item 1"]  # Has items
    line_edit.mcompleter.popup = MagicMock()

    line_edit.complete(select_first=False)

    line_edit.mcompleter.popup.assert_called_once_with(select_first=False)


def test_EnLineEdit_updateCompletions_singleMode(qtbot: QtBot) -> None:
    line_edit = EnLineEdit(multiple=False)
    qtbot.addWidget(line_edit)

    line_edit.setText("  hello world")
    line_edit.setCursorPosition(7)  # Cursor after "hello "

    line_edit.mcompleter.setCompletionPrefix = MagicMock()

    line_edit.updateCompletions()

    assert line_edit.original_cursor_pos == 7
    line_edit.mcompleter.setCompletionPrefix.assert_called_once_with("hello")


def test_EnLineEdit_updateCompletions_multipleMode_withSeparator(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ","
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("item1, item2, prefix")
    line_edit.setCursorPosition(len("item1, item2, prefix"))

    line_edit.mcompleter.setCompletionPrefix = MagicMock()

    line_edit.updateCompletions()

    assert line_edit.original_cursor_pos == len("item1, item2, prefix")
    line_edit.mcompleter.setCompletionPrefix.assert_called_once_with("prefix")


def test_EnLineEdit_updateCompletions_multipleMode_noSeparator(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ","
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("just_one_item")
    line_edit.setCursorPosition(len("just_one_item"))

    line_edit.mcompleter.setCompletionPrefix = MagicMock()

    line_edit.updateCompletions()

    assert line_edit.original_cursor_pos == len("just_one_item")
    line_edit.mcompleter.setCompletionPrefix.assert_called_once_with("just_one_item")


def test_EnLineEdit_updateCompletions_emptyText(qtbot: QtBot) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    line_edit.setText("")
    line_edit.setCursorPosition(0)

    line_edit.mcompleter.setCompletionPrefix = MagicMock()

    line_edit.updateCompletions()

    assert line_edit.original_cursor_pos == 0
    line_edit.mcompleter.setCompletionPrefix.assert_called_once_with("")


def test_EnLineEdit_updateCompletions_cursorInMiddle(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ";"
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("first; second; third")
    line_edit.setCursorPosition(len("first; sec"))  # Cursor after 'sec' in 'second'

    line_edit.mcompleter.setCompletionPrefix = MagicMock()

    line_edit.updateCompletions()

    assert line_edit.original_cursor_pos == len("first; sec")
    line_edit.mcompleter.setCompletionPrefix.assert_called_once_with("sec")


def test_EnLineEdit_getCompletedText_singleMode(qtbot: QtBot) -> None:
    line_edit = EnLineEdit(multiple=False)
    qtbot.addWidget(line_edit)

    completed_text, after_text = line_edit.getCompletedText("new completion")
    assert completed_text == "new completion"
    assert after_text == ""


def test_EnLineEdit_getCompletedText_multipleMode_emptyLineEdit(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = "|"
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("")
    line_edit.setCursorPosition(0)

    before, after = line_edit.getCompletedText("first_entry")
    assert before == "first_entry| "
    assert after == ""


def test_EnLineEdit_getCompletedText_multipleMode_noOriginalCursorPos(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ","
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("item1, prefix, suffix")
    line_edit.setCursorPosition(len("item1, prefix"))  # Cursor after 'prefix'

    line_edit.original_cursor_pos = None  # Ensure it uses cursorPosition()

    before, after = line_edit.getCompletedText("prefix_added")
    assert before == "item1, prefix_added, "
    assert after == "suffix"
    assert line_edit.original_cursor_pos is None  # Should be reset


def test_EnLineEdit_getCompletedText_multipleMode_withOriginalCursorPos(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ";"
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("alpha; beta; gamma")
    line_edit.original_cursor_pos = len(
        "alpha; be"
    )  # Simulate cursor in the middle of 'beta'

    before, after = line_edit.getCompletedText("betamax")
    assert before == "alpha; betamax; "
    assert after == "ta; gamma"
    assert line_edit.original_cursor_pos is None  # Should be reset


def test_EnLineEdit_getCompletedText_multipleMode_cursorAtEnd(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ","
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("words, are, here, and, the")
    line_edit.setCursorPosition(len("words, are, here, and, the"))

    before, after = line_edit.getCompletedText("there")
    assert before == "words, are, here, and, there, "
    assert after == ""


def test_EnLineEdit_getCompletedText_multipleMode_cursorAtStart(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ","
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("suffix_only")
    line_edit.setCursorPosition(0)

    before, after = line_edit.getCompletedText("prefix")
    assert before == "prefix, "
    assert after == "suffix_only"


def test_EnLineEdit_completionSelected_singleMode(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=False)
    qtbot.addWidget(line_edit)

    selected_text = "Single Item"
    mock_get_completed_text = MagicMock(return_value=(selected_text, ""))
    monkeypatch.setattr(line_edit, "getCompletedText", mock_get_completed_text)

    mock_set_text = MagicMock()
    monkeypatch.setattr(line_edit, "setText", mock_set_text)
    mock_set_cursor_position = MagicMock()
    monkeypatch.setattr(line_edit, "setCursorPosition", mock_set_cursor_position)

    with qtbot.waitSignal(line_edit.item_selected, timeout=1000):
        line_edit.completionSelected(selected_text)

    mock_get_completed_text.assert_called_once_with(selected_text)
    mock_set_text.assert_called_once_with(selected_text)
    mock_set_cursor_position.assert_called_once_with(len(selected_text))


def test_EnLineEdit_completionSelected_multipleMode(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    selected_text = "new_tag"
    before_part = "existing_tag1, existing_tag2, "
    after_part = " next_word"
    mock_get_completed_text = MagicMock(
        return_value=(before_part + selected_text + ", ", after_part)
    )
    monkeypatch.setattr(line_edit, "getCompletedText", mock_get_completed_text)

    mock_set_text = MagicMock()
    monkeypatch.setattr(line_edit, "setText", mock_set_text)
    mock_set_cursor_position = MagicMock()
    monkeypatch.setattr(line_edit, "setCursorPosition", mock_set_cursor_position)

    with qtbot.waitSignal(line_edit.item_selected, timeout=1000):
        line_edit.completionSelected(selected_text)

    mock_get_completed_text.assert_called_once_with(selected_text)
    mock_set_text.assert_called_once_with(
        before_part + selected_text + ", " + after_part
    )
    mock_set_cursor_position.assert_called_once_with(
        len(before_part + selected_text + ", ")
    )


def test_EnLineEdit_completionSelected_emptySelectedText(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    selected_text = ""
    mock_get_completed_text = MagicMock(return_value=("", ""))
    monkeypatch.setattr(line_edit, "getCompletedText", mock_get_completed_text)

    mock_set_text = MagicMock()
    monkeypatch.setattr(line_edit, "setText", mock_set_text)
    mock_set_cursor_position = MagicMock()
    monkeypatch.setattr(line_edit, "setCursorPosition", mock_set_cursor_position)

    with qtbot.waitSignal(line_edit.item_selected, timeout=1000):
        line_edit.completionSelected(selected_text)

    mock_get_completed_text.assert_called_once_with(selected_text)
    mock_set_text.assert_called_once_with("")
    mock_set_cursor_position.assert_called_once_with(0)


def test_EnLineEdit_applyCurrentText_singleMode(qtbot: QtBot) -> None:
    line_edit = EnLineEdit(multiple=False)
    qtbot.addWidget(line_edit)

    # Mock completionSelected to ensure it's not called
    line_edit.completionSelected = MagicMock()

    line_edit.setText("some text")
    line_edit.applyCurrentText()

    line_edit.completionSelected.assert_not_called()


def test_EnLineEdit_applyCurrentText_multipleMode_withSeparator(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ","
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("item1, item2, new_item ")
    line_edit.setCursorPosition(len("item1, item2, new_item "))

    line_edit.completionSelected = MagicMock()

    line_edit.applyCurrentText()

    line_edit.completionSelected.assert_called_once_with("new_item")


def test_EnLineEdit_applyCurrentText_multipleMode_noSeparator(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ","
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("single_item_no_separator")
    line_edit.setCursorPosition(len("single_item_no_separator"))

    line_edit.completionSelected = MagicMock()

    line_edit.applyCurrentText()

    # sep_pos should be -1 (not found), but this is a truthy value,
    # so completionSelected should still be called.
    # If sep_pos is 0 (first character) or -1 (not found), then the conditional `if sep_pos:`
    # will evaluate to false and completionSelected won't be called.
    line_edit.completionSelected.assert_called_once_with("single_item_no_separator")


def test_EnLineEdit_applyCurrentText_multipleMode_emptyText(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = ";"
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("")
    line_edit.setCursorPosition(0)

    line_edit.completionSelected = MagicMock()

    line_edit.applyCurrentText()

    # Separator is not found, so just called with the empty string.
    line_edit.completionSelected.assert_called_once_with("")


def test_EnLineEdit_applyCurrentText_multipleMode_separatorAtStart(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit(multiple=True)
    qtbot.addWidget(line_edit)

    test_separator = "|"
    monkeypatch.setattr(prefs.settings, "split_text_entered", test_separator)

    line_edit.setText("| item")
    line_edit.setCursorPosition(len("| item"))

    line_edit.completionSelected = MagicMock()  # type: ignore[method-assign]

    line_edit.applyCurrentText()

    # The `if sep_pos:` condition is `if 0:` which is false, so it won't call `completionSelected`
    line_edit.completionSelected.assert_not_called()


def test_EnLineEdit_relayout(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    line_edit.mcompleter.popup = MagicMock()

    mock_set_focus = MagicMock()
    monkeypatch.setattr(line_edit, "setFocus", mock_set_focus)

    line_edit.relayout()

    line_edit.mcompleter.popup.assert_called_once()
    mock_set_focus.assert_called_once_with(Qt.FocusReason.OtherFocusReason)


def test_EnLineEdit_changeText_noPopup(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    line_edit.no_popup = True

    mock_update_completions = MagicMock()
    monkeypatch.setattr(line_edit, "updateCompletions", mock_update_completions)
    mock_complete = MagicMock()
    monkeypatch.setattr(line_edit, "complete", mock_complete)

    line_edit.changeText()

    mock_update_completions.assert_not_called()
    mock_complete.assert_not_called()


def test_EnLineEdit_changeText_popupEnabled_emptyPrefix(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    line_edit.no_popup = False

    mock_update_completions = MagicMock()
    monkeypatch.setattr(line_edit, "updateCompletions", mock_update_completions)

    line_edit.mcompleter = MagicMock(spec=Completer)
    line_edit.mcompleter.complete_model = MagicMock()
    line_edit.mcompleter.complete_model.current_prefix = ""  # Empty prefix
    line_edit.mcompleter.setCurrentIndex = MagicMock()

    mock_complete = MagicMock()
    monkeypatch.setattr(line_edit, "complete", mock_complete)

    line_edit.changeText()

    mock_update_completions.assert_called_once()
    line_edit.mcompleter.setCurrentIndex.assert_called_once_with(QModelIndex())
    mock_complete.assert_called_once_with(select_first=False)


def test_EnLineEdit_changeText_popupEnabled_nonEmptyPrefix(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    line_edit = EnLineEdit()
    qtbot.addWidget(line_edit)

    line_edit.no_popup = False

    mock_update_completions = MagicMock()
    monkeypatch.setattr(line_edit, "updateCompletions", mock_update_completions)

    line_edit.mcompleter = MagicMock(spec=Completer)
    line_edit.mcompleter.complete_model = MagicMock()
    line_edit.mcompleter.complete_model.current_prefix = "test"  # Non-empty prefix
    line_edit.mcompleter.setCurrentIndex = MagicMock()  # Should not be called

    mock_complete = MagicMock()
    monkeypatch.setattr(line_edit, "complete", mock_complete)

    line_edit.changeText()

    mock_update_completions.assert_called_once()
    line_edit.mcompleter.setCurrentIndex.assert_not_called()
    mock_complete.assert_called_once_with(select_first=True)
