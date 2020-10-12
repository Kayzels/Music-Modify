"""Module for objects representing the tags saved in an ID3 file.
    """
from typing import List, Union
from dataclasses import dataclass

from mutagen import id3
from mutagen.id3 import Frames, ID3


def determine_list_name(tag: str) -> str:
    """Depending on the tag, sends the list name of the type of
        data that is stored.

        Parameters
        ----------
        tag : str -
            id3 tag frame value

        Returns
        -------
        str -
            name of the type of data. One of 'text, people, data or url'
        """
    if tag is None:
        return ''
    if 'TXXX' in tag:
        tag_frame = getattr(id3, 'TXXX').__base__
    else:
        try:
            tag_frame = getattr(id3, tag).__base__
        except AttributeError:
            return 'text'
    if tag_frame == id3.PairedTextFrame:
        return 'people'
    elif tag_frame == id3.BinaryFrame:
        return 'data'
    elif tag_frame == id3.UrlFrameU or tag_frame == id3.UrlFrame:
        return 'url'
    else:
        return 'text'


class SongTag:
    """Object representing an ID3 tag
        """
    def __init__(self, name: str, display_name: str):
        """Constructor for SongTag

            Parameters
            ----------
            name : str -
                ID3 tag name\n
            display_name : str -
                name shown for the tag
            """
        self.name = name
        self.list_name = determine_list_name(name)
        # ? type of data stored
        self.display_name = display_name
        self.value_length = self.determine_value_length()
        # ? int indicating whether list will contain str (1) or list (2)

    def determine_value_length(self) -> int:
        """Determines the length of the values that will be returned.

        Returns
        -------
        int -\n
        Returns 1 if strings will be returned.\n
        Returns 2 if the format is [role, person].
        """
        if self.list_name == 'people':
            return 2
        else:
            return 1

    def get_tag(self, song: ID3) -> Union[List[str],
                                          List[List[str]],
                                          None]:
        """Gets the current data for this tag in the sent song.

        Parameters
        ----------
        song : ID3 -
            song containing ID3 data

        Returns
        -------
        Union[List[str], List[List[str]], None] -
            returns the data which is present for this tag,
            considering the data format.\n
        Returns None if tag not in song, or empty.
            """
        try:
            return getattr(song[self.name], self.list_name)
        except KeyError:
            return None
        except AttributeError:
            return None

    def set_tag(self, song: ID3, values: Union[List,
                                               List[str],
                                               List[List[str]]]):
        """Sets the tag for this song to contain the values that are sent.

            Parameters
            ----------
            song : ID3 -
                Song where the values should be set.\n
            values : Union[List, List[str], List[List[str]]] -
                Values to be set - list type depends on data type of tag.
            """
        if not self.has_tag(song):
            self.generate_frame(song)
        setattr(song[self.name], self.list_name, values)

    def has_tag(self, song: ID3) -> bool:
        """Checks whether the existing tag object is in the ID3 song.

            Parameters
            ----------
            song : ID3 -
                Song that is being checked

            Returns
            -------
            bool -
                Whether the tag exists or not
            """
        return self.name in song

    def remove_tag(self, song: ID3):
        """Removes the SongTag object(s) wuth this name from the ID3 file.

            Args:
                song (ID3): ID3 file where the tag should be removed
            """
        song.delall(self.name)

    def generate_frame(self, song: ID3):
        """Creates a frame object of the songtag in the ID3 file sent.

            Parameters
            ----------
            song : ID3 -
                Song where the frame object should be created.
            """
        if self.has_tag(song):
            return
        encoding = id3.Encoding.UTF8
        frame: Frames
        try:
            if 'TXXX' not in self.name:
                # ? Checks if the tag is custom or not.
                frame = Frames[self.name](encoding, [])
            else:
                # ? Custom tags work differently, taking in an extra param.
                # ?This param is desc, which is a description taken
                # ? from the tag name.
                desc = self.name.split(':')[1]
                frame = Frames['TXXX'](encoding, desc=desc, text=[])
            song.add(frame)
        except TypeError:
            # ? Cannot create a tag frame with this key.
            print("Tag Name: " + str(self.name))


@dataclass
class SelectedTag():
    """A Dataclass to represent tag selection.
        """
    tag: Union[SongTag, None] = None
    copy_tag: Union[SongTag, None] = None
    role: Union[str, None] = None
