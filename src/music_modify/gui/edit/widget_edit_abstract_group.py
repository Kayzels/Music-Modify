"""Module that defines the abstract class used for widgets
in an EditDialog that display groups of values,
rather than a single value."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QBoxLayout, QToolButton, QWidget

from music_modify.custom_types.aliases import SongListData, SongTableData
from music_modify.custom_types.enums import EditButton, RowDirection
from music_modify.gui.meta import ABCQMeta

from .widget_edit_abstract import EditAbstractWidget

ValueG = TypeVar("ValueG", bound=SongListData | SongTableData)


class EditAbstractGroupWidget(
    EditAbstractWidget[ValueG], Generic[ValueG], ABC, metaclass=ABCQMeta
):
    """Abstract class for widgets displayed on an EditDialog
    that contain multiple items, which can be displayed in lists or tables.
    """

    def __init__(self, parent: QWidget, data: ValueG | None):
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
            down_button = QToolButton(self)
            down_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown)))
            button_layout.insertWidget(0, down_button)
            down_button.clicked.connect(lambda: self._moveRows(RowDirection.Down))

        if buttons & EditButton.Remove:
            remove_button = QToolButton(self)
            remove_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove)))
            button_layout.insertWidget(0, remove_button)
            remove_button.clicked.connect(self._removeRow)

        if buttons & EditButton.Add:
            add_button = QToolButton(self)
            add_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd)))
            button_layout.insertWidget(0, add_button)
            add_button.clicked.connect(self._addRow)

        if buttons & EditButton.Up:
            up_button = QToolButton(self)
            up_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp)))
            button_layout.insertWidget(0, up_button)
            up_button.clicked.connect(lambda: self._moveRows(RowDirection.Up))

        return button_layout

    @abstractmethod
    def _addRow(self) -> None:
        """Adds a row to the bottom of the widget."""
        pass

    @abstractmethod
    def _removeRow(self) -> None:
        """Removes the selected rows from the widget."""
        pass

    @abstractmethod
    def _moveRows(self, direction: RowDirection) -> None:
        """Moves the selected rows in the specified direction."""
        pass
