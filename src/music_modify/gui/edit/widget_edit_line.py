"""Module that defines an EditLineWidget.

This widget is used to edit metadata
that is can be contained in a single line (i.e. a single value).
"""

import logging
from typing import override

from PySide6.QtWidgets import QLineEdit, QWidget

from music_modify.custom_types.tag_value import (
    AbstractTagValue,
    TagValueFactory,
    TextTagValue,
)

from .widget_edit_abstract import EditAbstractWidget

logger = logging.getLogger(__name__)


class EditLineWidget(EditAbstractWidget):
    """Displays data in a line edit, used when the value is a single string."""

    def __init__(
        self,
        initial_value: AbstractTagValue | None = None,
        parent: QWidget | None = None,
    ) -> None:
        """Create an EditLineWidget.

        Args:
            initial_value: Original value that should be displayed.
            parent: Widget this widget should be displayed on.
        """
        if initial_value is not None and not isinstance(initial_value, TextTagValue):
            logger.warning(
                "Got an invalid initial value for an EditLineWidget. "
                + f"Expected None or a TextTagValue. Got {type(initial_value)}. "
                + "Setting to None."
            )
            initial_value = None
        if initial_value is not None and not initial_value.value:
            initial_value = None
        super().__init__(initial_value, parent)
        self.main_widget: QLineEdit
        "Main widget used to display the values currently stored."

        self._cached_value: TextTagValue | None = initial_value

    @override
    def _setupUi(self) -> None:
        layout = self.main_layout
        self.main_widget = QLineEdit()
        layout.addWidget(self.main_widget)
        self.value = self.original
        button_layout = self.createButtons()
        layout.addLayout(button_layout)

    @property
    @override
    def value(self) -> AbstractTagValue | None:
        text = self.main_widget.text()
        if not text:
            return None
        if self._cached_value is None or [text] != self._cached_value.value:
            new_value = TagValueFactory.createTagValue(text)
            if isinstance(new_value, TextTagValue):
                self._cached_value = new_value
            else:
                logger.warning(
                    "Creating a new value in EditLineWidget didn't produce a TextTagValue. "
                    + f" Got {type(new_value)}."
                )
                self._cached_value = None
        return self._cached_value

    @value.setter
    @override
    def value(self, value: AbstractTagValue | None) -> None:
        if value is None:
            self.main_widget.clear()
            return
        if not isinstance(value, TextTagValue):
            logger.warning(
                f"EditLineWidget received unexpected value type: {type(value)}. "
                + "Expected TextTagValue or None. "
                + "Clearing the stored value."
            )
            self.main_widget.clear()
            return
        if len(value.value) > 1:
            logger.warning(
                f"Expected only 1 value for EditLineWidget, but received {len(value.value)}."
            )
        self.main_widget.setText(value.getDisplayValue())


# TODO: Tests for isModified
