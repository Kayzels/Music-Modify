"""Module that defines a `SongRepository` object.

This works as a way of interacting with the list of songs.
"""

from collections.abc import Sequence
from os import PathLike

from PySide6.QtCore import QObject, Signal

from music_modify.custom_types import Song


class SongRepository(QObject):
    """Wrapper around a list of songs.

    Allows easier management for adding and removing songs.
    """

    songs_updated: Signal = Signal()
    "Signal that is emitted whenever songs are added or removed."

    def __init__(self) -> None:
        """Create a `SongRepository`, with no songs added yet."""
        super().__init__()
        self._songs: list[Song] = []

    def __getitem__(self, index: int) -> Song:
        """Returns the song at the index.

        Raises:
            IndexError if the index isn't valid.
        """
        try:
            return self._songs[index]
        except IndexError as err:
            raise IndexError from err

    def __len__(self) -> int:
        """Returns the number of songs in the repository."""
        return len(self._songs)

    def __contains__(self, new_song: Song | str | PathLike[str]) -> bool:
        """Returns True if a song with that file path already exists in the repo."""
        if isinstance(new_song, Song):
            file_matches = any(
                song.file == new_song.file and new_song.file is not None
                for song in self._songs
            )
            song_matches = new_song in self._songs
            return file_matches or song_matches
        return any(song.file == new_song for song in self._songs)

    def add(
        self,
        new: Song
        | str
        | PathLike[str]
        | Sequence[str | PathLike[str] | Song]
        | None = None,
    ) -> None:
        """Adds a Song to the list of songs, if not already present.

        If passed in a list of file paths, adds all the files that aren't present.
        """
        if isinstance(new, Sequence) and not isinstance(new, str):
            for file in new:
                self.add(file)
            return
        if isinstance(new, Song):
            if new not in self:
                self._songs.append(new)
                self.songs_updated.emit()
            return
        if new is not None and new in self:
            return
        song = Song(
            file=new,
        )
        self._songs.append(song)
        self.songs_updated.emit()

    def clear(self) -> None:
        """Remove all songs from the repository."""
        self._songs.clear()
        self.songs_updated.emit()

    def removeAtIndexes(self, indexes: list[int]) -> None:
        """Remove the songs at the specific indexes from the repository."""
        if not indexes:
            return
        # NOTE: Sort the indexes and make sure they're reversed,
        # to avoid shifting indexes when deleting
        indexes = sorted(indexes, reverse=True)
        for index in indexes:
            self._songs.pop(index)
        self.songs_updated.emit()

    def refreshDisplay(self) -> None:
        """Updates the information being displayed for each song in the repository.

        Should be called after any metadata is updated, to keep the view in sync.
        """
        # TODO: Is this function needed?
