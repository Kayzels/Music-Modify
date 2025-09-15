"""Module that defines an EditAbstractWidget.

This is an abstract class, that is used to define the general behaviour of a widget
inside an EditDialog.
"""

from abc import ABC, abstractmethod
import logging
from typing import final

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QHBoxLayout, QToolButton, QWidget

from music_modify.core.meta import ABCQMeta
from music_modify.custom_types.enums import EditButton
from music_modify.custom_types.tag_value import AbstractTagValue

logger = logging.getLogger(__name__)


class EditAbstractWidget(QWidget, ABC, metaclass=ABCQMeta):
    """Defines the required functionality for a widget inside an EditDialog."""

    value_updated: Signal = Signal()
    "Signal that indicates that a value has changed to a new value."
    value_reset: Signal = Signal()
    """Signal that indicates that  a value has been set back to the value
    it had when the widget was initialised."""

    def __init__(
        self,
        initial_value: AbstractTagValue | None = None,
        parent: QWidget | None = None,
    ) -> None:
        """Creates an EditAbstractWidget.

        Args:
            initial_value: Original value that should be displayed.
            parent: Widget this widget should be displayed on.
        """
        super().__init__(parent)
        self.clear_button: QToolButton | None = None
        "Button that clears the value being displayed and stored in the widget."
        self.reset_button: QToolButton | None = None
        "Button that restores the value to what it was at initialization."
        self.main_layout: QHBoxLayout
        "The layout that the main widget should be placed on."
        self._initial_value: AbstractTagValue | None = initial_value
        self._setupCommonUi()

    @abstractmethod
    def _setupUi(self) -> None:
        """Sets up the display of the widget.

        When this is called, it assumes that the `main_widget` and `main_layout`
        instance variables have been set.

        This function _should_ add the `main_widget` to `main_layout` or a child
        layout of `main_layout`. Any other UI initialization should be done here.
        """

    @final
    def isModified(self) -> bool:
        """Returns True if current value in the widget differs from initial value."""
        return self.value != self.original

    @property
    @abstractmethod
    def value(self) -> AbstractTagValue | None:
        """The value displayed and stored inside the widget, based on the data type."""

    @value.setter
    @abstractmethod
    def value(self, value: AbstractTagValue | None) -> None:
        pass

    @property
    @final
    def original(self) -> AbstractTagValue | None:
        """The original value that was stored inside the widget, before changes."""
        return self._initial_value

    @final
    def clear(self) -> None:
        """Clears the value stored and displayed in the widget."""
        self.value = None

    @final
    def reset(self) -> None:
        """Reset to the originally stored value, before any changes were made."""
        self.value = self.original

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
    def _setupCommonUi(self) -> None:
        """Ensures the layout and widget are created in the correct order.

        This is done so that methods can be assured that the attributes exist
        when they are run, but the attributes can be defined in child classes.
        """
        self.main_layout = self._setMainLayout()
        self._setupUi()
