"""Module that defines an abstract class, that is used to
define the general behaviour of a widget inside an EditDialog.
"""

from abc import ABC, abstractmethod
import copy
import logging
from typing import Generic, TypeVar

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QHBoxLayout, QToolButton, QWidget

from music_modify.custom_types.aliases import SongEditData
from music_modify.custom_types.enums import EditButton
from music_modify.gui.meta import ABCQMeta

logger = logging.getLogger(__name__)

ValueT = TypeVar("ValueT", bound=SongEditData)


class EditAbstractWidget(QWidget, Generic[ValueT], ABC, metaclass=ABCQMeta):
    """An abstract class that defines the desired behaviour for a widget
    inside an EditDialog.
    """

    value_updated: Signal = Signal()
    "Signal that indicates that a value has changed to a new value."
    value_reset: Signal = Signal()
    """Signal that indicates that  a value has been set back to the value
    it had when the widget was initialised."""

    def __init__(self, parent: QWidget, data: ValueT | None = None) -> None:
        super().__init__(parent)
        self._initValue(data)
        self._setMainLayout()
        self._setupUi()

    @abstractmethod
    def _initValue(self, data: ValueT | None) -> None:
        """Sets the original value that the widget should store."""
        pass

    @abstractmethod
    def _setupUi(self) -> None:
        """Sets up the display of the widget."""
        pass

    @abstractmethod
    def _displayValue(self) -> None:
        """Sets the values for the table based on the current value property."""
        pass

    @abstractmethod
    def _updateValue(self) -> None:
        """Updates the value that is stored in the widget, and displayed."""
        logger.info("Abstract updateValue called")
        pass

    @abstractmethod
    def _clearValue(self) -> None:
        """Sets the value to the equivalent empty value."""
        pass

    @abstractmethod
    def _isReset(self) -> bool:
        """Returns whether the value has been set back to its original state."""
        pass

    @property
    @abstractmethod
    def value(self) -> ValueT:
        """The value displayed and stored inside the widget,
        depending on the data type.
        """
        pass

    @value.setter
    def value(self, value: ValueT) -> None:
        self.value = value

    @property
    @abstractmethod
    def original(self) -> ValueT:
        """The original value that was stored inside the widget, before changes."""
        pass

    def clear(self) -> None:
        """Clears the value stored and displayed in the widget."""
        self._clearValue()
        self._displayValue()
        self._emitUpdate()

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
        """Creates a layout with the designated button types
        in the desired orientation.

        Args:
            buttons: The set of button types that should be displayed
            direction: Whether the buttons should be arranged vertically or horizontally
        """
        button_layout = QBoxLayout(direction)

        if buttons & EditButton.Clear:
            clear_button = QToolButton(self)
            clear_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear)))
            button_layout.addWidget(clear_button)
            clear_button.clicked.connect(self.clear)

        if buttons & EditButton.Reset:
            reset_button = QToolButton(self)
            reset_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentRevert)))
            button_layout.addWidget(reset_button)
            reset_button.clicked.connect(self.reset)

        return button_layout

    def _setMainLayout(self) -> None:
        """Creates the basic layout for the widget."""
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

    def _emitUpdate(self) -> None:
        """Emit a signal indicating whether the data has changed, or been reset."""
        if self._isReset():
            self.value_reset.emit()
        else:
            self.value_updated.emit()
