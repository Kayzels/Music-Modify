"""Module that defines the `Song` object.

Manages the metadata for an mp3 file.
"""

import logging
import os
from typing import cast

from mutagen import MutagenError, id3
from mutagen.id3 import ID3

from .tag_value import AbstractTagValue, TagValueFactory

logger = logging.getLogger(__name__)


class Song:
    """Object representing data about an mp3 file."""

    def __init__(
        self,
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
        self._filepath: str | os.PathLike[str] | None = file

        self._staged_changes: dict[str, AbstractTagValue | None] = {}
        "Changes that should be made to the ID3 values when saving."
        self._loaded_values: dict[str, AbstractTagValue] = {}
        "Values that are read from the ID3 object."

        self._id3: ID3 = ID3()

        if file is not None:
            self.load(file)

    @property
    def file(self) -> str | os.PathLike[str] | None:
        """The file on disk that this `Song` object represents."""
        return self._filepath

    def save(self) -> None:
        """Save the changed values for the song, and refresh the display."""
        for id3_key, tag_value in self._staged_changes.items():
            if tag_value is None:
                if id3_key in self._id3:
                    self._id3.delall(id3_key)
                if id3_key in self._loaded_values:
                    del self._loaded_values[id3_key]
            elif id3_key in self._id3:
                frame = tag_value.updateId3Frame(self._id3[id3_key])
                self._id3[id3_key] = frame
                self._loaded_values[id3_key] = tag_value
            else:
                frame = tag_value.toId3Frame(id3_key)
                self._id3.add(frame)
                self._loaded_values[id3_key] = tag_value

        self._staged_changes = {}

        if not self.file:
            logger.warning("No file path defined for saving.")
            return

        try:
            self._id3.save(self.file)
            logger.debug(f"Tags saved successfully to '{self.file}'.")
        except MutagenError:
            logger.exception(f"Error saving ID3 tags to '{self.file}'.")
            return

    def load(self, file: str | os.PathLike[str]) -> None:
        """Load the metadata from this specific file."""
        self._filepath = file
        self._staged_changes.clear()
        self._loaded_values.clear()
        try:
            self._id3.load(file)
        except MutagenError:
            logger.exception(
                f"Error loading '{file}' for mutagen. Initializing with empty tags."
            )
            self._filepath = None
            self._id3 = ID3()

        for id3_key, frame in self._id3.items():
            id3_key = cast(str, id3_key)
            frame = cast(id3.Frame, frame)
            tag_value: AbstractTagValue | None = TagValueFactory.fromId3Frame(frame)
            if tag_value:
                self._loaded_values[id3_key] = tag_value

    def setTag(self, id3_key: str, value: AbstractTagValue | None) -> None:
        """Stages a change for a tag.

        If `value` is `None`, the tag will be removed on save.
        """
        self._staged_changes[id3_key] = value

    def getTag(self, id3_key: str) -> AbstractTagValue | None:
        """Return the value stored in the song for that specific tag.

        Prioritizes staged changes, then loaded/cached values.

        Returns `None`, if the tag is not present.
        """
        if id3_key in self._staged_changes:
            return self._staged_changes[id3_key]
        if id3_key in self._loaded_values:
            return self._loaded_values[id3_key]
        if id3_key in self._id3:
            frame = cast(id3.Frame, self._id3[id3_key])
            tag_value: AbstractTagValue | None = TagValueFactory.fromId3Frame(frame)
            if tag_value:
                self._loaded_values[id3_key] = tag_value
            return tag_value
        return None

    def removeTag(self, id3_key: str) -> None:
        """Marks a tag for removal when the song is saved."""
        self.setTag(id3_key, None)

    def hasTag(self, id3_key: str) -> bool:
        """Returns `True` if the tag is defined in the metadata for the song."""
        return id3_key in self.getAllTagKeys()

    def getAllTagKeys(self) -> list[str]:
        """Returns a list of all tag keys present, considering staged changes."""
        all_keys = set(self._loaded_values.keys())
        for key, value in self._staged_changes.items():
            if value is None:
                all_keys.discard(key)
            else:
                all_keys.add(key)
        return list(all_keys)

    def resetChanges(self, id3_key: str | None = None) -> None:
        """Removes a staged change for a given identifier.

        This will revert the value to its state when the file loaded,
        or make it non-existent if it was a new tag.

        Not passing in an `id3_key` will clear all changes.
        """
        if not id3_key:
            self._staged_changes.clear()
            return

        if id3_key in self._staged_changes:
            del self._staged_changes[id3_key]
            logger.debug(f"Staged changes for '{id3_key}' cleared.")
        else:
            logger.debug(f"No staged changes found for '{id3_key}'.")
