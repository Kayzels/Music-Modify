"""Module that defines a `SongRepository` object.

This works as a way of interacting with the list of songs.
"""

from os import PathLike

from PySide6.QtCore import QObject, Signal

from music_modify.custom_types import Song
from music_modify.custom_types.songtag import SongTag


class SongRepository(QObject):
    """Wrapper around a list of songs.

    Allows easier management for adding and removing songs.
    """

    songs_updated: Signal = Signal()
    "Signal that is emitted whenever songs are added or removed."

    def __init__(
        self, all_tags: list[SongTag], table_tags: list[SongTag], display_split: str
    ) -> None:
        """Create a `SongRepository`, with no songs added yet."""
        super().__init__()
        self._all_tags: list[SongTag] = all_tags
        self._table_tags: list[SongTag] = table_tags
        self._display_split: str = display_split
        self._songs: list[Song] = []

    def getSong(self, index: int) -> Song | None:
        """Gets the song at a specific index."""
        if index < 0 or index >= len(self._songs):
            return None
        return self._songs[index]

    def __getitem__(self, index: int) -> Song | None:
        """Returns the song at the index.

        Returns `None` if the index is invalid, rather than raising an IndexError.
        """
        return self.getSong(index)

    def __len__(self) -> int:
        """Returns the number of songs in the repository."""
        return len(self._songs)

    def __contains__(self, new_song: Song | str | PathLike[str]) -> bool:
        """Returns True if a song with that file path already exists in the repo."""
        if isinstance(new_song, Song):
            file_matches = any(song.file == new_song.file for song in self._songs)
            song_matches = new_song in self._songs
            return file_matches or song_matches
        return any(song.file == new_song for song in self._songs)

    def addFile(self, file: str | PathLike[str]) -> None:
        """Add file to the list of songs, if not already present."""
        if file not in self:
            self._songs.append(
                Song(self._all_tags, self._table_tags, self._display_split, file)
            )
            self.songs_updated.emit()

    def addFiles(self, files: list[str] | list[PathLike[str]]) -> None:
        """Adds the list of files to the repository."""
        for file in files:
            self.addFile(file)

    def addSong(self, song: Song | None = None) -> None:
        """Add the song to the repository, not necessarily linked to a file."""
        if song:
            self._songs.append(song)
        else:
            self._songs.append(
                Song(self._all_tags, self._table_tags, self._display_split)
            )
        self.songs_updated.emit()

    def clearFiles(self) -> None:
        """Remove all songs from the repository."""
        self._songs.clear()
        self.songs_updated.emit()

    def removeSongs(self, indexes: list[int]) -> None:
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
        for song in self._songs:
            song.updateInfo()
