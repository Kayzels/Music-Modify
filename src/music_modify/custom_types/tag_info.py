"""Module that stores the `TagInfo` dataclass that represents
basic information about a tag, before it is converted to a `SongTag`."""

from dataclasses import dataclass


@dataclass
class TagInfo:
    """Basic tag information, used when construcing a `SongTag` object,
    and in places where only basic data is needed."""

    id3_key: str
    "The string value for the frame that should be accessed for a song."
    display_name: str
    "The display name for the id3_key, in human-readable form."
    show_in_table: bool = False
    "Whether the tag should appear in the main files table, or not."
