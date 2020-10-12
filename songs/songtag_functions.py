"""Functions related to SongTags.
   """
# ? Separate from SongTag module due to import cycles
from typing import Union

from prefs import settings
from songs.songtag import SongTag


def map_tag(display_name: str) -> Union[SongTag, None]:
    """When given a display_name, determines which tag it refers to.
        If the tag doesn't exist, returns None.

        Parameters
        ----------
        display_name : str -
            Displayed Name for tag.

        Returns
        -------
        Union[SongTag, None] -
            Returns SongTag if in all tags, else None.
        """
    tag_name = None
    for tag_pair in settings.all_tags_list:
        if display_name == tag_pair[0]:
            tag_name = tag_pair[1]
            break
    if tag_name is None:
        tag = None
    else:
        tag = SongTag(display_name, tag_name)
    return tag


def map_optional_tag(tag_name: str,
                     optional_name: str) -> Union[SongTag, None]:
    """Gets the tag from the given tag name. If the tag is None,
        gets the tag from the optional name.

        Parameters
        ----------
        tag_name : str -
            Display name of the tag to get\n
        optional_name : str -
            Display name of the tag to get if the original tag doesn't exist

        Returns
        -------
        Union[SongTag, None] -
            Returns the SongTag with one of the names if it exists, else None.
        """
    tag = map_tag(tag_name)
    if tag is None:
        tag = map_tag(optional_name)
    return tag
