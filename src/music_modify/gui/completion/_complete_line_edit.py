# pyright: reportImportCycles=false

"""Module for an enhanced QLineEdit."""

# Adapted from https://github.com/kovidgoyal/calibre/blob/master/src/calibre/gui2/complete2.py

from typing import cast, override

from PySide6.QtCore import QEvent, QModelIndex, Qt, Signal, Slot
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit, QWidget

from music_modify.prefs import prefs

from ._completer import Completer


class EnLineEdit(QLineEdit):
    """A line edit that completes on multiple items separated by a separator.

    Use `updateItemsCache` to set the list of all possible completions.
    """

    item_selected: Signal = Signal(str)
    "Signal that is emitted when an item is chosen from the completion list."

    def __init__(
        self,
        parent: QWidget | None = None,
        completer_widget: QWidget | None = None,
        *,
        strip_completion_entries: bool = True,
        multiple: bool = True,
    ) -> None:
        """Create a line edit that has a popup for completion suggestions.

        Args:
            parent: The widget that this widget should be displayed on.
            completer_widget: The widget that completion items should be displayed on.
                If not set, defaults to this widget itself.
            strip_completion_entries: Whether whitespace should be kept in entries.
            multiple: Whether multiple items can be displayed and selected,
                or only single items.
        """
        super().__init__(parent)
        self.setClearButtonEnabled(True)

        self.original_cursor_pos: int | None = None
        completer_widget = self if completer_widget is None else completer_widget
        "The widget that completion items should be displayed on."

        self.mcompleter: Completer = Completer(
            completer_widget, strip_completion_entries=strip_completion_entries
        )
        "List view that contains the completion items."

        self.mcompleter.item_selected.connect(
            self.completionSelected, type=Qt.ConnectionType.QueuedConnection
        )
        self.mcompleter.apply_current_text.connect(
            self.applyCurrentText,
            type=Qt.ConnectionType.QueuedConnection,
        )
        self.mcompleter.relayout_needed.connect(self.relayout)
        self.mcompleter.setFocusProxy(completer_widget)
        self.textEdited.connect(self.changeText)

        self.no_popup: bool = False
        "Whether a popup should be displayed for the line edit or not"
        self.multiple: bool = multiple
        "Whether multiple items can be displayed and selected, or only single items"

    @property
    def all_items(self) -> tuple[str, ...]:
        """All possible values that can be used for completion."""
        return self.mcompleter.complete_model.all_items

    @all_items.setter
    def all_items(self, items: tuple[str, ...]) -> None:
        self.mcompleter.complete_model.setItems(items)

    @property
    def disable_popup(self) -> bool:
        """Whether the popup should be displayed or not."""
        return self.mcompleter.disable_popup

    @disable_popup.setter
    def disable_popup(self, val: bool) -> None:
        self.mcompleter.disable_popup = bool(val)

    def setElideMode(self, val: Qt.TextElideMode) -> None:
        """Sets the elide mode for the completion widget."""
        self.mcompleter.setTextElideMode(val)

    def updateItemsCache(self, items: tuple[str, ...]) -> None:
        """Set the possible completion items."""
        self.all_items = items

    @override
    def event(self, event: QEvent) -> bool:
        try:
            if event.type() == QEvent.Type.ShortcutOverride and (
                cast(QKeyEvent, event).key() in (Qt.Key.Key_Left, Qt.Key.Key_Right)
                and (
                    (
                        cast(QKeyEvent, event).modifiers()
                        & ~Qt.KeyboardModifier.KeypadModifier
                    )
                    == Qt.KeyboardModifier.ControlModifier
                )
            ):
                event.accept()
        except AttributeError:
            pass
        return super().event(event)

    def complete(self, *, show_all: bool = False, select_first: bool = True) -> None:
        """Show the completion items."""
        orig_text: str | None = None
        if show_all:
            orig_text = self.mcompleter.complete_model.current_prefix
            self.mcompleter.setCompletionPrefix("")
        if not self.mcompleter.complete_model.current_items:
            self.mcompleter.hide()
            return
        self.mcompleter.popup(select_first=select_first)
        self.setFocus(Qt.FocusReason.OtherFocusReason)
        self.mcompleter.scrollToItem(orig_text)

    def updateCompletions(self) -> None:
        """Update the list of completion items.

        Uses the cursor position to find what the prefix should be,
        and generates the completions based on that.
        """
        self.original_cursor_pos = cpos = self.cursorPosition()
        text = str(self.text())
        prefix = text[:cpos]
        complete_prefix = prefix.lstrip()
        if self.multiple:
            sep = prefs.settings.split_text_entered
            complete_prefix = prefix.split(sep)[-1].lstrip()
        self.mcompleter.setCompletionPrefix(complete_prefix)

    def getCompletedText(self, text: str) -> tuple[str, str]:
        """Get the list of completed items in before and after parts."""
        if not self.multiple:
            return text, ""
        sep = prefs.settings.split_text_entered
        cursor_pos = self.original_cursor_pos
        if cursor_pos is None:
            cursor_pos = self.cursorPosition()
        self.original_cursor_pos = None

        curtext = str(self.text())
        before_text = curtext[:cursor_pos]
        after_text = curtext[cursor_pos:].rstrip()

        # Remove the completion prefix from the before text
        before_text = sep.join(before_text.split(sep)[:-1]).rstrip()

        # Remove the separator and space from after, if it exists
        if after_text.startswith(sep + " "):
            after_text = after_text[len(sep) + 1 :]
        if before_text:
            before_text += sep + " "
        completed_text = text + sep + " "
        return before_text + completed_text, after_text

    @Slot(str)
    def completionSelected(self, text: str) -> None:
        """Operate on a selected completion item."""
        before_text, after_text = self.getCompletedText(str(text))
        self.setText(before_text + after_text)
        self.setCursorPosition(len(before_text))
        self.item_selected.emit(text)

    @Slot()
    def applyCurrentText(self) -> None:
        """Use the current text as a selection."""
        if self.multiple:
            sep = prefs.settings.split_text_entered
            text = str(self.text())
            sep_pos = text.rfind(sep)
            if sep_pos:
                new_text = text[sep_pos + 1 :].strip()
                self.completionSelected(new_text)

    @Slot()
    def relayout(self) -> None:
        """Re-display the widget with completion."""
        self.mcompleter.popup()
        self.setFocus(Qt.FocusReason.OtherFocusReason)

    @Slot()
    def changeText(self) -> None:
        """Change the displayed text and completion items."""
        if self.no_popup:
            return
        self.updateCompletions()
        select_first = len(self.mcompleter.complete_model.current_prefix) > 0
        if not select_first:
            self.mcompleter.setCurrentIndex(QModelIndex())
        self.complete(select_first=select_first)
