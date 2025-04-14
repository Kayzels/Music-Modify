# pyright: reportPrivateImportUsage=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportUnknownMemberType=false

from typing import Final
from mutagen import id3
from mutagen.id3 import Frames, ID3

from music_modify.types.enums import TagType


class SongTag:
    """Object representing an ID3 tag"""

    def __init__(self, display_name: str, id3_key: str):
        self._id3_key: Final[str] = display_name
        self._display_name: Final[str] = display_name
        self._frame_type: Final[TagType] = SongTag.get_frame_type(display_name)

    @property
    def id3_key(self) -> str:
        return self._id3_key

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def frame_type(self) -> TagType:
        return self._frame_type

    @staticmethod
    def get_frame_type(tag_name: str) -> TagType:
        """Depending on the tag, determines the list name of the type of
        data that is stored."""
        if "TXXX" in tag_name:
            tag_frame = getattr(id3, "TXXX").__base__
        else:
            try:
                tag_frame = getattr(id3, tag_name).__base__
            except AttributeError:
                return TagType.Text
        if tag_frame == id3.PairedTextFrame:
            return TagType.People
        elif tag_frame in (id3.UrlFrame, id3.UrlFrameU):
            return TagType.Url
        return TagType.Text

    def __len__(self) -> int:
        """Returns 1 if strings will be returned.
        Returns 2 if the format is [role, person]"""
        return 2 if self.frame_type == TagType.People else 1

    def get_tag(self, song: ID3) -> list[str] | list[list[str]] | None:
        """Gets the current data for this tag in the sent song.
        Returns None if tag is not in song, or empty."""
        try:
            return getattr(song[self.id3_key], self.frame_type.value)
        except KeyError:
            return None
        except AttributeError:
            return None

    def set_tag(self, song: ID3, values: list[str] | list[list[str]]) -> None:
        """Sets the tag for this song to contain the values that are sent."""
        if not self.has_tag(song):
            self.generate_frame(song)
        setattr(song[self.id3_key], self.frame_type.value, values)

    def has_tag(self, song: ID3) -> bool:
        """Checks whether the existing tag object is in the ID3 song."""
        return self.id3_key in song

    def remove_tag(self, song: ID3) -> None:
        """Removes the SongTag object(s) with this name from the ID3 file."""
        song.delall(self.id3_key)

    def generate_frame(self, song: ID3) -> None:
        """Creates a frame object of the SongTag in the ID3 file."""
        if self.has_tag(song):
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
            print(f"Tag Name: {self.id3_key}")
