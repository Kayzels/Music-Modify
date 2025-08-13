"""Module that defines a `SongTag` object,
which is used to represent an ID3 tag."""

import logging
from typing import Final, cast, override

from mutagen import id3
from mutagen.id3 import ID3, Frames

from .aliases import (
    SongEditData,
    SongGroupData,
    SongLineData,
    SongListData,
    SongTableData,
)
from .enums import TagType

logger = logging.getLogger(__name__)


class SongTag:
    """Object representing an ID3 tag"""

    KEYS_ALLOW_MULTIPLE_VALUES: set[str] = {
        "TCOM",  # Composer
        "TCON",  # Content Type (Genres)
        "TENC",  # Encoder
        "TEXT",  # Lyricist
        "TKWD",  # Keywords
        "TMOO",  # Mood
        "TOLY",  # Original Lyricist
        "TPE4",  # Interpreter/Remixer
    }
    """Hardcoded list of keys that store a list of strings,
    rather than a single value."""

    def __init__(self, display_name: str, id3_key: str) -> None:
        self._id3_key: Final[str] = id3_key
        self._display_name: Final[str] = display_name
        self._frame_type: Final[TagType] = SongTag._getFrameType(id3_key)

    @override
    def __repr__(self) -> str:
        return f"SongTag({self.id3_key}, {self.display_name})"

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SongTag):
            return False
        return (self.display_name == other.display_name) and (
            self.id3_key == other.id3_key
        )

    @property
    def id3_key(self) -> str:
        """The string value used to know which frame is being referenced
        in a song."""
        return self._id3_key

    @property
    def display_name(self) -> str:
        """The display name for the specific tag."""
        return self._display_name

    @property
    def frame_type(self) -> TagType:
        """The kind of metadata that the tag will store."""
        return self._frame_type

    @property
    def allow_multiple(self) -> bool:
        """Whether this specific tag stores a list of values (`True`),
        or a single value (`False`)."""
        # TODO: Consider whether people tags should return True here.
        return self.id3_key in SongTag.KEYS_ALLOW_MULTIPLE_VALUES

    @staticmethod
    def _getFrameType(id3_key: str) -> TagType:
        """Depending on the tag, determines the list name of the type of
        data that is stored.
        This is needed to extract the correct type of data from the tag later."""
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
        """Returns 1 if strings will be returned.
        Returns 2 if the format is [role, person]"""
        return 2 if self.frame_type == TagType.People else 1

    def getTag(self, song: ID3) -> SongGroupData:
        """Gets the current data for this tag in the song sent in.
        Returns None if tag is not in song, or empty.
        Returns a list of strings if the format is a single string, like for the title,
        or if it is a list of values, like for the composer
        Returns a list of pairs of strings if the format is a group of pairs,
        like for the involved people list."""
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
        except AttributeError:
            # Shouldn't happen: means trying to get the wrong frame type.
            logger.warning(
                (
                    f"AttributeError when accessing frame type {self.frame_type}"
                    f" from song for id3_key {self.id3_key}"
                ),
            )
            return None

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
        try:
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
        except TypeError:
            # ? Cannot create a tag frame with this key
            logger.warning(f"Cannot create a tag frame with this key: {self.id3_key}")

    def getValue(self, song: ID3) -> SongEditData | None:
        """Returns the value for the tag in the format useful for editing,
        based on the type.
        """
        song_data = self.getTag(song)
        if song_data is None:
            return None
        match self.frame_type:
            case TagType.People:
                song_data = cast(SongTableData, song_data)
                return song_data
            case _:
                # noinspection PyTypeHints
                song_data = cast(SongLineData | SongListData, song_data)
                if self.allow_multiple:
                    return [str(val) for val in song_data]
                else:
                    return str(song_data[0])
