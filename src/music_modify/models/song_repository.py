"""Module that defines a `SongRepository` object, which works as a way of interacting
with the list of songs."""

from os import PathLike

from PySide6.QtCore import QObject, Signal

from music_modify.custom_types import Song


class SongRepository(QObject):
    """Wrapper around a list of songs, that allows easier management
    for adding and removing songs
    """

    songs_updated: Signal = Signal()
    "Signal that is emitted whenever songs are added or removed."

    def __init__(self):
        super().__init__()
        self._songs: list[Song] = []

    def getSongs(self):
        """Returns the list of songs the repository manages."""
        return self._songs

    def getSong(self, index: int) -> Song | None:
        """Gets the song at a specific index."""
        if index < 0 or index >= len(self._songs):
            return None
        return self._songs[index]

    def __getitem__(self, index: int) -> Song | None:
        return self.getSong(index)

    def __len__(self):
        return len(self._songs)

    def addFile(self, file: str | PathLike[str]):
        """Add file to the list of songs, if not already present."""
        if not any(song.file == file for song in self._songs):
            self._songs.append(Song(file))
            self.songs_updated.emit()

    def addFiles(self, files: list[str] | list[PathLike[str]]):
        """Adds the list of files to the repository."""
        for file in files:
            self.addFile(file)

    def clearFiles(self):
        """Remove all songs from the repository."""
        self._songs.clear()
        self.songs_updated.emit()

    def removeSongs(self, indexes: list[int]):
        """Remove the songs at the specific indexes from the repository."""
        if not indexes:
            return
        # NOTE: Sort the indexes and make sure they're reversed,
        # to avoid shifting indexes when deleting
        indexes = sorted(indexes, reverse=True)
        for index in indexes:
            self._songs.pop(index)
        self.songs_updated.emit()

    def refreshDisplay(self):
        """Updates the information being displayed for each song in the repository.
        Should be called after any metadata is updated, to keep the view in sync.
        """
        for song in self._songs:
            song.updateInfo()
