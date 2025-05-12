# pyright: reportIncompatibleMethodOverride=false
import copy
import logging
from typing import override

from PySide6.QtWidgets import QLineEdit, QWidget

from music_modify.custom_types.aliases import SongLineData
from music_modify.custom_types.enums import Direction

from .widget_edit_abstract import EditAbstractWidget

logger = logging.getLogger(__name__)


class EditLineWidget(EditAbstractWidget):
    def __init__(self, parent: QWidget, data: SongLineData):
        super().__init__(parent, data)

        self._original_data: str
        self.main_widget: QLineEdit

    @override
    def _initValue(self, data: SongLineData):
        if data is None or len(data) == 0:
            self.value = ""
        else:
            self.value = str(data[0])

        self._original_data = self.value

    @override
    def _setupUi(self) -> None:
        layout = self.layout()
        if layout is None:
            logger.info("Didn't create a layout for line edit")
            return

        self.main_widget = QLineEdit()
        self._displayValue()
        layout.addWidget(self.main_widget)
        self.main_widget.editingFinished.connect(self._updateValue)

    @override
    def _isReset(self) -> bool:
        return self.value == self.original

    @override
    def _updateValue(self) -> None:
        new_text = self.main_widget.text()
        if new_text != self.value:
            self.value = new_text
            self._emitUpdate()

    @override
    def _displayValue(self) -> None:
        """Sets the values for the table based on the current value property."""
        if not hasattr(self, "main_widget"):
            return

        self.main_widget.setText(self.value)

    @override
    def _removeRow(self) -> None:
        return

    @override
    def _addRow(self) -> None:
        return

    @override
    def _moveRows(self, direction: Direction) -> None:
        return

    @property
    @override
    def value(self) -> str:
        return self._value

    @value.setter
    @override
    def value(self, value: str):
        self._value: str = value

    @property
    @override
    def original(self) -> str:
        return self._original_data


# TODO: Add reset and clear buttons next to the line edit
