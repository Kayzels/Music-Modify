"""Module for tags that store strings, lists of strings, and similar."""

from collections.abc import Sequence
from typing import override

from mutagen import id3

from .abstract_tag_value import AbstractTagValue


class TextTagValue(AbstractTagValue):
    """Class for managing text values (single or multiple)."""

    def __init__(
        self,
        value: Sequence[str | id3.ID3TimeStamp],
    ) -> None:
        """Creates a TextTagValue for storing text values."""
        self._value = [str(t) for t in value]

    @property
    @override
    def value(self) -> list[str]:
        return self._value

    @override
    def toId3Frame(
        self, id3_key: str, encoding: id3.Encoding = id3.Encoding.UTF8
    ) -> id3.Frame:
        if id3_key.startswith("TXXX"):
            desc = id3_key.removeprefix("TXXX").removeprefix(":")
            if not desc:
                raise ValueError("Cannot create a TXXX frame without a desc.")
            return id3.TXXX(encoding=encoding, text=self.value, desc=desc)
        frame_class = getattr(id3, id3_key)
        id3_frame: id3.Frame = frame_class(encoding=encoding)
        if not hasattr(id3_frame, "text"):
            raise ValueError(
                f"Tried to create a text frame with an invalid id3 key: {id3_key}"
            )
        id3_frame.text = self.value
        return id3_frame

    @override
    def getDisplayValue(self) -> str:
        return AbstractTagValue.join_character.join(self.value)

    @override
    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, AbstractTagValue) and isinstance(other.value, list):
            return self.value == other.value
        if isinstance(other, str | id3.ID3TimeStamp):
            return self.getDisplayValue() == str(other)
        if isinstance(other, list):
            if all(isinstance(item, str) for item in other):
                return self.value == other
            converted_items = [str(item) for item in other]
            return self.value == converted_items
        return False

    __hash__ = AbstractTagValue.__hash__
