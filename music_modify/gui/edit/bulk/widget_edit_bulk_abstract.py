from abc import abstractmethod
import logging

from PySide6.QtWidgets import QWidget

from music_modify.custom_types import Song, SongTag
from music_modify.gui.meta import ABCQMeta

logger = logging.getLogger(__name__)


class EditBulkAbstractWidget(QWidget, metaclass=ABCQMeta):
    def __init__(self, parent: QWidget, tag: SongTag):
        super().__init__(parent)

        self._tag: SongTag = tag

    @abstractmethod
    def setupUi(self) -> None:
        pass

    @abstractmethod
    def updateTag(self, songs: list[Song]) -> bool:
        pass

    @property
    def tag(self) -> SongTag:
        return self._tag
