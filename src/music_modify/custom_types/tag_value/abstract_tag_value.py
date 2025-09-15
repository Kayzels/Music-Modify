"""Module that defines the general behaviour for that all Tag Values use."""

from abc import ABC, abstractmethod
from typing import Any, override

from mutagen import id3


class AbstractTagValue(ABC):
    """Abstract class for application-level tag-value representations.

    Supports storing values, equality checks, and converting to id3 frames.
    """

    join_character = ", "

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

    @abstractmethod
    def updateId3Frame(self, frame: id3.Frame) -> id3.Frame:
        """Update an existing id3 frame to store the new values."""

    @override
    def __eq__(self, other: object, /) -> bool:
        raise NotImplementedError

    @override
    def __hash__(self) -> int:
        raise TypeError("TagValue objects are not hashable.")
