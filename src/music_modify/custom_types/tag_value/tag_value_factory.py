"""Module for a TagValueFactory, that creates TagValues."""

import logging
import mimetypes
from pathlib import Path
from typing import Any, cast

from mutagen import id3
from PySide6.QtCore import QObject

from music_modify.custom_types import constants

from .abstract_tag_value import AbstractTagValue
from .paired_text_tag_value import PairedTextTagValue
from .picture_tag_value import PictureTagValue
from .text_tag_value import TextTagValue

logger = logging.getLogger(__name__)


class TagValueFactory:
    """Factory for creating AbstractTagValue subclass instances."""

    @staticmethod
    def fromId3Frame(
        frame: id3.Frame, parent: QObject | None = None
    ) -> AbstractTagValue | None:
        """Converts a mutagen id3.Frame object into an AbstractTagValue instance.

        Returns None if the frame stores data in an unknown format.
        """
        # NOTE: Using getattr because static analysis doesn't find attributes.
        match frame:
            case id3.TextFrame():
                return TextTagValue(getattr(frame, "text", []), parent)
            case id3.PairedTextFrame():
                return PairedTextTagValue(getattr(frame, "people", []), parent)
            case id3.APIC():
                return PictureTagValue(
                    data=getattr(frame, "data", b""),
                    mime=getattr(frame, "mime", ""),
                    picture_type=getattr(frame, "type", id3.PictureType.COVER_FRONT),
                    parent=parent,
                    desc=getattr(frame, "desc", ""),
                    salt=getattr(frame, "salt", None),
                )
            case _:
                return None

    @staticmethod
    def _generateApicValue(
        path: Path, parent: QObject | None = None
    ) -> PictureTagValue | None:
        """Generate a PictureTagValue from the file path, if valid."""
        if not path.exists():
            logger.error("No file existed at the path sent.")
            return None
        try:
            with path.open("rb") as f:
                image_data = f.read()
            mime_type = mimetypes.guess_type(path)[0]
            if mime_type is None:
                logger.warning(f"Could not guess mimetype for '{path}'.")
                mime_type = ""
            return PictureTagValue(image_data, mime_type, parent=parent)
        except OSError:
            logger.exception(f"Error reading image file '{path}' for APIC tag.")
            return None

    @staticmethod
    def _generateFromListValue(
        values: list[Any], parent: QObject | None = None
    ) -> AbstractTagValue | None:
        v = values
        if all(isinstance(item, str) for item in v):
            v = cast(list[str], v)
            return TextTagValue(v, parent)
        if all(
            isinstance(item, list)
            and len(item) == constants.PAIR_SIZE
            and all(isinstance(inner_value, str) for inner_value in item)
            for item in v
        ):
            v = cast(list[list[str]], v)
            return PairedTextTagValue(v, parent)
        return None

    @staticmethod
    def _generateFromEmptyValue(
        id3_key: str | None, parent: QObject | None = None
    ) -> AbstractTagValue | None:
        match id3_key:
            case None:
                return None
            case "APIC":
                return PictureTagValue(parent=parent)
            case "TIPL" | "TMCL":
                return PairedTextTagValue([], parent)
            case t if t.startswith("T"):
                return TextTagValue([], parent)
            case _:
                return None

    @staticmethod
    def createTagValue(
        value_input: Any,  # noqa: ANN401
        id3_key: str | None = None,
        parent: QObject | None = None,
    ) -> AbstractTagValue | None:
        """Creates an AbstractTagValue instance from raw user input.

        Args:
            value_input: Data that should be stored, used for determining the type.
            id3_key: Key that the data will be stored for.
                If sending in a path to an image, id3_key __must__ be set to "APIC",
                otherwise it will be interpreted as a string.
            join_character: Character used to join multiple values in string displays
            change_signal: Signal that should be linked to updating the join character
                in created TagValue object.
            parent: Owns the created object. When it is deleted, the created object
                will be too.

        Returns None if the value input is not a known format
        or if a precise format can't be determined.

        Falls back to using the id3 key if sent, to determine which type should be used.
        """
        match value_input:
            case str() as value:
                if id3_key == "APIC":
                    path = Path(value)
                    result = TagValueFactory._generateApicValue(path, parent)
                else:
                    result = TextTagValue([value], parent)
            case Path() as path:
                result = TagValueFactory._generateApicValue(path, parent)
            case _ if not value_input:
                result = TagValueFactory._generateFromEmptyValue(id3_key, parent)
            case list() as values:
                result = TagValueFactory._generateFromListValue(values, parent)
            case _:
                result = None

        return result
