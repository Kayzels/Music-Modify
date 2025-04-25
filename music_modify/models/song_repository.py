from os import PathLike

from PySide6.QtCore import QObject, Signal

from music_modify.custom_types import Song


class SongRepository(QObject):
    songs_updated: Signal = Signal()

    def __init__(self):
        super().__init__()
        self._songs: list[Song] = []

    def getSongs(self):
        return self._songs

    def __len__(self):
        return len(self._songs)

    def addFile(self, file: str | PathLike[str]):
        if not any(song.file == file for song in self._songs):
            self._songs.append(Song(file))
            self.songs_updated.emit()

    def addFiles(self, files: list[str] | list[PathLike[str]]):
        for file in files:
            self.addFile(file)

    def clearFiles(self):
        self._songs.clear()
        self.songs_updated.emit()

    def removeSongs(self, indexes: list[int]):
        if not indexes:
            return
        # NOTE: Sort the indexes and make sure they're reversed,
        # to avoid shifting indexes when deleting
        indexes = sorted(indexes, reverse=True)
        for index in indexes:
            self._songs.pop(index)
        self.songs_updated.emit()

    def refreshDisplay(self):
        for song in self._songs:
            song.updateInfo()
