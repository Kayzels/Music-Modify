"""Module for tags that store string pairs."""

from typing import override

from mutagen import id3

from music_modify.custom_types import constants

from .abstract_tag_value import AbstractTagValue


class PairedTextTagValue(AbstractTagValue):
    """Class for managing values stored in pairs."""

    def __init__(self, value: list[list[str]]) -> None:
        """Creates a PairedTextTagValue for storing pair values."""
        self._value: list[list[str]] = [
            pair for pair in value if len(pair) == constants.PAIR_SIZE
        ]

    @property
    @override
    def value(self) -> list[list[str]]:
        return self._value

    @override
    def toId3Frame(
        self, id3_key: str, encoding: id3.Encoding = id3.Encoding.UTF8
    ) -> id3.Frame:
        frame_class = getattr(id3, id3_key)
        id3_frame: id3.Frame = frame_class(encoding=encoding)
        if not hasattr(id3_frame, "people"):
            raise ValueError(
                f"Tried to create a paired text frame with an invalid id3 key: {id3_key}"
            )
        id3_frame.people = self.value
        return id3_frame

    @override
    def getDisplayValue(self) -> str:
        text_pairs: list[str] = []
        for pair in self.value:
            role, person = pair
            text_pairs.append(f"{role}: {person}")
        # TODO: Get join character from prefs
        return ", ".join(text_pairs)

    @override
    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, AbstractTagValue) and isinstance(other.value, list):
            return self.value == other.value
        if isinstance(other, str):
            return self.getDisplayValue() == other
        if isinstance(other, list):
            return self.value == other
        return False

    __hash__ = AbstractTagValue.__hash__
