"""Module for song objects representing data about an mp3 file.
    """
from typing import cast, List, Union

from mutagen.id3 import ID3

from songs.songtag import SongTag
from prefs import settings


class Song ():
    """Object representing data about an mp3 file
        """
    def __init__(self, file: str):
        """Constructor for Song object.

            Parameters
            ----------
            file : str -
                The music file to work on.

            Extended
            --------
            Contains data for the table model,
                and info that is needed for editing\n
            Creates an ID3 version of the file and stores for later.
            """
        self._file = file
        self.id3 = ID3(file)
        self.display_info = self._generate_columns()

    def _generate_columns(self) -> List[str]:
        """Creates the data for the table model as a list.

            Returns
            -------
            List[str] -
                List of the current data stored in the file,
                uses "-" if empty, to keep same length.
            """
        info = []
        display_split = settings.split_values_display
        column: SongTag
        for column in settings.files_tags:
            data_string = ''
            current_data: Union[List[str], List[List[str]], None]
            try:
                current_data = column.get_tag(self.id3)
                if current_data in [[], None]:
                    data_string = "-"
                elif column.value_length == 1:
                    current_data = cast(List[str], current_data)
                    try:
                        data_string = display_split.join(current_data)
                    except TypeError:
                        data_string = "-"
                elif column.value_length == 2:
                    current_data = cast(List[List[str]], current_data)
                    tag_values = []
                    for value in current_data:
                        if len(value) == 2:
                            tag_values.append(f"{value[0]}:{value[1]}")
                        else:
                            print(f"Value has invalid length: f{value}")
                            continue
                    data_string = display_split.join(tag_values)
            except KeyError:
                data_string = "-"
            info.append(data_string)
        return info

    def save(self):
        """Save the changes to the ID3 file.
            """
        self.id3.save(v2_version=4)
        self.display_info = self._generate_columns()
