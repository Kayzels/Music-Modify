"""Defines functionality for working with rows in widgets."""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from functools import cached_property
import logging
from typing import final

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton, QWidget

from music_modify.core.enums import EditButton, RowDirection
from music_modify.core.meta import ABCQMeta

logger = logging.getLogger(__name__)


class RowOperationMixin(ABC, metaclass=ABCQMeta):
    """Mixin for widgets that support row-based operations (add, remove, move).

    Calling on `createButtonOperations` will create the signals, set the icons,
    and set instance attributes for the specific button.
    If this function isn't called, this mixin does nothing.

    It is an abstract class that requires that `_addRow`, `_removeRow`, and `_moveRows`
    are defined.

    If `createButtonOperations` is called with the specified button types,
    this will create instance attributes for `add_button`, `remove_button`, `up_button`
    and `down_button`.

    Attributes:
        add_button (QToolButton): Button to add row to widget
        remove_button (QToolButton): Button to remove selected row from widget
        up_button (QToolButton): Button for moving rows up in the widget
        down_button (QToolButton): Button for moving rows down in the widget
    """

    @abstractmethod
    def _addRow(self) -> None:
        """Adds a row to the widget."""

    @abstractmethod
    def _removeRow(self) -> None:
        """Removes the selected row(s) from the widget."""

    @abstractmethod
    def _moveRows(self, direction: RowDirection) -> None:
        """Moves the selected rows in the specified direction."""

    @cached_property
    def _button_icons(self) -> Mapping[EditButton, QIcon.ThemeIcon]:
        """Stores the possible icons that buttons can have."""
        return {
            EditButton.Add: QIcon.ThemeIcon.ListAdd,
            EditButton.Remove: QIcon.ThemeIcon.ListRemove,
            EditButton.Up: QIcon.ThemeIcon.GoUp,
            EditButton.Down: QIcon.ThemeIcon.GoDown,
        }

    @final
    def _createSignalConnection(
        self, button: QToolButton, button_type: EditButton
    ) -> None:
        """Creates the signal for the button, based on the type.

        Args:
            button: The displayed button to create a signal for
            button_type: The kind of signal that should be added to the button.
                It needs to be a _single_ flag, so it should be called with
                `&` (bitwise and) before being sent through,
                so that it's the only flag.

        Important:
            The `button_type` needs to be the specific type.
            It should be called with `&` (bitwise and) before being sent through.
            This ensures it's only the one flag.
        """
        if len(button_type) != 1:
            raise ValueError("button_type must be a single EditButton flag.")

        match button_type:
            case EditButton.Down:
                button.clicked.connect(lambda: self._moveRows(RowDirection.Down))
            case EditButton.Up:
                button.clicked.connect(lambda: self._moveRows(RowDirection.Up))
            case EditButton.Add:
                button.clicked.connect(self._addRow)
            case EditButton.Remove:
                button.clicked.connect(self._removeRow)
            case _:
                logger.info(
                    f"Invalid button type called: {button_type}. No action taken."
                )

    @final
    def _setAttribute(self, button: QToolButton, button_type: EditButton) -> None:
        """Sets the button to be an instance attribute, based on the type.

        Args:
            button: The displayed button that should be made an attribute
            button_type: The type of attribute that should be set.
                It needs to be a _single_ flag, so it should be called with
                `&` (bitwise and) before being sent through,
                so that it's the only flag.

        Important:
            The `button_type` needs to be the specific type.
            It should be called with `&` (bitwise and) before being sent through.
            This ensures it's only the one flag.
        """
        if len(button_type) != 1:
            raise ValueError("button_type must be a single EditButton flag.")

        match button_type:
            case EditButton.Down:
                button.setText("Move down")
                self.down_button: QToolButton = button
                "Button used for moving rows down in the widget."
            case EditButton.Up:
                button.setText("Move up")
                self.up_button: QToolButton = button
                "Button used for moving rows up in the widget."
            case EditButton.Add:
                button.setText("Add rows")
                self.add_button: QToolButton = button
                "Button that adds a row to the widget."
            case EditButton.Remove:
                button.setText("Remove rows")
                self.remove_button: QToolButton = button
                "Button that removes the selected row from the widget."
            case _:
                logger.info(
                    f"Invalid button type called: {button_type}. No action taken."
                )

    @final
    def _setIcon(self, button: QToolButton, button_type: EditButton) -> None:
        """Sets the icon for the button, based on the type.

        Args:
            button: The displayed button that the icon should be set for
            button_type: The type of button being made, which defined the icon to set.
                It needs to be a _single_ flag, so it should be called with
                `&` (bitwise and) before being sent through,
                so that it's the only flag.

        Important:
            The `button_type` needs to be the specific type.
            It should be called with `&` (bitwise and) before being sent through.
            This ensures it's only the one flag.
        """
        if len(button_type) != 1:
            raise ValueError("button_type must be a single EditButton flag.")

        if button_type in self._button_icons:
            button.setIcon(QIcon(QIcon.fromTheme(self._button_icons[button_type])))

    # noinspection PyTypeChecker
    @final
    def createOperationButtons(
        self,
        parent: QWidget,
        buttons: EditButton = (
            EditButton.Up | EditButton.Add | EditButton.Remove | EditButton.Down
        ),
        order: tuple[EditButton, EditButton, EditButton, EditButton] = (
            EditButton.Up,
            EditButton.Add,
            EditButton.Remove,
            EditButton.Down,
        ),
    ) -> list[QToolButton]:
        """Creates the buttons for row operations.

        Args:
            parent: The widget that the buttons should be parented by
            buttons: The kinds of buttons to create.
            order (optional): The way that buttons should be arranged.
                Should contain Up, Add, Remove, and Down in any order,
                with no duplicates.

        Returns:
            A list of the created buttons.
        """
        new_buttons = []

        for edit_button in (
            EditButton.Up | EditButton.Add | EditButton.Remove | EditButton.Down
        ):
            if edit_button not in order:
                raise Exception(f"Missing required button in order: {edit_button}")

        for edit_button in order:
            if edit_button in buttons:
                new_button = QToolButton(parent)
                current_flag = buttons & edit_button
                self._setIcon(new_button, current_flag)
                self._createSignalConnection(new_button, current_flag)
                self._setAttribute(new_button, current_flag)
                new_buttons.append(new_button)

        return new_buttons
