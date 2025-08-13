"""Module that defines the widgets that are used for text completion."""

# Adapted from https://github.com/kovidgoyal/calibre/blob/master/src/calibre/gui2/complete2.py

# TODO: Don't allow multiple values that are the same

from typing import cast, override

from PySide6.QtCore import (
    QEvent,
    QModelIndex,
    QObject,
    QPoint,
    Qt,
    QTimer,
    Signal,
    SignalInstance,
    Slot,
)
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QLineEdit,
    QListView,
    QSizePolicy,
    QStyle,
    QStyleOptionComboBox,
    QWidget,
)

from music_modify.custom_types.enums import NavDirection
from music_modify.prefs import prefs
from music_modify.utils import getUniqueOrdered

from .complete_model import CompleteModel


class Completer(QListView):
    item_selected: Signal = Signal(str)
    apply_current_text: Signal = Signal()
    relayout_needed: Signal = Signal()

    def __init__(
        self,
        completer_widget: QWidget,
        max_visible_items: int = 7,
        *,
        strip_completion_entries: bool = True,
    ) -> None:
        super().__init__(completer_widget)

        self.disable_popup: bool = False
        self.setWindowFlags(Qt.WindowType.Popup)
        self.max_visible_items: int = max_visible_items
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setUniformItemSizes(True)
        self.setAlternatingRowColors(True)
        self.setModel(
            CompleteModel(self, strip_completion_entries=strip_completion_entries),
        )
        self.setMouseTracking(True)
        self.activated.connect(self.itemChosen)
        self.pressed.connect(self.itemChosen)
        self.installEventFilter(self)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tab_accepts_uncompleted_text: bool = True

    @override
    def hide(self) -> None:
        self.setCurrentIndex(QModelIndex())
        QListView.hide(self)

    def itemChosen(self, index: QModelIndex) -> None:
        if not self.isVisible():
            return
        self.hide()
        text = self.model().data(index, Qt.ItemDataRole.UserRole)
        self.item_selected.emit(str(text))

    def setItems(self, items: tuple[str, ...]) -> None:
        cast(CompleteModel, self.model()).setItems(items)
        if self.isVisible():
            self.relayout_needed.emit()

    def setCompletionPrefix(self, prefix: str) -> None:
        cast(CompleteModel, self.model()).setCompletionPrefix(prefix)
        if self.isVisible():
            self.relayout_needed.emit()

    def nextMatch(self, direction: NavDirection = NavDirection.Next) -> None:
        current = self.currentIndex()
        if current.isValid():
            row = current.row()
        else:
            row = self.model().rowCount() if direction == NavDirection.Previous else -1
        row = row + (-1 if direction == NavDirection.Previous else 1)

        index = cast(CompleteModel, self.model()).index(row % self.model().rowCount())
        self.setCurrentIndex(index)

    def scrollToItem(self, text: str | None) -> None:
        if text:
            index = cast(CompleteModel, self.model()).indexForPrefix(text)
            if index is not None and index.isValid():
                self.setCurrentIndex(index)

    def popup(self, *, select_first: bool = True) -> None:
        if self.disable_popup:
            return

        model = cast(CompleteModel, self.model())
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
        idx = self.indexAt(event.pos())
        if idx.isValid():
            current = self.currentIndex()
            if idx.row() != current.row():
                self.setCurrentIndex(idx)
        return super().mouseMoveEvent(event)

    @override
    def eventFilter(self, obj: QObject, event: QEvent, /) -> bool:
        """Redirect keypresses from the popup to the widget."""
        widget = cast(QWidget | None, self.parent())
        if widget is None:
            return False
        etype = event.type()
        if obj is not self:
            return QObject.eventFilter(self, obj, event)

        if etype == QEvent.Type.KeyPress:
            event = cast(QKeyEvent, event)
            try:
                key = event.key()
            except AttributeError:
                return QObject.eventFilter(self, obj, event)
            if key == Qt.Key.Key_Escape:
                self.hide()
                event.accept()
                return True
            if (
                key == Qt.Key.Key_F4
                and event.modifiers() & Qt.KeyboardModifier.AltModifier
            ):
                self.hide()
                event.accept()
                return True
            if key in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
                idx = self.currentIndex()
                if idx.isValid():
                    self.itemChosen(idx)
                self.hide()
                event.accept()
                return True
            if key == Qt.Key.Key_Tab:
                idx = self.currentIndex()
                if idx.isValid():
                    self.itemChosen(idx)
                    self.hide()
                elif self.tab_accepts_uncompleted_text:
                    self.hide()
                    self.apply_current_text.emit()
                elif self.model().rowCount() > 0:
                    self.nextMatch()
                event.accept()
                return True
            if key in (Qt.Key.Key_PageUp, Qt.Key.Key_PageDown):
                return False
            if key in (Qt.Key.Key_Up, Qt.Key.Key_Down):
                self.nextMatch(
                    direction=NavDirection.Previous
                    if key == Qt.Key.Key_Up
                    else NavDirection.Next,
                )
                event.accept()
                return True

            widget = cast("EditWithComplete", widget)

            widget.eat_focus_out = False
            widget.keyPressEvent(event)
            widget.eat_focus_out = True

        elif (
            etype == QEvent.Type.MouseButtonPress
            and hasattr(event, "globalPos")
            and not self.rect().contains(
                self.mapFromGlobal(cast(QMouseEvent, event).globalPos()),
            )
        ):
            event = cast(QMouseEvent, event)
            if isinstance(widget, QComboBox):
                opt = QStyleOptionComboBox()
                widget.initStyleOption(opt)
                subcontrol = widget.style().hitTestComplexControl(
                    QStyle.ComplexControl.CC_ComboBox,
                    opt,
                    widget.mapFromGlobal(event.globalPos()),
                    widget,
                )
                if subcontrol == QStyle.SubControl.SC_ComboBoxArrow:
                    QTimer.singleShot(0, self.hide)
                    event.accept()
                    return True
            self.hide()
            event.accept()
            return True
        elif etype in (QEvent.Type.InputMethod, QEvent.Type.ShortcutOverride):
            QApplication.sendEvent(widget, event)

        return False


