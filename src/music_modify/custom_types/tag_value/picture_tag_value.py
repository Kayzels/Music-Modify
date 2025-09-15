"""Module for tags that store images."""

import logging
from typing import override

from mutagen import id3

from .abstract_tag_value import AbstractTagValue

logger = logging.getLogger(__name__)


class PictureTagValue(AbstractTagValue):
    """Class for managing tags that store image values."""

    def __init__(
        self,
        data: bytes = b"",
        mime: str = "",
        picture_type: id3.PictureType = id3.PictureType.COVER_FRONT,
        *,
        desc: str = "",
        salt: str | None = None,
    ) -> None:
        """Creates a PictureTagValue for storing image values.

        Args:
            data: Raw image data, as a byte string.
            mime: The mimetype for the image. Use "->" if the data is a URI.
            picture_type: What the image being stored is of; the source of the image.
            parent: The QObject that owns this one. When that object is deleted,
                this object is too.
            join_character: The character used for joining the details
                in the string representation.
            desc: Text description of the image.
            salt: Value used to ensure unique frames with the same description.
        """
        self._data: bytes = data
        self.mime: str = mime
        self.picture_type: id3.PictureType = picture_type
        self.desc: str | None = desc
        self.salt: str | None = salt

    @property
    @override
    def value(self) -> bytes:
        return self._data

    @override
    def toId3Frame(
        self, id3_key: str, encoding: id3.Encoding = id3.Encoding.UTF8
    ) -> id3.Frame:
        if id3_key != "APIC":
            logger.warning(
                f"Sent an unexpected id3 key for a PictureTagValue: {id3_key}."
            )

        apic = id3.APIC(mime=self.mime, type=self.picture_type, data=self.value)
        if self.desc:
            apic.desc = self.desc
        if self.salt:
            apic.salt = self.salt
        return apic

    @override
    def updateId3Frame(self, frame: id3.Frame) -> id3.Frame:
        if frame.FrameID != "APIC":
            raise ValueError("Tried to update a frame that wasn't an image frame.")
        frame.data = self.value
        frame.type = self.picture_type
        frame.mime = self.mime
        if self.desc:
            frame.desc = self.desc
        if self.salt:
            frame.salt = self.salt
        return frame

    @override
    def getDisplayValue(self) -> str:
        # They don't use the builtin enum type,
        # so no name or value attributes.
        picture_type = (
            str(self.picture_type)
            .removeprefix("PictureType.")
            .replace("_", " ")
            .title()
        )
        result = f"Attached Picture: {picture_type}"
        suffix = ""
        if self.desc:
            suffix += self.desc
        if self.mime:
            if suffix:
                suffix += AbstractTagValue.join_character
            suffix += self.mime
        if suffix:
            result += f" ({suffix})"
        return result

    @override
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, PictureTagValue):
            return False

        attributes: tuple[str, ...] = ("value", "mime", "picture_type", "desc", "salt")

        return other.value == self.value and all(
            getattr(self, attr) == getattr(other, attr) for attr in attributes
        )

    __hash__ = AbstractTagValue.__hash__
