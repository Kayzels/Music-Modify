from music_modify.custom_types import SongTag
from music_modify.prefs import prefs


def mapTag(display_name: str) -> SongTag | None:
    """When given a display_name, determines which tag it refers to.
    If the tag doesn't exist, returns None."""
    found_tag = list(
        filter(lambda tag: tag._display_name == display_name, prefs.settings.all_tags)
    )
    if len(found_tag) != 1:
        return None
    return found_tag[0]


def mapKey(id3_key: str) -> SongTag | None:
    """When given an id3_key, determined which tag it refers to.
    If the tag doesn't exist, return None."""
    found_tag = list(
        filter(lambda tag: tag.id3_key == id3_key, prefs.settings.all_tags)
    )
    if len(found_tag) != 1:
        return None
    return found_tag[0]


def mapOptionalTag(tag_name: str, optional_name: str) -> SongTag | None:
    """Gets the tag from the given tag name.
    If the tag is None, gets the tag from the optional name.

    Args:
    -----
    tag_name: str - Display name of the tag to get
    optional_name: str - Display name of the tag to get if the original tag doesn't exist
    """
    tag = mapTag(tag_name)
    if tag is None:
        tag = mapTag(optional_name)
    return tag
