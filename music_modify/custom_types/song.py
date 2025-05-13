# pyright: reportUnknownMemberType=false, reportPrivateImportUsage=false

import logging
import os
from typing import cast

from mutagen.id3 import ID3

from music_modify.custom_types.aliases import (
    SongGroupData,
    SongLineData,
    SongListData,
    SongTableData,
)
from music_modify.custom_types.enums import TagType
from music_modify.prefs import prefs

logger = logging.getLogger(__name__)


class Song:
    """Object representing data about an mp3 file"""

    def __init__(self, file: str | os.PathLike[str]):
        self.file: str | os.PathLike[str] = file
        self.id3: ID3 = ID3(file)
        self.display_info: list[str] = self._generateColumns()

    def _generateColumns(self) -> list[str]:
        info: list[str] = []
        display_split = prefs.settings.split_values_display
        for column in prefs.settings.table_tags:
            data_string = ""
            current_data: SongGroupData
            try:
                current_data = column.getTag(self.id3)
                if current_data in [[], None]:
                    data_string = ""
                elif column.frame_type != TagType.People:
                    # Single value or list of single values.
                    current_data = cast(SongLineData | SongListData, current_data)
                    try:
                        data_string = display_split.join(
                            [str(val) for val in current_data]
                        )
                    except TypeError:
                        data_string = ""
                        logger.warning(
                            f"TypeError when generating columns for {current_data} with type {type(current_data)}"
                        )
                else:
                    current_data = cast(SongTableData, current_data)
                    tag_values: list[str] = []
                    for value in current_data:
                        if len(value) == 2:
                            tag_values.append(f"{value[0]}:{value[1]}")
                        else:
                            logger.warning(
                                f"Song column value has an invalid length: {value}"
                            )
                            continue
                    data_string = display_split.join(tag_values)
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
