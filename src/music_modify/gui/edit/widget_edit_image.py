"""Module that defines an EditImageWidget.

This widget is used to edit image metadata.
"""

import logging
from typing import override

from PySide6.QtCore import QByteArray
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget

from music_modify.custom_types.tag_value import AbstractTagValue, PictureTagValue

from .widget_edit_abstract import EditAbstractWidget

logger = logging.getLogger(__name__)


class EditImageWidget(EditAbstractWidget):
    """Displays images in a QLabel."""

    def __init__(
        self,
        initial_value: AbstractTagValue | None = None,
        parent: QWidget | None = None,
    ) -> None:
        """Create an EditImageWidget.

        Args:
            initial_value: Original value that should be displayed.
            parent: Widget this widget should be displayed on.
        """
        if initial_value is not None and not isinstance(initial_value, PictureTagValue):
            logger.warning(
                "Got an invalid initial value for an EditImageWidget. "
                + f"Expected None or a PictureTagValue. Got {type(initial_value)}. "
                + "Setting to None."
            )
            initial_value = None
        if initial_value is not None and not initial_value.value:
            initial_value = None
        super().__init__(initial_value, parent)

        self.main_widget: QLabel
        self._cached_value: PictureTagValue | None = initial_value

    @override
    def _setupUi(self) -> None:
        self.main_widget = QLabel()
        self.main_widget.setScaledContents(True)
        self.main_widget.setMaximumSize(200, 200)
        self.main_layout.addWidget(self.main_widget)
        self.value = self.original

        return super()._setupUi()

    @property
    @override
    def value(self) -> AbstractTagValue | None:
        return self._cached_value

    @value.setter
    @override
    def value(self, value: AbstractTagValue | None) -> None:
        if value is None:
            self.main_widget.clear()
            self._cached_value = None
            return

        if not isinstance(value, PictureTagValue):
            logger.warning(
                f"EditImageWidget received unexpected value type: {type(value)}. "
                + "Expected PictureTagValue or None. "
                + "Clearing the displayed image."
            )
            self.main_widget.clear()
            self._cached_value = None
            return

        if not value.value:
            self.main_widget.clear()
            self._cached_value = None

        pixmap = QPixmap()
        if not pixmap.loadFromData(QByteArray(value.value)):
            logger.error("Failed to load image data into QPixmap")
            self.main_widget.clear()
            self._cached_value = None
            return

        self.main_widget.setPixmap(pixmap)
        self._cached_value = value
