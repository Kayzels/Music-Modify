"""Module that defines an EditAbstractWidget.

This is an abstract class, that is used to define the general behaviour of a widget
inside an EditDialog.
"""

from abc import ABC, abstractmethod
import copy
import logging
from typing import final

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QHBoxLayout, QToolButton, QWidget

from music_modify.core.meta import ABCQMeta
from music_modify.custom_types.aliases import SongEditData
from music_modify.custom_types.enums import EditButton

logger = logging.getLogger(__name__)


class EditAbstractWidget[ValueT: SongEditData, WidgetT: QWidget](
    QWidget, ABC, metaclass=ABCQMeta
):
    """Defines the required functionality for a widget inside an EditDialog."""

    value_updated: Signal = Signal()
    "Signal that indicates that a value has changed to a new value."
    value_reset: Signal = Signal()
    """Signal that indicates that  a value has been set back to the value
    it had when the widget was initialised."""

    def __init__(self, parent: QWidget, data: ValueT | None = None) -> None:
        """Creates an EditAbstractWidget.

        Args:
            parent: The widget that this widget should be displayed on.
            data: The data to be displayed.
        """
        super().__init__(parent)
        self.clear_button: QToolButton | None = None
        "Button that clears the value being displayed and stored in the widget."
        self.reset_button: QToolButton | None = None
        "Button that restores the value to what it was at initialization."
        self.main_layout: QHBoxLayout
        "The layout that the main widget should be placed on."
        self.main_widget: WidgetT
        "Main widget used to display the values currently stored."
        self._original_data: ValueT
        self._initValue(data)
        self._setupCommonUi()

    @final
    def _initValue(self, data: ValueT | None, /) -> None:
        """Sets the original value that the widget should store."""
        if data is None:
            self.value = self.empty
        else:
            self.value = data

        self._original_data = copy.deepcopy(self.value)

    @abstractmethod
    def _setupUi(self) -> None:
        """Sets up the display of the widget.

        When this is called, it assumes that the `main_widget` and `main_layout`
        instance variables have been set.

        This function _should_ add the `main_widget` to `main_layout` or a child
        layout of `main_layout`. Any other UI initialization should be done here.
        """

    @abstractmethod
    def _displayValue(self) -> None:
        """Sets the values for the table based on the current value property."""

    @abstractmethod
    def _updateValue(self) -> None:
        """Updates the value that is stored in the widget, and displayed."""

    @abstractmethod
    def _isReset(self) -> bool:
        """Returns whether the value has been set back to its original state."""

    @abstractmethod
    def _setMainWidget(self) -> WidgetT:
        """Set the widget that should be used for the main widget.

        This function _must_ set the `main_widget` instance variable.

        It also should not call other private methods like `_displayValue`.
        It is better for that function to be called in `_setupUi`.
        """

    @property
    @final
    def value(self) -> ValueT:
        """The value displayed and stored inside the widget, based on the data type."""
        return self._value

    @value.setter
    @final
    def value(self, value: ValueT) -> None:
        """The value displayed and stored inside the widget, based on the data type."""
        self._value: ValueT = value

    @property
    @final
    def original(self) -> ValueT:
        """The original value that was stored inside the widget, before changes."""
        return self._original_data

    @property
    @abstractmethod
    def empty(self) -> ValueT:
        """The empty value for the data type, for example, the empty list or string."""

    @final
    def clear(self) -> None:
        """Clears the value stored and displayed in the widget."""
        self.value = self.empty
        self._displayValue()
        self._emitUpdate()

    @final
    def reset(self) -> None:
        """Reset to the originally stored value, before any changes were made."""
        if not self._isReset():
            self.value = copy.deepcopy(self.original)
            self._displayValue()
            self._emitUpdate()

    # noinspection PyTypeChecker
    def createButtons(
        self,
        buttons: EditButton = EditButton.Reset | EditButton.Clear,
        direction: QBoxLayout.Direction = QBoxLayout.Direction.LeftToRight,
    ) -> QBoxLayout:
        """Creates a layout with the designated button types in the desired orientation.

        Args:
            buttons: The set of button types that should be displayed
            direction: Whether the buttons should be arranged vertically or horizontally
        """
        button_layout = QBoxLayout(direction)

        if buttons & EditButton.Clear:
            self.clear_button = QToolButton(self)
            self.clear_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear)))
            button_layout.addWidget(self.clear_button)
            self.clear_button.clicked.connect(self.clear)

        if buttons & EditButton.Reset:
            self.reset_button = QToolButton(self)
            self.reset_button.setIcon(
                QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentRevert))
            )
            button_layout.addWidget(self.reset_button)
            self.reset_button.clicked.connect(self.reset)

        return button_layout

    @final
    def _setMainLayout(self) -> QHBoxLayout:
        """Creates the basic layout for the widget."""
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout

    @final
    def _emitUpdate(self) -> None:
        """Emit a signal indicating whether the data has changed, or been reset."""
        if self._isReset():
            self.value_reset.emit()
        else:
            self.value_updated.emit()

    @final
    def _setupCommonUi(self) -> None:
        """Ensures the layout and widget are created in the correct order.

        This is done so that methods can be assured that the attributes exist
        when they are run, but the attributes can be defined in child classes.
        """
        self.main_layout = self._setMainLayout()
        self.main_widget = self._setMainWidget()
        self._setupUi()
