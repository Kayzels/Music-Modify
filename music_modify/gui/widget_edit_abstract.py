# pyright: reportImplicitAbstractClass=false, reportPrivateImportUsage=false
from abc import abstractmethod
import copy
import logging

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QToolButton

from music_modify.custom_types.aliases import SongEditData, SongGroupData
from music_modify.custom_types.enums import Direction, EditButton

from .meta import ABCQMeta

logger = logging.getLogger(__name__)


class EditAbstractWidget(QWidget, metaclass=ABCQMeta):
    value_updated: Signal = Signal()
    value_reset: Signal = Signal()

    def __init__(self, parent: QWidget, data: SongGroupData):
        super().__init__(parent)
        self._initValue(data)
        self._setMainLayout()
        self._setupUi()

    def _setMainLayout(self):
        """Creates the basic layout for the widget."""
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

    def _createButtons(
        self,
        buttons: EditButton = EditButton.Up
        | EditButton.Down
        | EditButton.Add
        | EditButton.Remove,
    ) -> QVBoxLayout:
        """Adds buttons for moving rows up and down, adding and deleting rows."""
        button_layout = QVBoxLayout()

        if buttons & EditButton.Up:
            up_button = QToolButton(self)
            up_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp)))
            button_layout.addWidget(up_button)
            up_button.clicked.connect(lambda: self._moveRows(Direction.Up))

        if buttons & EditButton.Add:
            add_button = QToolButton(self)
            add_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd)))
            button_layout.addWidget(add_button)
            add_button.clicked.connect(self._addRow)

        if buttons & EditButton.Remove:
            remove_button = QToolButton(self)
            remove_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove)))
            button_layout.addWidget(remove_button)
            remove_button.clicked.connect(self._removeRow)

        if buttons & EditButton.Down:
            down_button = QToolButton(self)
            down_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown)))
            button_layout.addWidget(down_button)
            down_button.clicked.connect(lambda: self._moveRows(Direction.Down))

        return button_layout

    @abstractmethod
    def _initValue(self, data: SongGroupData) -> None:
        """Sets the original value that the widget should store."""
        pass

    @abstractmethod
    def _setupUi(self) -> None:
        logger.info("Abstract setupUi called")
        pass

    def _emitUpdate(self) -> None:
        """Emit a signal indicating whether the data has changed, or been reset."""
        if self._isReset():
            self.value_reset.emit()
        else:
            self.value_updated.emit()

    @abstractmethod
    def _isReset(self) -> bool:
        """Returns whether the value has been set back to its original state."""
        logger.info("Abstract isReset called")
        pass

    @abstractmethod
    def _updateValue(self) -> None:
        """Updates the value that is stored in the widget, and displayed."""
        logger.info("Abstract updateValue called")
        pass

    @abstractmethod
    def _displayValue(self) -> None:
        """Sets the values for the table based on the current value property."""
        pass

    def reset(self) -> None:
        """Reset to the originally stored value, before any changes were made."""
        if not self._isReset():
            self.value = copy.deepcopy(self.original)
            self._displayValue()
            self._emitUpdate()

    @abstractmethod
    def _addRow(self) -> None:
        pass

    @abstractmethod
    def _removeRow(self) -> None:
        pass

    @abstractmethod
    def _moveRows(self, direction: Direction) -> None:
        pass

    @property
    @abstractmethod
    def value(self) -> SongEditData:
        logger.info("Abstract value property called")
        pass

    @value.setter
    def value(self, value: SongEditData):
        self.value = value

    @property
    @abstractmethod
    def original(self) -> SongEditData:
        pass
