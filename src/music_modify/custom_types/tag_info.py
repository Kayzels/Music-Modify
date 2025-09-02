"""Module that stores the `TagInfo` dataclass.

This dataclass represents basic information about a tag,
before it is converted to a `SongTag`.
"""

from dataclasses import KW_ONLY, dataclass

from .enums import EditorType


@dataclass
class TagInfo:
    """Basic tag information.

    Used when constructing a `SongTag` object,
    and in places where only basic data is needed.
    """

    _: KW_ONLY
    id3_key: str
    "The string value for the frame that should be accessed for a song."
    display_name: str
    "The display name for the id3_key, in human-readable form."
    show_in_table: bool = False
    "Whether the tag should appear in the main files table, or not."
    editor_type: EditorType = EditorType.Automatic
    "The type of widget/display that should be used for editing a tag."
