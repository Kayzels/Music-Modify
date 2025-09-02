"""Module that defines a `SongTag` object, which is used to represent an ID3 tag."""

import logging
from typing import ClassVar, Final, cast, override

from mutagen import id3
from mutagen.id3 import ID3, Frames

from .aliases import (
    SongEditData,
    SongGroupData,
    SongLineData,
    SongListData,
    SongTableData,
)
from .enums import EditorType, TagType

logger = logging.getLogger(__name__)


class SongTag:
    """Object representing an ID3 tag."""

    KEYS_ALLOW_MULTIPLE_VALUES: ClassVar[set[str]] = {
        "TPE1",  # Artist
        "TPE2",  # Album Artist
        "TCOM",  # Composer
        "TCON",  # Content Type (Genres)
        "TENC",  # Encoder
        "TEXT",  # Lyricist
        "TKWD",  # Keywords
        "TMOO",  # Mood
        "TOLY",  # Original Lyricist
        "TPE4",  # Interpreter/Remixer
    }
    """List of keys that store a list of strings,
    rather than a single value."""

    def __init__(
        self,
        *,
        display_name: str,
        id3_key: str,
        editor_type: EditorType = EditorType.Automatic,
    ) -> None:
        """Create a `SongTag` based on a display name and key.

        Args:
            display_name: The human-readable name for the tag
            id3_key: The field in an id3 object that this tag refers to
            editor_type: The kind of widget the data for this tag is displayed with
        """
        self._id3_key: Final[str] = id3_key
        self._display_name: Final[str] = display_name
        self._frame_type: Final[TagType] = SongTag._getFrameType(id3_key)
        self._editor_type: Final[EditorType] = SongTag._calculateEditorType(
            editor_type, id3_key
        )

    @override
    def __repr__(self) -> str:
        return f"SongTag(display_name='{self.display_name}', id3_key='{self.id3_key}')"

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SongTag):
            return False
        return (self.display_name == other.display_name) and (
            self.id3_key == other.id3_key
        )

    @override
    def __hash__(self) -> int:
        return hash((self.id3_key, self.display_name))

    @property
    def id3_key(self) -> str:
        """The string value used to know which frame is being referenced in a song."""
        return self._id3_key

    @property
    def display_name(self) -> str:
        """The display name for the specific tag."""
        return self._display_name

    @property
    def frame_type(self) -> TagType:
        """The kind of metadata that the tag will store."""
        return self._frame_type

    @staticmethod
    def _calculateEditorType(editor_type: EditorType, key: str) -> EditorType:
        if editor_type != EditorType.Automatic:
            return editor_type
        frame_type = SongTag._getFrameType(key)
        if frame_type == TagType.People:
            return EditorType.PeopleValue
        if key in SongTag.KEYS_ALLOW_MULTIPLE_VALUES:
            return EditorType.MultipleText
        return EditorType.SingleText

    @staticmethod
    def _getFrameType(id3_key: str) -> TagType:
        """Determines the list name of the type of data that is stored in the tag.

        This is needed to extract the correct type of data from the tag later.
        """
        if "TXXX" in id3_key:
            tag_frame = id3.TXXX.__base__
        else:
            try:
                tag_frame = getattr(id3, id3_key).__base__
            except AttributeError:
                return TagType.Text
        match tag_frame:
            case id3.PairedTextFrame:
                return TagType.People
            case id3.UrlFrame | id3.UrlFrameU:
                return TagType.Url
            case id3.BinaryFrame:
                return TagType.Data
            case _:
                return TagType.Text

    def __len__(self) -> int:
        """Returns the general number of items this tag can store.

        Returns 1 if strings will be returned.
        Returns 2 if the format is [role, person]
        """
        return 2 if self.frame_type == TagType.People else 1

    def getTag(self, song: ID3) -> SongGroupData:
        """Gets the current data for this tag in the song sent in.

        Returns None if tag is not in song, or empty.

        Returns a list of strings if the format is a single string, like for the title,
        or if it is a list of values, like for the composer

        Returns a list of pairs of strings if the format is a group of pairs,
        like for the involved people list.
        """
        try:
            # NOTE: Done like this because the frame type changes,
            # and there is no quick way to directly extract the right type.
            # The result of song[self.id3_key] looks like
            # [TRCK(encoding=<Encoding.LATIN1: 0>, text=['1/16'])]
            # The 'text' field there changes depending on the frame type.
            # The most common types are 'text', 'people', 'url', and 'data'.
            return getattr(song[self.id3_key], self.frame_type.value)
        except KeyError:
            # Happens if trying to get a key from a song that doesn't have it.
            # For example, if a song hasn't got a composer (TCOM) set,
            # this will happen.
            logger.debug(f"KeyError from song for id3_key {self.id3_key}")
            return None

    @property
    def editor_type(self) -> EditorType:
        """Stores the kind of widget that should be used for editing the values."""
        return self._editor_type

    def setTag(self, song: ID3, values: SongGroupData) -> None:
        """Sets the tag for this song to contain the values that are sent."""
        if not self.hasTag(song):
            self.generateFrame(song)
        setattr(song[self.id3_key], self.frame_type.value, values)

    def hasTag(self, song: ID3) -> bool:
        """Checks whether the existing tag object is in the ID3 song."""
        return self.id3_key in song

    def removeTag(self, song: ID3) -> None:
        """Removes the SongTag object(s) with this name from the ID3 file."""
        song.delall(self.id3_key)

    def generateFrame(self, song: ID3) -> None:
        """Creates a frame object of the SongTag in the ID3 file."""
        if self.hasTag(song):
            return
        encoding = id3.Encoding.UTF8
        if "TXXX" not in self.id3_key:
            # ? Checks if the tag is custom or not.
            frame = Frames[self.id3_key](encoding, [])
        else:
            # ? Custom tags work differently, taking in an extra param.
            # ? This param is desc, which is a description taken
            # ? from the tag name.
            desc = self.id3_key.split(":")[1]
            frame = Frames["TXXX"](encoding, desc=desc, text=[])
        song.add(frame)

    def getValue(self, song: ID3) -> SongEditData | None:
        """Returns the value for the tag in a format useful for editing.

        This is done based on the type.
        If it stores (role, person) values, it returns a list of list of strings.
        If it stores multiple values, a list of strings is returned.
        If it stores a single string, this string is returned.
        """
        song_data = self.getTag(song)
        if song_data is None:
            return None
        match self.editor_type:
            case EditorType.PeopleValue:
                return cast(SongTableData, song_data)
            case EditorType.MultipleText:
                return [str(val) for val in cast(SongListData, song_data)]
            case _:
                return str(cast(SongLineData, song_data)[0])
