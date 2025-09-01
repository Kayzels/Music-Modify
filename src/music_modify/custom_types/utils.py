"""Utility module for SongTags specifically.

Not part of the general utils, as that leads to an import cycle.
"""

import logging
from typing import cast

from music_modify.custom_types import constants

from .aliases import SongEditData, SongListData, SongTableData
from .songtag import SongTag

logger = logging.getLogger(__name__)


def mapTag(display_name: str, tag_list: list[SongTag]) -> SongTag | None:
    """When given a display_name, determines which tag it refers to.

    If the tag doesn't exist, returns None.
    """
    found_tag = list(filter(lambda tag: tag.display_name == display_name, tag_list))
    if len(found_tag) != 1:
        return None
    return found_tag[0]


def mapKey(id3_key: str, tag_list: list[SongTag]) -> SongTag | None:
    """When given an id3_key, determined which tag it refers to.

    If the tag doesn't exist, return None.
    """
    found_tag = list(filter(lambda tag: tag.id3_key == id3_key, tag_list))
    if len(found_tag) != 1:
        return None
    return found_tag[0]


def mapOptionalTag(
    tag_name: str,
    optional_name: str,
    tag_list: list[SongTag],
) -> SongTag | None:
    """Gets the tag from the given tag name.

    If the tag is None, gets the tag from the optional name.

    Args:
        tag_name: Display name of the tag to get
        optional_name: Display name of the tag to get if the original tag
            doesn't exist
        tag_list: The list of tags to check for the names.
    """
    tag = mapTag(tag_name, tag_list)
    if tag is None:
        tag = mapTag(optional_name, tag_list)
    return tag


def valueToString(value: SongEditData | None, display_split: str) -> str:
    """Converts data from a specific tag into a string representation.

    Uses `display_split` as the separator if there are multiple values,
    when `value` is a list.
    """
    if value is None or len(value) == 0:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value[0], str):
        value = cast(SongListData, value)
        return display_split.join(value)
    value = cast(SongTableData, value)
    tag_values: list[str] = []
    for group in value:
        if len(group) == constants.PEOPLE_COL_COUNT:
            tag_values.append(f"{group[0]}:{group[1]}")
        else:
            logger.warning(f"Song column has an invalid length: {group}")
            continue
    return display_split.join(tag_values)


def toTag(tag: str | SongTag, tag_list: list[SongTag]) -> SongTag | None:
    """Generate a SongTag from a string.

    First searches for the id3 key, and then the display name.
    If it cannot be found, returns None.

    If the tag isn't in tag_list, it's not a tag we manage,
    so None is returned.
    """
    if isinstance(tag, SongTag):
        if tag in tag_list:
            return tag
        return None
    result = mapKey(tag, tag_list)
    if result is None:
        result = mapTag(tag, tag_list)
    return result
