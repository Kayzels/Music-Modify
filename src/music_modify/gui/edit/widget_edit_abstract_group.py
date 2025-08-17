"""Module that defines an EditAbstractGroupWidget.

This widget is the abstract class used for widgets
in an EditDialog that display groups of values,
rather than a single value.
"""

from abc import ABC, abstractmethod
from typing import override

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QToolButton, QWidget

from music_modify.custom_types.aliases import SongListData, SongTableData
from music_modify.custom_types.enums import EditButton, RowDirection
from music_modify.gui.meta import ABCQMeta

from .widget_edit_abstract import EditAbstractWidget


class EditAbstractGroupWidget[ValueG: SongListData | SongTableData, WidgetT: QWidget](
    EditAbstractWidget[ValueG, WidgetT],
    ABC,
    metaclass=ABCQMeta,
):
    """Abstract class for widgets on an EditDialog that contain multiple items.

    These items can be displayed in lists or tables.
    """

    def __init__(self, parent: QWidget, data: ValueG | None) -> None:
        """Create an EditAbstractGroupWidget.

        Args:
            parent: The widget that this widget should be displayed on.
            data: The data to be displayed on this widget.
        """
        self.down_button: QToolButton | None = None
        "Button used for moving rows down in the widget."
        self.remove_button: QToolButton | None = None
        "Button that removes the selected row from the widget."
        self.add_button: QToolButton | None = None
        "Button that adds a row to the widget."
        self.up_button: QToolButton | None = None
        "Button used for moving rows up in the widget."
        super().__init__(parent, data)

    # noinspection PyTypeChecker
    @override
    def createButtons(
        self,
        buttons: EditButton = EditButton.Up
        | EditButton.Down
        | EditButton.Add
        | EditButton.Remove,
        direction: QBoxLayout.Direction = QBoxLayout.Direction.TopToBottom,
    ) -> QBoxLayout:
        button_layout = super().createButtons(buttons, direction)

        # Group specific widgets should appear before the general ones.
        # So populate from last going forward, with insert

        if buttons & EditButton.Down:
            self.down_button = QToolButton(self)
            self.down_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown)))
            button_layout.insertWidget(0, self.down_button)
            self.down_button.clicked.connect(lambda: self._moveRows(RowDirection.Down))

        if buttons & EditButton.Remove:
            self.remove_button = QToolButton(self)
            self.remove_button.setIcon(
                QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
            )
            button_layout.insertWidget(0, self.remove_button)
            self.remove_button.clicked.connect(self._removeRow)

        if buttons & EditButton.Add:
            self.add_button = QToolButton(self)
            self.add_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd)))
            button_layout.insertWidget(0, self.add_button)
            self.add_button.clicked.connect(self._addRow)

        if buttons & EditButton.Up:
            self.up_button = QToolButton(self)
            self.up_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp)))
            button_layout.insertWidget(0, self.up_button)
            self.up_button.clicked.connect(lambda: self._moveRows(RowDirection.Up))

        return button_layout

    @abstractmethod
    def _addRow(self) -> None:
        """Adds a row to the bottom of the widget."""

    @abstractmethod
    def _removeRow(self) -> None:
        """Removes the selected rows from the widget."""

    @abstractmethod
    def _moveRows(self, direction: RowDirection) -> None:
        """Moves the selected rows in the specified direction."""
