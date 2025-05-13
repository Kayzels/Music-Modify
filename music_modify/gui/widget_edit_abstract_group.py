# pyright: reportImplicitAbstractClass=false
from abc import abstractmethod
from typing import override

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QToolButton

from music_modify.custom_types.aliases import SongGroupData
from music_modify.custom_types.enums import Direction, EditButton

from .meta import ABCQMeta
from .widget_edit_abstract import EditAbstractWidget


class EditAbstractGroupWidget(EditAbstractWidget, metaclass=ABCQMeta):
    def __init__(self, parent: QWidget, data: SongGroupData):
        super().__init__(parent, data)

    @override
    def _createButtons(
        self,
        buttons: EditButton = EditButton.Up
        | EditButton.Down
        | EditButton.Add
        | EditButton.Remove,
        layout_type: type[QVBoxLayout | QHBoxLayout] = QVBoxLayout,
    ) -> QVBoxLayout | QHBoxLayout:
        button_layout = super()._createButtons(buttons, layout_type)

        # Group specific widgets should appear before the general ones.
        # So populate from last going forward, with insert

        if buttons & EditButton.Down:
            down_button = QToolButton(self)
            down_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown)))
            button_layout.insertWidget(0, down_button)
            down_button.clicked.connect(lambda: self._moveRows(Direction.Down))

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
            up_button.clicked.connect(lambda: self._moveRows(Direction.Up))

        return button_layout

    @abstractmethod
    def _addRow(self) -> None:
        pass

    @abstractmethod
    def _removeRow(self) -> None:
        pass

    @abstractmethod
    def _moveRows(self, direction: Direction) -> None:
        pass
