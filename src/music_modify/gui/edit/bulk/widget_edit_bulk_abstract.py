"""Module that defines a EditBulkAbstractWidget.

This is the abstract class that defines the functionality
that all widgets on a BulkEditDialog should have.
"""

from abc import ABC, abstractmethod
import logging

from PySide6.QtWidgets import QWidget

from music_modify.core.meta import ABCQMeta
from music_modify.custom_types import Song, TagInfo

logger = logging.getLogger(__name__)


class EditBulkAbstractWidget(QWidget, ABC, metaclass=ABCQMeta):
    """Defines the functionality that all widgets on a BulkEditDialog should have."""

    split_text_entered: str = ", "
    "The string that is used to split values when multiple are entered."
    # TODO: Must be updated in MainWindow

    def __init__(self, tag: TagInfo, parent: QWidget | None = None) -> None:
        """Creates a widget on `parent` for displaying the data in `tag`.

        Args:
            tag: The field in the song that this widget displays the data for.
            parent: The widget that this widget should be displayed on.
        """
        super().__init__(parent)

        self._tag: TagInfo = tag

    @abstractmethod
    def setupUi(self) -> None:
        """Creates the display of the widget."""

    @abstractmethod
    def updateTag(self, songs: list[Song]) -> set[Song]:
        """Update the value for the tag in all the songs.

        Args:
            songs: The list of songs that should be updated

        Returns:
            The set of songs that need to be updated.
        """

    @property
    def tag(self) -> TagInfo:
        """The tag that contains the metadata for the data the widget displays."""
        return self._tag
