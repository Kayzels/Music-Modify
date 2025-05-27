import logging
import os

from mutagen.id3 import ID3

from music_modify.prefs import prefs

from .aliases import SongEditData, SongGroupData
from .utils import toTag, valueToString
from .songtag import SongTag

logger = logging.getLogger(__name__)


class Song:
    """Object representing data about an mp3 file"""

    def __init__(self, file: str | os.PathLike[str] | None = None):
        self.file: str | os.PathLike[str] | None = file
        self.id3: ID3 = ID3()
        if file is not None:
            self.load(file)
        self.display_info: list[str] = self._generateColumns()

    def _generateColumns(self) -> list[str]:
        info: list[str] = []
        for column in prefs.settings.table_tags:
            data_string: str
            try:
                data_string = valueToString(
                    self.getValue(column), prefs.settings.split_values_display
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

    def load(self, file: str | os.PathLike[str]):
        self.file = file
        self.id3.load(file)

    def setTag(self, tag: str | SongTag, value: SongGroupData):
        found_tag = toTag(tag, prefs.settings.all_tags)
        if found_tag is not None:
            found_tag.setTag(self.id3, value)

    def getValue(self, tag: str | SongTag) -> SongEditData | None:
        found_tag = toTag(tag, prefs.settings.all_tags)
        if found_tag is None:
            return None
        return found_tag.getValue(self.id3)

    def removeTag(self, tag: str | SongTag) -> None:
        found_tag = toTag(tag, prefs.settings.all_tags)
        if found_tag is None:
            return
        found_tag.removeTag(self.id3)

    def hasTag(self, tag: str | SongTag) -> bool:
        found_tag = toTag(tag, prefs.settings.all_tags)
        if found_tag is None:
            return False
        return found_tag.hasTag(self.id3)
