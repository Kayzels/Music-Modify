"""Module that defines the `Song` object.

Manages the metadata for an mp3 file.
"""

import logging
import os

from mutagen.id3 import ID3

from .aliases import SongEditData, SongGroupData
from .songtag import SongTag
from .utils import toTag, valueToString

logger = logging.getLogger(__name__)


class Song:
    """Object representing data about an mp3 file."""

    def __init__(
        self,
        all_tags: list[SongTag],
        table_tags: list[SongTag],
        display_split: str,
        file: str | os.PathLike[str] | None = None,
    ) -> None:
        """Creates a Song object from a provided file.

        If `file` is `None`, it creates an empty ID3 that is not related
        to any specific file.

        Args:
            all_tags: The tags that should be accessible and updateable.
            table_tags: The tags that should be used for generating columns.
            display_split: The character used for splitting values when they
                store multiple items.
            file: The file that the metadata should be loaded from.
        """
        self._all_tags: list[SongTag] = all_tags
        self._table_tags: list[SongTag] = table_tags
        self._display_split: str = display_split
        self.file: str | os.PathLike[str] | None = file
        "The file on disk that this `Song` object represents."
        self.id3: ID3 = ID3()
        "The metadata structure and values stored in the song."
        if file is not None:
            self.load(file)
        self.display_info: list[str]
        "The displayed values for the tags that are present in the song."
        self.updateInfo()

    def _generateColumns(self) -> list[str]:
        """Generate display values for the columns that should be shown in the table."""
        info: list[str] = []
        for column in self._table_tags:
            data_string = valueToString(
                value=self.getValue(column), display_split=self._display_split
            )
            info.append(data_string)
        return info

    def updateInfo(self) -> None:
        """Update the displayed values.

        Ensures the values are in sync with what is stored in the file.
        """
        self.display_info = self._generateColumns()

    def save(self) -> None:
        """Save the changed values for the song, and refresh the display."""
        if self.file is not None:
            self.id3.save(v2_version=4)
        self.updateInfo()

    def load(self, file: str | os.PathLike[str]) -> None:
        """Load the metadata from this specific file."""
        self.file = file
        self.id3.load(file)
        self.updateInfo()

    def setTag(self, tag: str | SongTag, value: SongGroupData) -> None:
        """Set the tag within the file to have the value specified."""
        found_tag = toTag(tag, self._all_tags) if not isinstance(tag, SongTag) else tag
        if found_tag is not None:
            found_tag.setTag(self.id3, value)

    def getValue(self, tag: str | SongTag) -> SongEditData | None:
        """Return the value stored in the song for that specific tag.

        Returns `None`, if the tag is not present.
        """
        found_tag = toTag(tag, self._all_tags) if not isinstance(tag, SongTag) else tag
        if found_tag is None:
            return None
        return found_tag.getValue(self.id3)

    def removeTag(self, tag: str | SongTag) -> None:
        """Remove the tag from the stored metadata for a song, if it exists."""
        found_tag = toTag(tag, self._all_tags) if not isinstance(tag, SongTag) else tag
        if found_tag is None:
            return
        found_tag.removeTag(self.id3)

    def hasTag(self, tag: str | SongTag) -> bool:
        """Returns `True` if the tag is defined in the metadata for the song."""
        found_tag = toTag(tag, self._all_tags) if not isinstance(tag, SongTag) else tag
        if found_tag is None:
            return False
        return found_tag.hasTag(self.id3)
