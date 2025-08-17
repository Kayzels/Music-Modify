"""Module that defines an EditLineWidget.

This widget is used to edit metadata
that is can be contained in a single line (i.e. a single value).
"""

import logging
from typing import override

from PySide6.QtWidgets import QLineEdit, QWidget

from .widget_edit_abstract import EditAbstractWidget

logger = logging.getLogger(__name__)


class EditLineWidget(EditAbstractWidget[str, QLineEdit]):
    """Displays data in a line edit, used when the value is a single string."""

    def __init__(self, parent: QWidget, data: str | None) -> None:
        """Create an EditLineWidget.

        Args:
            parent: The widget that this widget should be displayed on.
            data: The data to be displayed on this widget.
        """
        super().__init__(parent, data)

        self._original_data: str

    @override
    def _initValue(self, data: str | None, /) -> None:
        if data is None:
            self.value = ""
        else:
            self.value = data

        self._original_data = self.value

    @override
    def _setMainWidget(self) -> QLineEdit:
        main_widget = QLineEdit()
        main_widget.editingFinished.connect(self._updateValue)
        return main_widget

    @override
    def _setupUi(self) -> None:
        layout = self.main_layout
        self._displayValue()
        layout.addWidget(self.main_widget)
        button_layout = self.createButtons()
        layout.addLayout(button_layout)

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
