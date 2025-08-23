"""Module that defines a EditBulkAbstractWidget.

This is the abstract class that defines the functionality
that all widgets on a BulkEditDialog should have.
"""

from abc import ABC, abstractmethod
import logging

from PySide6.QtWidgets import QWidget

from music_modify.custom_types import Song, SongTag
from music_modify.gui.meta import ABCQMeta

logger = logging.getLogger(__name__)


class EditBulkAbstractWidget(QWidget, ABC, metaclass=ABCQMeta):
    """Defines the functionality that all widgets on a BulkEditDialog should have."""

    def __init__(self, parent: QWidget, tag: SongTag) -> None:
        """Creates a widget on `parent` for displaying the data in `tag`.

        Args:
            parent: The widget that this widget should be displayed on.
            tag: The field in the song that this widget displays the data for.
        """
        super().__init__(parent)

        self._tag: SongTag = tag

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
    def tag(self) -> SongTag:
        """The tag that contains the metadata for the data the widget displays."""
        return self._tag