class LineEdit(QLineEdit):
    item_selected: Signal = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
        completer_widget: QWidget | None = None,
        *,
        strip_completion_entries: bool = True,
        multiple: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setClearButtonEnabled(True)

        self.original_cursor_pos: int | None = None
        completer_widget = self if completer_widget is None else completer_widget

        self.mcompleter: Completer = Completer(
            completer_widget,
            strip_completion_entries=strip_completion_entries,
        )
        self.mcompleter.item_selected.connect(
            self.completionSelected,
            type=Qt.ConnectionType.QueuedConnection,
        )
        self.mcompleter.apply_current_text.connect(
            self.applyCurrentText,
            type=Qt.ConnectionType.QueuedConnection,
        )
        self.mcompleter.relayout_needed.connect(self.relayout)
        self.mcompleter.setFocusProxy(completer_widget)
        self.textEdited.connect(self.changeText)
        self.no_popup: bool = False

        self.multiple: bool = multiple
        self.add_separator: bool = True

    @property
    def all_items(self) -> tuple[str, ...]:
        return cast(CompleteModel, self.mcompleter.model()).all_items

    @all_items.setter
    def all_items(self, items: tuple[str, ...]) -> None:
        cast(CompleteModel, self.mcompleter.model()).setItems(items)

    @property
    def disable_popup(self) -> bool:
        return self.mcompleter.disable_popup

    @disable_popup.setter
    def disable_popup(self, val: bool) -> None:
        self.mcompleter.disable_popup = bool(val)

    def setElideMode(self, val: Qt.TextElideMode) -> None:
        self.mcompleter.setTextElideMode(val)

    def updateItemsCache(self, items: tuple[str, ...]) -> None:
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

    def complete(
        self,
        *,
        show_all: bool = False,
        select_first: bool = True,
    ) -> None:
        orig: str | None = None
        if show_all:
            orig = cast(CompleteModel, self.mcompleter.model()).current_prefix
            self.mcompleter.setCompletionPrefix("")
        if not cast(CompleteModel, self.mcompleter.model()).current_items:
            self.mcompleter.hide()
            return
        self.mcompleter.popup(select_first=select_first)
        self.setFocus(Qt.FocusReason.OtherFocusReason)
        self.mcompleter.scrollToItem(orig)

    def updateCompletions(self) -> None:
        self.original_cursor_pos = cpos = self.cursorPosition()
        text = str(self.text())
        prefix = text[:cpos]
        complete_prefix = prefix.lstrip()
        if self.multiple:
            sep = prefs.settings.split_text_entered
            complete_prefix = prefix.split(sep)[-1].lstrip()
        self.mcompleter.setCompletionPrefix(complete_prefix)

    def getCompletedText(self, text: str) -> tuple[str, str]:
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
        if before_text:
            before_text += sep + " "
        if self.add_separator or after_text:
            completed_text = text + sep + " "
        else:
            completed_text = text
        return before_text + completed_text, after_text

    @Slot(str)
    def completionSelected(self, text: str) -> None:
        before_text, after_text = self.getCompletedText(str(text))
        self.setText(before_text + after_text)
        self.setCursorPosition(len(before_text))
        self.item_selected.emit(text)

    @Slot()
    def applyCurrentText(self) -> None:
        if self.multiple:
            sep = prefs.settings.split_text_entered
            txt = str(self.text())
            sep_pos = txt.rfind(sep)
            if sep_pos:
                ntxt = txt[sep_pos + 1 :].strip()
                self.completionSelected(ntxt)

    @Slot()
    def relayout(self) -> None:
        self.mcompleter.popup()
        self.setFocus(Qt.FocusReason.OtherFocusReason)

    @Slot()
    def changeText(self) -> None:
        if self.no_popup:
            return
        self.updateCompletions()
        select_first = (
            len(cast(CompleteModel, self.mcompleter.model()).current_prefix) > 0
        )
        if not select_first:
            self.mcompleter.setCurrentIndex(QModelIndex())
        self.complete(select_first=select_first)


