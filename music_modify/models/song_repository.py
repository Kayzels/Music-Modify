from os import PathLike
from music_modify.custom_types import Song
from PySide6.QtCore import Signal, QObject


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
