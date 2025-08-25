"""Module that defines a widget used for input with completion suggestions."""

# Adapted from https://github.com/kovidgoyal/calibre/blob/master/src/calibre/gui2/complete2.py

from typing import override

from PySide6.QtCore import QEvent, QObject, Qt, Signal, SignalInstance
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QComboBox, QSizePolicy, QWidget

from music_modify.prefs import prefs
from music_modify.utils.list_utils import getUniqueOrdered

from ._complete_line_edit import EnLineEdit

# TODO: Don't allow multiple values that are the same


class EditWithComplete(QComboBox):
    """A QLineEdit-like widget that offers completion suggestions."""

    item_selected: Signal = Signal(str)
    "Signal that is emitted when an item in the completion list is chosen."

    def __init__(
        self,
        parent: QWidget,
        items: tuple[str, ...] | None = None,
        *,
        multiple: bool = True,
        initial: str = "",
    ) -> None:
        """Creates a widget for entering text with completion suggestions.

        Args:
            parent: The widget that this widget should be displayed on.
            items: The completion suggestions for the widget on initialization.
            multiple: Whether multiple values should be allowed as output.
            initial: The initial value to display in the widget.
        """
        super().__init__(parent)
        self.setMinimumContentsLength(20)

        self.line_edit: EnLineEdit = EnLineEdit(
            self, completer_widget=self, multiple=multiple
        )
        self.setLineEdit(self.line_edit)
        self.line_edit.item_selected.connect(self.item_selected)
        # noinspection PyTypeChecker
        self.setCompleter(None)  # pyright: ignore[reportArgumentType]
        self.eat_focus_out: bool = True
        "Whether this widget should consume a focus event or not."
        self.installEventFilter(self)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        if items:
            self.updateItemsCache(items)
        self.showInitialValue(initial)

    @override
    def showPopup(self) -> None:
        orig = self.disable_popup
        self.disable_popup = False
        try:
            self.line_edit.complete(show_all=True)
        finally:
            self.disable_popup = orig

    @override
    def keyPressEvent(self, event: QKeyEvent, /) -> None:
        if (
            event.key() in (Qt.Key.Key_Down, Qt.Key.Key_Up)
            and not self.line_edit.text()
            and not self.disable_popup
        ):
            event.accept()
            self.showPopup()
            return
        super().keyPressEvent(event)

    def updateItemsCache(self, items: tuple[str, ...]) -> None:
        """Update the completion item suggestions."""
        self.line_edit.updateItemsCache(items)

    def showInitialValue(self, value: str) -> None:
        """Set the text for the line edit to the value sent."""
        value = str(value) if value else ""
        self.setText(value)
        self.selectAll()

    @property
    def all_items(self) -> tuple[str, ...]:
        """The possible values that a user can enter for completion."""
        return self.line_edit.all_items

    @all_items.setter
    def all_items(self, items: tuple[str, ...]) -> None:
        self.line_edit.all_items = items

    @property
    def disable_popup(self) -> bool:
        """Whether the popup should be displayed or not."""
        return self.line_edit.disable_popup

    @disable_popup.setter
    def disable_popup(self, val: bool) -> None:
        self.line_edit.disable_popup = bool(val)

    def setElideMode(self, val: Qt.TextElideMode) -> None:
        """The mode used for eliding text when there is too much."""
        self.line_edit.setElideMode(val)

    def text(self) -> str:
        """The text being displayed for the current item in the combo box."""
        return self.line_edit.text()

    @override
    def setCurrentText(self, text: str, /) -> None:
        self.setText(text)
        self.selectAll()

    def selectAll(self) -> None:
        """Selects all the text in the line edit, and moves the cursor to the end."""
        self.line_edit.selectAll()

    def setText(self, text: str) -> None:
        """Sets the text that should be displayed in the line edit."""
        self.line_edit.no_popup = True
        self.line_edit.setText(text)
        self.line_edit.no_popup = False

    def home(self, *, mark: bool = False) -> None:
        """Moves the text cursor to the beginning of the line.

        If `mark` is True, text is selected towards the first position.
        Otherwise, any selected text is unselected if the cursor is moved.
        """
        self.line_edit.home(mark)

    def setCursorPosition(self, pos: int) -> None:
        """Set the cursor position for the line edit.

        This causes a repaint when appropriate.
        """
        self.line_edit.setCursorPosition(pos)

    @property
    def textChanged(self) -> SignalInstance:
        """Signal that is emitted when the text in the line edit changes."""
        return self.line_edit.textChanged

    @override
    def clear(self) -> None:
        self.line_edit.clear()
        super().clear()

    @override
    def eventFilter(self, watched: QObject, event: QEvent, /) -> bool:
        try:
            completer = self.line_edit.mcompleter
        except AttributeError:
            return False
        if (
            self.eat_focus_out
            and self is watched
            and event.type() == QEvent.Type.FocusOut
            and completer.isVisible()
        ):
            return True
        return super().eventFilter(watched, event)

    @property
    def values(self) -> list[str]:
        """The split items that are currently displayed in the line edit.

        The text is split by the setting value for `split_text_entered`.
        """
        text = self.text()
        return getUniqueOrdered(text, prefs.settings.split_text_entered)
