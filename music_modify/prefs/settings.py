""" Settings file that imports from config to share across python files.
        Tags and the default string splits are created.
    """

import configparser
# from pathlib import Path
from typing import List, Tuple

from songs.songtag import SongTag
from utils import file_utils


config = configparser.ConfigParser()

config.read(file_utils.get_resource_path('config.ini'))
# config.read(Path("config.ini"))

# ? the symbol that entered text should split on:
split_text_entered = config['Split']['split_text_entered'] + ' '
# ? the symbol values displayed split on:
split_values_display = config['Split']['split_values_display']
# ? the symbol that current tag info should split on:
split_values_at = config['Split']['split_values_at'] + ' '


def create_tag_pairs(value_string: str) -> List[Tuple[str, str]]:
    """Creates a list of tag pairs

        Parameters
        ----------
        value_string : str -
            input string from config file of the form: display_name, tag_name\n

        Returns
        -------
        List[Tuple[str, str]] -
            tag pairs list of the form:
            [(display_name, tag_name), (display_name, tag_name)]
        """
    tag_list = []
    values = value_string.splitlines()
    for value in values:
        if value != '':
            display_name, tag_name = value.split(', ')
            tag = (display_name, tag_name)
            tag_list.append(tag)
    return tag_list


def create_tag(tag_list: Tuple[str, str]) -> SongTag:
    """Creates a SongTag from the tuple of tag info sent

        Parameters
        ----------
        tag_list : Tuple[str, str] -
            Info about tag, in the form: (display_name, tag_name)

        Returns
        -------
        SongTag -
            SongTag object for defined tag
        """
    display_name = tag_list[0]
    tag_name = tag_list[1]
    return SongTag(tag_name, display_name)


def create_tags_list(tag_list: List[Tuple[str, str]]) -> List[SongTag]:
    """Generates a list of SongTag objects from the sent list
        list of tag info.

        Parameters
        ----------
        tag_list : List[Tuple[str, str]] -
            List of tuples with format: (display_name, tag_name).

        Returns
        -------
        List[SongTag] -
            List of SongTag objects for the tags sent in.
        """
    tags = []
    for tag in tag_list:
        new_tag = create_tag(tag)
        tags.append(new_tag)
    return tags


def create_tags_general(values: str) -> Tuple[
        List[Tuple[str, str]], List[SongTag]]:
    """Performs both tag creation functions and returns as a tuple.

        Parameters
        ----------
        values : str -
            string from config file for specific tags group.

        Returns
        -------
        Tuple[ List[Tuple[str, str]], List[SongTag]] -
            Tag pairs List, Songtags List.
        """
    tag_list = create_tag_pairs(values)
    tags = create_tags_list(tag_list)
    return tag_list, tags


standard_tags_string = config['Tags']['standard_tags']
standard_tags_list, standard_tags = create_tags_general(standard_tags_string)

files_tag_string = config['Tags']['file_tags']
files_tags_list, files_tags = create_tags_general(files_tag_string)

custom_tags_string = config['Tags']['custom_tags']
custom_tags_list, custom_tags = create_tags_general(custom_tags_string)

all_tags_list = standard_tags_list + custom_tags_list