class EnComboBox(QComboBox):
    """Enhanced QComboBox.

    Limits added text to those not already in the line edit."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setLineEdit(QLineEdit(self))
        completer = self.completer()
        if completer is not None:
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setMinimumContentsLength(20)

    def text(self) -> str:
        return str(self.currentText())

    def setText(self, text: str) -> None:
        # noinspection PyTypeChecker
        idx: int = self.findText(
            text,
            Qt.MatchFlag.MatchCaseSensitive | Qt.MatchFlag.MatchFixedString,
        )
        if idx == -1:
            self.insertItem(0, text)
            idx = 0
        self.setCurrentIndex(idx)


class EditWithComplete(EnComboBox):
    item_selected: Signal = Signal(str)

    def __init__(self, parent: QWidget, *, multiple: bool = True) -> None:
        super().__init__(parent)

        self.setLineEdit(LineEdit(self, completer_widget=self, multiple=multiple))
        cast(LineEdit, self.lineEdit()).item_selected.connect(self.item_selected)
        # noinspection PyTypeChecker
        self.setCompleter(None)  # pyright: ignore[reportArgumentType]
        self.eat_focus_out: bool = True
        self.installEventFilter(self)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

    @override
    def showPopup(self) -> None:
        orig = self.disable_popup
        self.disable_popup = False
        try:
            cast(LineEdit, self.lineEdit()).complete(show_all=True)
        finally:
            self.disable_popup = orig

    def updateItemsCache(self, items: tuple[str, ...]) -> None:
        cast(LineEdit, self.lineEdit()).updateItemsCache(items)

    def showInitialValue(self, value: str) -> None:
        value = str(value) if value else ""
        self.setText(value)
        self.selectAll()

    @property
    def all_items(self) -> tuple[str, ...]:
        return cast(LineEdit, self.lineEdit()).all_items

    @all_items.setter
    def all_items(self, items: tuple[str, ...]) -> None:
        cast(LineEdit, self.lineEdit()).all_items = items

    @property
    def disable_popup(self) -> bool:
        return cast(LineEdit, self.lineEdit()).disable_popup

    @disable_popup.setter
    def disable_popup(self, val: bool) -> None:
        cast(LineEdit, self.lineEdit()).disable_popup = bool(val)

    def setElideMode(self, val: Qt.TextElideMode) -> None:
        cast(LineEdit, self.lineEdit()).setElideMode(val)

    @override
    def text(self) -> str:
        return cast(LineEdit, self.lineEdit()).text()

    @override
    def setCurrentText(self, text: str) -> None:
        self.setText(text)
        self.selectAll()

    def selectAll(self) -> None:
        cast(LineEdit, self.lineEdit()).selectAll()

    @override
    def setText(self, text: str) -> None:
        edit = cast(LineEdit, self.lineEdit())
        edit.no_popup = True
        edit.setText(text)
        edit.no_popup = False

    def home(self, *, mark: bool = False) -> None:
        cast(LineEdit, self.lineEdit()).home(mark)

    def setCursorPosition(self, v: int) -> None:
        cast(LineEdit, self.lineEdit()).setCursorPosition(v)

    @property
    def textChanged(self) -> SignalInstance:
        return cast(LineEdit, self.lineEdit()).textChanged

    @override
    def clear(self) -> None:
        cast(LineEdit, self.lineEdit()).clear()
        super().clear()

    @override
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        try:
            completer = cast(LineEdit, self.lineEdit()).mcompleter
        except AttributeError:
            return False
        etype = event.type()
        if self.eat_focus_out and self is obj and etype == QEvent.Type.FocusOut:
            if completer.isVisible():
                return True
        return super().eventFilter(obj, event)

    @property
    def values(self) -> list[str]:
        text = self.text()
        return getUniqueOrdered(text, prefs.settings.split_text_entered)

    @values.setter
    def values(self, values: list[str]) -> None:
        self.updateItemsCache(tuple(values))


def testWidgets() -> int:
    from PySide6.QtWidgets import QDialog, QVBoxLayout

    d = QDialog()
    d.setLayout(QVBoxLayout())
    edit = EditWithComplete(d)
    layout = d.layout()
    if layout is not None:
        layout.addWidget(edit)
    items = [
        "oane\n line2\n line3",
        "otwo",
        "othree",
        "ooone",
        "ootwo",
        "other",
        "odd",
        "over",
        "orc",
        "oven",
        "owe",
        "oothree",
        "a1",
        "a2",
        "Edgas",
        "Èdgar",
        "Édgaq",
        "Edgar",
        "Édgar",
    ]
    edit.updateItemsCache(tuple(items))
    edit.showInitialValue("")
    return d.exec()
