"""Package for representing the values stored in an ID3 tag."""

from .abstract_tag_value import AbstractTagValue
from .paired_text_tag_value import PairedTextTagValue
from .picture_tag_value import PictureTagValue
from .tag_value_factory import TagValueFactory
from .text_tag_value import TextTagValue

__all__ = [
    "AbstractTagValue",
    "PairedTextTagValue",
    "PictureTagValue",
    "TagValueFactory",
    "TextTagValue",
]
