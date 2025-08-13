"""Module that contains the abstract class that defines the functionality
that all widgets on a BulkEditDialog should have."""

from abc import ABC, abstractmethod
import logging

from PySide6.QtWidgets import QWidget

from music_modify.custom_types import Song, SongTag
from music_modify.gui.meta import ABCQMeta

logger = logging.getLogger(__name__)


class EditBulkAbstractWidget(QWidget, ABC, metaclass=ABCQMeta):
    def __init__(self, parent: QWidget, tag: SongTag) -> None:
        super().__init__(parent)

        self._tag: SongTag = tag

    @abstractmethod
    def setupUi(self) -> None:
        """Creates the display of the widget."""

    @abstractmethod
    def updateTag(self, songs: list[Song]) -> bool:
        """Update the value for the tag in all the songs.

        Args:
            songs: The list of songs that should be updated

        Returns:
            True if the songs were successfully updated, else False.
        """

    @property
    def tag(self) -> SongTag:
        """The tag that contains the metadata for the data the widget displays."""
        return self._tag
