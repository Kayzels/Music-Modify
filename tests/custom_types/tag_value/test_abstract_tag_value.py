"""Tests for AbstractTagValue."""

from typing import Any, override

from mutagen import id3
import pytest

from music_modify.custom_types.tag_value import AbstractTagValue


def test_AbstractTagValue_eq_NotImplemented_raised() -> None:
    """Tests that AbstractTagValue subclasses without eq raise NotImplemented."""

    class _TestTagValue(AbstractTagValue):
        @property
        @override
        def value(self) -> Any:
            return ""

        @override
        def getDisplayValue(self) -> str:
            return ""

        @override
        def toId3Frame(
            self, id3_key: str, encoding: id3.Encoding = id3.Encoding.UTF8
        ) -> id3.Frame:
            return super().toId3Frame(id3_key, encoding)

    value = _TestTagValue()
    with pytest.raises(NotImplementedError):
        _ = value == ""
