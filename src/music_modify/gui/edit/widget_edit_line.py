"""Module that defines a widget that is used to edit metadata
that is can be contained in a single line (i.e. a single value)."""

import logging
from typing import cast, override

from PySide6.QtWidgets import QHBoxLayout, QLayout, QLineEdit, QWidget

from .widget_edit_abstract import EditAbstractWidget

logger = logging.getLogger(__name__)


class EditLineWidget(EditAbstractWidget[str]):
    """Displays data in a line edit, used when the value is a single string."""

    def __init__(self, parent: QWidget, data: str | None) -> None:
        super().__init__(parent, data)

        self._original_data: str
        self.main_widget: QLineEdit

    @override
    def _initValue(self, data: str | None) -> None:
        if data is None:
            self.value = ""
        else:
            self.value = data

        self._original_data = self.value

    @override
    def _setupUi(self) -> None:
        layout: QLayout | None = self.layout()
        if layout is None:
            logger.info("Didn't create a layout for line edit")
            return
        layout = cast(QHBoxLayout, layout)

        self.main_widget = QLineEdit()
        self._displayValue()
        layout.addWidget(self.main_widget)
        button_layout = self.createButtons()
        layout.addLayout(button_layout)
        self.main_widget.editingFinished.connect(self._updateValue)

    @override
    def _isReset(self) -> bool:
        return self.value == self.original

    @override
    def _updateValue(self) -> None:
        new_text: str = self.main_widget.text()
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
    def _clearValue(self) -> None:
        self.value = ""

    @property
    @override
    def value(self) -> str:
        return self._value

    @value.setter
    @override
    def value(self, value: str) -> None:
        self._value: str = value

    @property
    @override
    def original(self) -> str:
        return self._original_data
