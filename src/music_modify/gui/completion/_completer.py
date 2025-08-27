"""Module that defines the list widget that is used for displaying completion items.

This widget should be used as a replacement for a QCompleter.
"""

# Adapted from https://github.com/kovidgoyal/calibre/blob/master/src/calibre/gui2/complete2.py

from typing import TYPE_CHECKING, cast, override

from PySide6.QtCore import QEvent, QModelIndex, QObject, QPoint, Qt, QTimer, Signal
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QListView,
    QStyle,
    QStyleOptionComboBox,
    QWidget,
)

from music_modify.custom_types.enums import NavDirection

from ._complete_model import CompleteModel

if TYPE_CHECKING:
    from .edit_with_complete import EditWithComplete


class Completer(QListView):
    """Widget that is used for displaying completion suggestions."""

    item_selected: Signal = Signal(str)
    "Signal that is emitted when any item is actually selected."
    apply_current_text: Signal = Signal()
    """Signal that is emitted when the current text displayed should be used,
    and added to the items."""
    relayout_needed: Signal = Signal()
    "Signal that is emitted when the widgets need to be re-laid out."

    def __init__(
        self,
        completer_widget: QWidget,
        max_visible_items: int = 7,
        *,
        strip_completion_entries: bool = True,
    ) -> None:
        """Creates a Completer list widget for displaying completion suggestions."""
        super().__init__(completer_widget)
        self.disable_popup: bool = False
        "Whether to use a popup for this widget or not."
        self.setWindowFlags(Qt.WindowType.Popup)
        self.max_visible_items: int = max_visible_items
        "The maximum number of items that the popup should display."
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setUniformItemSizes(True)
        self.setAlternatingRowColors(True)
        self.complete_model = CompleteModel(
            self, strip_completion_entries=strip_completion_entries
        )
        self.setModel(self.complete_model)
        self.setMouseTracking(True)
        self.activated.connect(self.chooseItem)
        self.pressed.connect(self.chooseItem)
        self.installEventFilter(self)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tab_accepts_uncompleted_text: bool = True
        "Whether tab fills in the suggested text, or just enters a tab."

    @override
    def hide(self) -> None:
        self.setCurrentIndex(QModelIndex())
        QListView.hide(self)

    def chooseItem(self, index: QModelIndex) -> None:
        """Selects the item at this specific index."""
        if not self.isVisible():
            return
        self.hide()
        text = self.model().data(index, Qt.ItemDataRole.UserRole)
        self.item_selected.emit(str(text))

    def setItems(self, items: tuple[str, ...]) -> None:
        """Set the completion items for the model, and re-layout if needed."""
        self.complete_model.setItems(items)
        if self.isVisible():
            self.relayout_needed.emit()

    def setCompletionPrefix(self, prefix: str) -> None:
        """Sets the prefix for the model."""
        self.complete_model.setCompletionPrefix(prefix)
        if self.isVisible():
            self.relayout_needed.emit()

    def nextMatch(self, direction: NavDirection = NavDirection.Next) -> None:
        """Go to the next (or previous) item in the model."""
        current_index = self.currentIndex()
        if current_index.isValid():
            row = current_index.row()
        else:
            row = self.model().rowCount() if direction == NavDirection.Previous else -1
        row = row + (-1 if direction == NavDirection.Previous else 1)
        index = self.complete_model.index(row % self.model().rowCount())
        self.setCurrentIndex(index)

    def scrollToItem(self, text: str | None) -> None:
        """Goes to the first item in the model that matches the text sent."""
        if text:
            index = self.complete_model.indexForPrefix(text)
            if index is not None and index.isValid():
                self.setCurrentIndex(index)

    def popup(self, *, select_first: bool = True) -> None:
        """Creates and displays the popup for this widget."""
        if self.disable_popup:
            return

        model = self.complete_model
        widget = cast(QWidget | None, self.parent())
        if widget is None:
            return

        screen = widget.screen().availableGeometry()
        height = (
            self.sizeHintForRow(0) * min(self.max_visible_items, model.rowCount()) + 3
        ) + 3
        horizontal_scroll = self.horizontalScrollBar()
        if horizontal_scroll and horizontal_scroll.isVisible():
            height += horizontal_scroll.sizeHint().height()

        real_height = widget.height()
        pos = widget.mapToGlobal(QPoint(0, widget.height() - 2))
        width = min(widget.width(), screen.width())

        if (pos.x() + width) > (screen.x() + screen.width()):
            pos.setX(screen.x() + screen.width() - width)
        if pos.x() < screen.x():
            pos.setX(screen.x())

        top = pos.y() - real_height - screen.top() + 2
        bottom = screen.bottom() - pos.y()
        height = max(height, self.minimumHeight())
        if height > bottom:
            height = min(max(top, bottom), height)

            if top > bottom:
                pos.setY(pos.y() - height - real_height + 2)

        self.setGeometry(pos.x(), pos.y(), width, height)

        if (
            select_first
            and not self.currentIndex().isValid()
            and self.model().rowCount() > 0
        ):
            self.setCurrentIndex(model.index(0))

        if not self.isVisible():
            self.show()

    @override
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Select the item if it is displayed and valid.

        Otherwise just forward the movement.
        """
        idx = self.indexAt(event.position().toPoint())
        if idx.isValid():
            current = self.currentIndex()
            if idx.row() != current.row():
                self.setCurrentIndex(idx)
        return super().mouseMoveEvent(event)

    def _processKeyPress(  # noqa: C901, PLR0912
        self, watched: QObject, event: QKeyEvent, widget: QWidget
    ) -> bool:
        """Process an event where a keyboard button is typed."""
        try:
            key = event.key()
        except AttributeError:
            return QObject.eventFilter(self, watched, event)
        processed = False
        if key == Qt.Key.Key_Escape:
            self.hide()
            event.accept()
            processed = True
        if key == Qt.Key.Key_F4 and event.modifiers() & Qt.KeyboardModifier.AltModifier:
            self.hide()
            event.accept()
            processed = True
        if key in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            idx = self.currentIndex()
            if idx.isValid():
                self.chooseItem(idx)
            self.hide()
            event.accept()
            processed = True
        if key == Qt.Key.Key_Tab:
            idx = self.currentIndex()
            if idx.isValid():
                self.chooseItem(idx)
                self.hide()
            elif self.tab_accepts_uncompleted_text:
                self.hide()
                self.apply_current_text.emit()
            elif self.model().rowCount() > 0:
                self.nextMatch()
            event.accept()
            processed = True
        if key in (Qt.Key.Key_PageUp, Qt.Key.Key_PageDown):
            # Let the list view handle these keys
            return False
        if key in (Qt.Key.Key_Up, Qt.Key.Key_Down):
            self.nextMatch(
                direction=NavDirection.Previous
                if key == Qt.Key.Key_Up
                else NavDirection.Next
            )
            event.accept()
            processed = True

        if processed:
            return True

        # Send to widget
        if hasattr(widget, "eat_focus_out"):
            widget = cast("EditWithComplete", widget)
            widget.eat_focus_out = False
            widget.keyPressEvent(event)
            widget.eat_focus_out = True
            if not widget.hasFocus():
                # Widget lost focus, so hide popup
                self.hide()
            if event.isAccepted():
                return True

        return False

    def _processMouseEvent(self, event: QMouseEvent, widget: QWidget) -> bool:
        if isinstance(widget, QComboBox):
            # Ensure clicking the dropdown arrow of the combobox closes the popup
            opt = QStyleOptionComboBox()
            widget.initStyleOption(opt)
            subcontrol = widget.style().hitTestComplexControl(
                QStyle.ComplexControl.CC_ComboBox,
                opt,
                widget.mapFromGlobal(event.globalPosition().toPoint()),
                widget,
            )
            if subcontrol == QStyle.SubControl.SC_ComboBoxArrow:
                QTimer.singleShot(0, self.hide)
                event.accept()
                return True
        self.hide()
        event.accept()
        return True

    @override
    def eventFilter(self, watched: QObject, event: QEvent, /) -> bool:
        widget = cast(QWidget | None, self.parent())
        if widget is None:
            return False
        etype = event.type()
        if watched is not self:
            return QObject.eventFilter(self, watched, event)
        if etype == QEvent.Type.KeyPress:
            event = cast(QKeyEvent, event)
            return self._processKeyPress(watched, event, widget)
        if (
            etype == QEvent.Type.MouseButtonPress
            and hasattr(event, "globalPosition")
            and not self.rect().contains(
                self.mapFromGlobal(cast(QMouseEvent, event).globalPosition().toPoint())
            )
        ):
            # A click outside the popup, close it.
            event = cast(QMouseEvent, event)
            return self._processMouseEvent(event, widget)
        if etype in (QEvent.Type.InputMethod, QEvent.Type.ShortcutOverride):
            QApplication.sendEvent(widget, event)

        return False
