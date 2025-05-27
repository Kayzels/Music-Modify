import logging
import os

from mutagen.id3 import ID3

from music_modify.prefs import prefs

from .utils import valueToString

logger = logging.getLogger(__name__)


class Song:
    """Object representing data about an mp3 file"""

    def __init__(self, file: str | os.PathLike[str]):
        self.file: str | os.PathLike[str] = file
        self.id3: ID3 = ID3(file)
        self.display_info: list[str] = self._generateColumns()

    def _generateColumns(self) -> list[str]:
        info: list[str] = []
        for column in prefs.settings.table_tags:
            data_string: str
            try:
                data_string = valueToString(
                    column.getValue(self.id3), prefs.settings.split_values_display
                )
            except KeyError:
                logger.info(f"{self.id3} wasn't a key in the song.")
                data_string = ""
            info.append(data_string)
        return info

    def updateInfo(self):
        self.display_info = self._generateColumns()

    def save(self):
        self.id3.save(v2_version=4)
        self.updateInfo()
