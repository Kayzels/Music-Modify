import copy
import logging
from abc import abstractmethod

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QToolButton, QVBoxLayout, QWidget

from music_modify.custom_types.aliases import SongEditData, SongGroupData
from music_modify.custom_types.enums import EditButton
from music_modify.gui.meta import ABCQMeta

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
        buttons: EditButton = EditButton.Reset | EditButton.Clear,
        layout_type: type[QVBoxLayout | QHBoxLayout] = QHBoxLayout,
    ) -> QVBoxLayout | QHBoxLayout:
        """Adds buttons for moving rows up and down, adding and deleting rows."""
        button_layout = layout_type()

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

    @abstractmethod
    def _clearValue(self) -> None:
        """Sets the value to the equivalent empty value."""
        pass

    def reset(self) -> None:
        """Reset to the originally stored value, before any changes were made."""
        if not self._isReset():
            self.value = copy.deepcopy(self.original)
            self._displayValue()
            self._emitUpdate()

    def clear(self) -> None:
        """Clears the value stored and displayed in the widget."""
        self._clearValue()
        self._displayValue()
        self._emitUpdate()

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
