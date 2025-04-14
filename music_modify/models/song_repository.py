from music_modify.custom_types import Song


class SongRepository:
    def __init__(self):
        self._songs: list[Song] = []

    def getSongs(self):
        return self._songs

    def __len__(self):
        return len(self._songs)
