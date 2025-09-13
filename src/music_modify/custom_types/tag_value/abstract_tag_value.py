"""Module that defines the general behaviour for that all Tag Values use."""

from abc import ABC, abstractmethod
from typing import Any, override

from mutagen import id3
from PySide6.QtCore import QObject, Signal, Slot

from music_modify.core.meta import ABCQMeta


class AbstractTagValue(QObject, ABC, metaclass=ABCQMeta):
    """Abstract class for application-level tag-value representations.

    Supports storing values, equality checks, and converting to id3 frames.
    """

    join_character_changed: Signal = Signal()

    def __init__(
        self, /, join_character: str = ", ", parent: QObject | None = None
    ) -> None:
        """Creates an AbstractTagValue."""
        super().__init__(parent)
        self._join_character: str = join_character

    @property
    def join_character(self) -> str:
        """Character used to join values when displaying."""
        return self._join_character

    @join_character.setter
    def join_character(self, character: str) -> None:
        current = self.join_character
        if current != character:
            self._join_character = character
            self.join_character_changed.emit()

    @Slot(str)
    def setJoinCharacter(self, character: str) -> None:
        """Slot for setting the join character, to make it easier for Qt."""
        self.join_character = character

    @property
    @abstractmethod
    def value(self) -> Any:  # noqa: ANN401
        """Value that is being stored."""

    @abstractmethod
    def toId3Frame(
        self, id3_key: str, encoding: id3.Encoding = id3.Encoding.UTF8
    ) -> id3.Frame:
        """Create an ID3 frame storing the data for the specific ID3 key."""

    @abstractmethod
    def getDisplayValue(self) -> str:
        """Returns a string representation of the stored value."""

    @override
    def __eq__(self, other: object, /) -> bool:
        raise NotImplementedError

    @override
    def __hash__(self) -> int:
        raise TypeError("TagValue objects are not hashable.")
