# pyright: reportImplicitAbstractClass=false, reportPrivateImportUsage=false
from abc import abstractmethod
import logging

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QToolButton

from music_modify.custom_types.aliases import SongEditData, SongGroupData
from music_modify.custom_types.enums import Direction

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
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

    def _createButtons(self) -> QVBoxLayout:
        button_layout = QVBoxLayout()

        up_button = QToolButton(self)
        up_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp)))
        button_layout.addWidget(up_button)
        up_button.clicked.connect(lambda: self._moveRows(Direction.Up))

        add_button = QToolButton(self)
        add_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd)))
        button_layout.addWidget(add_button)
        add_button.clicked.connect(self._addRow)

        remove_button = QToolButton(self)
        remove_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove)))
        button_layout.addWidget(remove_button)
        remove_button.clicked.connect(self._removeRow)

        down_button = QToolButton(self)
        down_button.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown)))
        button_layout.addWidget(down_button)
        down_button.clicked.connect(lambda: self._moveRows(Direction.Down))

        return button_layout

    @abstractmethod
    def _initValue(self, data: SongGroupData) -> None:
        pass

    @abstractmethod
    def _setupUi(self) -> None:
        logger.info("Abstract setupUi called")
        pass

    def _emitUpdate(self) -> None:
        if self._isReset():
            self.value_reset.emit()
        else:
            self.value_updated.emit()

    @abstractmethod
    def _isReset(self) -> bool:
        logger.info("Abstract isReset called")
        pass

    @abstractmethod
    def _updateValue(self) -> None:
        logger.info("Abstract updateValue called")
        pass

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
