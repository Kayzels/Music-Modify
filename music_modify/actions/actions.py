
"""Module for the possible actions that can be done on a music file.
    """
# region Python Imports
from collections import OrderedDict
import inspect
from pathlib import Path
from typing import Any, Callable, cast, Dict, List, Tuple, Union
# endregion
# region Custom Imports
import numpy as np
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
import requests
# endregion
# region Project Imports
from actions import download_discogs, download_lastfm
from models import SongTableProxyModel
from prefs import settings
from signals import ActionSignals, SubactionSignals
from songs import songtag_functions, SelectedTag, Song, SongTag
from utils.enums import ActionType, CopyType, InputWidget, UserRole,\
    ValuesTableType
from utils import file_utils
# endregion


# region Manual Actions
def add_tag(song: Song, tag: SongTag):
    """Add a non-existent tag to the tags in a song.

        Parameters
        ----------
        song : Song -
            Song that the tag should be added to\n
        tag : SongTag -
            Tag that should be added.
        """
    if not tag.has_tag(song.id3):
        tag.set_tag(song.id3, [])
        song.save()


def remove_tag(song: Song, tag: SongTag):
    """Remove all values a tag and then remove the tag from the song.

        Parameters
        ----------
        song : Song -
            Song that the tag should be removed from\n
        tag : SongTag -
            Tag that should be removed.
        """
    if tag.has_tag(song.id3):
        tag.remove_tag(song.id3)
        song.save()


def set_tag(song: Song,
            tag: SongTag,
            new_values: Union[List[str], List[List[str]], None]):
    """Sets the values of the given tag to the values sent.

        Parameters
        ----------
        song : Song -
            Song where the tag should be set\n
        tag : SongTag -
            Tag that should be set\n
        new_values : Union[List[str], List[List[str]], None] -
            Values that should be set.
        """
    if new_values is None:
        add_tag(song, tag)
        return
    tag.set_tag(song.id3, new_values)
    song.save()


def add_values(song: Song,
               tag: SongTag,
               new_values: Union[List[str], List[List[str]], None]):
    """Append values sent to the tag in the song.

        Parameters
        ----------
        song : Song -
            Song where the data should change\n
        tag : SongTag -
            The tag whose values should change\n
        new_values : Union[List[str], List[List[str]], None] -
            The values to be added
        """
    if new_values is None:
        add_tag(song, tag)
        return
    values = tag.get_tag(song.id3)
    if values is None:
        set_tag(song, tag, new_values)
        return
    values_copy = values.copy()
    for value in new_values:
        if value not in values:
            values_copy.append(value)  # type: ignore
    tag.set_tag(song.id3, values_copy)
    song.save()


def remove_values(song: Song,
                  tag: SongTag,
                  values_to_remove: Union[List[str], List[List[str]], None]):
    """Remove the given values from the tag for this song.

        Parameters
        ----------
        song : Song -
            Song to be edited\n
        tag : SongTag -
            Tag the values awill be removed from\n
        remove_values : Union[List[str], List[List[str]], None] -
            Values to be removed
        """
    if values_to_remove is None:
        return
    values = tag.get_tag(song.id3)
    if values is None:
        return
    values = values.copy()
    for value in values_to_remove:
        try:
            values.remove(value)  # type: ignore
        except ValueError:
            continue
    if len(values) > 0:
        tag.set_tag(song.id3, values)
    else:
        tag.remove_tag(song.id3)
    song.save()


def remove_duplicates(song: Song, tag: SongTag):
    """Remove duplicate values from a specific tag.

        Parameters
        ----------
        song : Song -
            Song to be edited\n
        tag : SongTag -
            Tag to be edited
        """
    values = tag.get_tag(song.id3)
    if values is None:
        return
    else:
        values = tuple([tuple(value)  # type: ignore
                       if isinstance(value, list)
                       else value
                       for value in values])
        new_list = [list(value)
                    if isinstance(value, tuple)
                    else value
                    for value in list(OrderedDict.fromkeys((values)))]
        tag.set_tag(song.id3, new_list)
        song.save()


def _split_value(value: str) -> List[str]:
    """Splits the string provided at the split value in settings.

        Parameters
        ----------
        value : str -
            The string that should be split

        Returns
        -------
        List[str]
            The string that has been split
        """
    split_string = settings.split_values_at
    if split_string not in value:
        return [value]
    else:
        return value.split(split_string)


def split_values(song: Song, tag: SongTag):
    """Split the values in a tag on the given string in settings.

        Parameters
        ----------
        song : Song -
            Song to be edited\n
        tag : SongTag -
            Tag where data should be split
        """
    values_to_set: Union[List, List[str], List[List[str]]] = []
    values = tag.get_tag(song.id3)
    if values is None:
        return
    for value in values:
        if tag.value_length == 1:
            values_to_set = cast(List[str], values_to_set)
            value = cast(str, value)
            values_split = _split_value(value)
            values_to_set.extend(values_split)
        else:
            values_to_set = cast(List[List[str]], values_to_set)
            value = cast(List[str], value)
            role, person = value
            split_roles = _split_value(role)
            split_people = _split_value(person)
            for split_role in split_roles:
                for split_person in split_people:
                    values_to_set.append([split_role, split_person])
    tag.set_tag(song.id3, values_to_set)
    song.save()


def _replace_value(values_copy: np.ndarray,
                   new_values: List[List[str]],
                   tag_length: int,
                   item_index: int,
                   item: str,
                   *,
                   index_of_pair: Union[int, None] = None,
                   pair: Union[List[str], None] = None
                   ):
    """Replace the specific value in the tag if the value is the same as
        the first index in the new_values list.

        Parameters
        ----------
        values_copy : np.ndarray -
            Array where the changed values are saved to\n
        new_values : List[List[str]] -
            List of the values that should be changed.
            Formatted as a list of lists, with the inner list being:
                [original_value(str), new_value(str)]\n
        tag_length : int -
            The nature of the way values are saved in a tag -
            whether the values are strings (1), or pairs(2) [role, person]\n
        item_index : int -
            The location of the current value being checked\n
        item : str -
            The current value being checked\n
        index_of_pair : Union[int, None], optional -
            Where the pair is in the original list, by default None\n
        pair : Union[List[str], None], optional -
            The values of the pair in the original list, by default None
        """
    if tag_length == 1:
        values_slice = np.s_[item_index]
    else:
        # ? create a slice to refer to the exact location in the
        # ? 2d array.
        index_in_pair = item_index
        values_slice = np.s_[index_of_pair, index_in_pair]
    for nv_index, item_pair in enumerate(new_values):
        old_value, new_value = item_pair
        if old_value == item:
            if nv_index == 0:
                values_copy[values_slice] = new_value
            else:
                # ? Get previous old value and check if the same.
                previous_value = new_values[nv_index - 1][0]
                if old_value != previous_value:
                    values_copy[values_slice] = new_value
                else:
                    if tag_length == 1:
                        np.append(values_copy, [new_value], 0)
                    elif tag_length == 2:
                        pair = cast(List[str], pair)
                        if item_index == 0:
                            new_pair = [new_value, pair[1]]
                        else:
                            new_pair = [pair[0], new_value]
                        np.append(values_copy, [new_pair], 0)


def replace_values(song: Song,
                   tag: SongTag,
                   new_values: Union[List[List[str]], None]):
    """Replace the values in the given tag if they match the strings in
        new values.

        Parameters
        ----------
        song : Song -
            Song to be edited\n
        tag : SongTag -
            Tag being edited\n
        new_values : Union[List[List[str]], None] -
            Values to change
        """
    if not new_values:
        return
    new_values = cast(List[List[str]], new_values)
    values = tag.get_tag(song.id3)
    if values is None:
        return
    values_copy = np.array(values)
    if tag.value_length == 1:
        values = cast(List[str], values)
        for index, item in enumerate(values):
            _replace_value(values_copy=values_copy,
                           new_values=new_values,
                           tag_length=tag.value_length,
                           item_index=index,
                           item=item)
    elif tag.value_length == 2:
        values = cast(List[List[str]], values)
        for index_of_pair, pair in enumerate(values):
            for index_in_pair, pair_item in enumerate(pair):
                _replace_value(values_copy=values_copy,
                               new_values=new_values,
                               tag_length=tag.value_length,
                               index_of_pair=index_of_pair,
                               pair=pair,
                               item_index=index_in_pair,
                               item=pair_item)
    values_copy = values_copy.tolist()
    tag.set_tag(song.id3, values_copy)
    song.save()


def copy_values(song: Song,
                tag_selection: SelectedTag,
                *,
                copy_mode: CopyType = CopyType.NotUsed,
                to_song: Union[Song, None] = None):
    """Copies values from one tag in a song to another, or across songs.

        Parameters
        ----------
        song : Song -
            Song that should be edited.\n
        tag_selection : SelectedTag -
            Which tag should send data, and which should receive\n
        copy_mode : CopyType, optional -
            Enum indicating whether data should be replaced or appended,
            and whether data is being sent within the same song, or to a
            different song.\n
        to_song : Union[Song, None], optional -
            Song data should be sent to. If None, uses the original song.
            By default None
        """
    if copy_mode & CopyType.Across:
        if to_song is None:
            return
    else:
        if to_song is None:
            to_song = song
    to_song = cast(Song, to_song)
    tag = tag_selection.tag
    copy_tag = tag_selection.copy_tag
    if tag is None or copy_tag is None:
        return
    tag = cast(SongTag, tag)
    copy_tag = cast(SongTag, copy_tag)
    role = tag_selection.role
    orig_copy_vals = copy_tag.get_tag(song.id3)
    if orig_copy_vals is None:
        return
    orig_copy_vals = cast(Union[List[str], List[List[str]]], orig_copy_vals)
    copy_vals: Union[List[str], List[List[str]], List]
    if role is not None:
        copy_vals = []
        copy_vals = cast(List[List[str]], copy_vals)
        for value in orig_copy_vals:
            value = cast(str, value)
            copy_vals.append([role, value])
    else:
        copy_vals = orig_copy_vals
    arguments: Tuple[Song, SongTag, Union[List[str], List[List[str]]]]
    arguments = (to_song, tag, copy_vals)
    if copy_mode & CopyType.Append:
        add_values(*arguments)
    else:
        set_tag(*arguments)
# endregion


# region Download Actions
def add_lastfm_tags(song: Song):
    """Adds the tags received from Last.fm to the song.

        Parameters
        ----------
        song : Song -
            Song to be edited
        """
    tag_mappings = download_lastfm.download_lastfm_mappings(song)
    if tag_mappings is None:
        return
    for songtag, values in tag_mappings.items():
        add_values(song, songtag, values)


def add_discogs_tags(response: requests.Response,
                     songs: List[Union[Song, None]],
                     song_indexes: List[int],
                     job_index: int,
                     action_index: int,
                     signals: ActionSignals,
                     subaction_signals: SubactionSignals):
    """Adds the data from the discogs response to the list of songs,
        at the related mappings.

        Parameters
        ----------
        response : requests.Response -
            Response recieved from discogs related to a specific release ID\n
        songs : List[Union[Song, None]] -
            List of current songs to be edited\n
        song_indexes : List[int] -
            List indicating which song should be edited
            related to which track number from the discogs release\n
        job_index : int -
            The number of the job associated with this action.
            Stored for progress updates.\n
        action_index : int -
            The number of this action in the job list.
            Stored for progress updates.\n
        signals : ActionSignals -
            The signals stored in order to update progress.
        """
    discogs_mappings = download_discogs.map_discogs_tags(response,
                                                         job_index,
                                                         action_index,
                                                         subaction_signals)
    signals.action_started.emit(job_index, action_index, len(discogs_mappings))
    for index, mapping in enumerate(discogs_mappings):
        if song_indexes[index] is not None and song_indexes[index] >= 0:
            signals.action_progress.emit(job_index, action_index, index)
            try:
                song = songs[song_indexes[index]]
                song = cast(Song, song)
                for tag, values in mapping.items():
                    add_values(song, tag, values)
            except IndexError:
                continue
# endregion


# region Excel Actions
relative_path = str(Path('music_modify', 'excel', 'excel_current_info.xlsx'))
excel_file = file_utils.get_resource_path(relative_path)
tag_workbook = openpyxl.load_workbook(excel_file)
# tag_workbook = openpyxl.load_workbook(
#     Path.cwd()/Path('excel', 'excel_current_info.xlsx'))


def _add_values_to_sheet(tag: SongTag,
                         song: Song,
                         sheet: Worksheet,
                         second_sheet: Union[Worksheet, None] = None):
    """Add the values from a speicifc tag to the indicated sheet.
        If a second sheet is added,
        add the second values from the tag.

        Parameters
        ----------
        tag : SongTag -
            Which tag the data should be received from\n
        song : Song -
            Which song the data should be receieved from\n
        sheet : Worksheet -
            Which sheet the data should be added to\n
        second_sheet : Union[Worksheet, None], optional -
            Second sheet where data should be added, by default None
        """
    values = tag.get_tag(song.id3)
    if values is None:
        return
    for value in values:
        if tag.value_length == 1:
            value = cast(str, value)
            sheet.append([value])
        elif tag.value_length == 2:
            value = cast(List[str], value)
            role, person = value
            sheet.append([role])
            if second_sheet is not None:
                second_sheet.append([person])


def add_values_to_excel(song: Song):
    """Add the values from the song to the tag_workbook.

        Parameters
        ----------
        song : Song
            Song where data should be received from
        """
    people_sheet = tag_workbook['People']
    people_tags = ['Composer',
                   'Lyricist',
                   'Conductor',
                   'Remixer',
                   'Artist',
                   'Album Artist']
    for tag_name in people_tags:
        tag = songtag_functions.map_tag(tag_name)
        if tag is None:
            continue
        _add_values_to_sheet(tag, song, people_sheet)

    instrument_sheet = tag_workbook['Instruments']
    musician_credits = songtag_functions.map_tag('Musician Credits')
    if musician_credits is not None:
        _add_values_to_sheet(musician_credits,
                             song,
                             instrument_sheet,
                             people_sheet)

    role_sheet = tag_workbook['Roles']
    involved_people = songtag_functions.map_tag("Involved People")
    if involved_people is not None:
        _add_values_to_sheet(involved_people,
                             song,
                             role_sheet,
                             people_sheet)

    genre_sheet = tag_workbook['Genres']
    genre = songtag_functions.map_tag('Genre')
    if genre is not None:
        _add_values_to_sheet(genre, song, genre_sheet)

    publisher_sheet = tag_workbook['Publishers']
    publisher = songtag_functions.map_tag('Publisher')
    if publisher is not None:
        _add_values_to_sheet(publisher, song, publisher_sheet)

    # ! to reduce excess memory, spreadsheet is not saved in this function.
    # ! For the changes to be saved, call:
    # tag_workbook.save(Path('excel', 'excel_current_info.xlsx')
# endregion


# region Action Classes & Mappings
class ActionDetails:
    """Class used to store the additional information needed
        for an action to be performed.
    """
    def __init__(self,
                 function: Callable,
                 action_type: ActionType = ActionType.Unset,
                 input_type: Tuple[InputWidget, Union[ValuesTableType, None]]
                 = (InputWidget.NotUsed, None),
                 params: Union[Dict[str, Any], None] = None):
        """Constructor for Action Details. Stores additional info.

        Parameters
        ----------
        function : Callable -
            Function that should be performed\n
        action_type : ActionType, optional -
            Enum indicating the nature of the action that will be performed.
            By default ActionType.Unset.\n
        input_type : Tuple[InputWidget, Union[ValuesTableType, None]],
            optional -
            Enum indicating whether the action requires additional input,
            and if so, what type.
            First param is the widget that should be shown.
            Second param is the nature of that widget.
            By default (InputWidget.NotUsed, None).\n
        params : Union[Dict[str, Any], None], optional -
            Additional parameters that should be sent to
            the function before being performed.
            By default None.
        """
        self.function = function
        self.action_type = action_type
        self.input_type = input_type[0]
        self.values_table_type = input_type[1]
        self.extra_params = params


function_mappings = {
    'Add Tag': ActionDetails(add_tag, ActionType.Manual),
    'Remove Tag': ActionDetails(remove_tag, ActionType.Manual),
    'Set Tag': ActionDetails(set_tag,
                             ActionType.Manual,
                             (InputWidget.ValuesTable,
                              ValuesTableType.Standard)),
    'Add Values': ActionDetails(add_values,
                                ActionType.Manual,
                                (InputWidget.ValuesTable,
                                 ValuesTableType.Standard)),
    'Remove Values': ActionDetails(remove_values,
                                   ActionType.Manual,
                                   (InputWidget.ValuesTable,
                                    ValuesTableType.Standard)),
    'Replace Values': ActionDetails(replace_values,
                                    ActionType.Manual,
                                    (InputWidget.ValuesTable,
                                     ValuesTableType.Replace)),
    'Split Values': ActionDetails(split_values, ActionType.Manual),
    'Remove Duplicate Values': ActionDetails(remove_duplicates,
                                             ActionType.Manual),
    'Copy Values Within (Append)': ActionDetails(copy_values,
                                                 ActionType.Manual,
                                                 params={
                                                    'copy_mode':
                                                    CopyType.Append
                                                 }),
    'Copy Values Within (Replace)': ActionDetails(copy_values,
                                                  ActionType.Manual),
    'Copy Values Across (Append)': ActionDetails(copy_values,
                                                 ActionType.Manual,
                                                 (InputWidget.CopyTable,
                                                  None),
                                                 params={
                                                     'copy_mode':
                                                     CopyType.Append |
                                                     CopyType.Across
                                                 }),
    'Copy Values Across (Replace)': ActionDetails(copy_values,
                                                  ActionType.Manual,
                                                  (InputWidget.CopyTable,
                                                   None),
                                                  params={
                                                      'copy_mode':
                                                      CopyType.Across
                                                  }),
    'Add Last.fm Tags': ActionDetails(add_lastfm_tags, ActionType.Download),
    'Add Discogs Tags': ActionDetails(add_discogs_tags,
                                      ActionType.Download,
                                      (InputWidget.DiscogsTable, None)),
    'Add Values to Excel': ActionDetails(add_values_to_excel, ActionType.Excel)
}


class ActionToCreate():
    """Class storing the information required for an action to be performed.
        """
    def __init__(self, model: SongTableProxyModel):
        """Constructor for Action To Create. Stores required info for action

            Parameters
            ----------
            model : SongTableProxyModel -
                The model of the songs being edited in this action.
            """
        self.model = model
        self.action: Union[str, None] = None
        self.tags: Union[List[SelectedTag], None] = []
        self.values: Union[None, List[Union[str, List[str]]]] = None
        self.response: Union[None, requests.Response] = None
        self.mappings: Union[None, List[Union[int, None]]] = None
        self.custom_songs_name: Union[None, str] = None
        self.custom_values_name: Union[None, str] = None
        self.copy_mappings: Union[List[int], None] = None
        self.tags_display: Union[str, None] = None
        self.discogs_release_id: Union[str, None] = None

    def get_songs(self) -> List[Song]:
        """Gets the songs from the sent model, in order for editing.

            Returns
            -------
            List[Song] -
                List of songs that were stored in the model.
            """
        songs: List[Song] = []
        for row_num in range(self.model.rowCount()):
            song_index = self.model.index(row_num, 0)
            song = self.model.data(song_index, UserRole.SongRole.value)
            songs.append(song)
        return songs


class Action():
    """Class used to create an action that should be performed,
        and then perform that action
        """
    def __init__(self,
                 action_to_create: ActionToCreate,
                 job_index: int,
                 action_index: int
                 ):
        """Constructor for Action.

            Parameters
            ----------
            action_to_create : ActionToCreate -
                The data that is needed to determine the nature of the action.
            """
        self.action = action_to_create.action
        if self.action is None:
            return
        self.action = cast(str, self.action)

        self.action_details = function_mappings[self.action]
        self.function = self.action_details.function
        self.extra_params = self.action_details.extra_params

        self.songs = action_to_create.get_songs()
        self.tags = action_to_create.tags
        self.new_values = action_to_create.values
        self.copy_mappings = action_to_create.copy_mappings
        self.response = action_to_create.response
        self.song_indexes = action_to_create.mappings
        self.subaction_signals = SubactionSignals() if self.response else None

        self.custom_songs_name = action_to_create.custom_songs_name
        self.custom_values_name = action_to_create.custom_values_name
        self.tags_display = action_to_create.tags_display
        self.discogs_release_id = action_to_create.discogs_release_id

        self.signals = ActionSignals()
        self.job_index = job_index
        self.action_index = action_index

        self.method_params = self.map_parameters_global()

    def map_parameters_global(self) -> Union[Dict[str, Any]]:
        """Determine which parameters a function needs,
            and return those function as a keyword dict.
            Does not include arguments like song and tag,
            as they are iterated over in the action.

            Returns
            -------
            Union[Dict[str, Any]] -
                Dict of keyword arguments needed to perform the function
                related to this action.
            """
        global_params: Dict[str, Any] = {}
        sig = inspect.signature(self.function)
        for param in sig.parameters:
            if param == 'new_values':
                global_params['new_values'] = self.new_values
            elif param == 'values_to_remove':
                global_params['values_to_remove'] = self.new_values
            elif param == 'response':
                global_params['response'] = self.response
            elif param == 'songs':
                global_params['songs'] = self.songs
            elif param == 'song_indexes':
                global_params['song_indexes'] = self.song_indexes
            elif param == 'job_index':
                global_params['job_index'] = self.job_index
            elif param == 'action_index':
                global_params['action_index'] = self.action_index
            elif param == 'signals':
                global_params['signals'] = self.signals
            elif param == 'subaction_signals':
                global_params['subaction_signals'] = self.subaction_signals
        if self.extra_params is None:
            return global_params
        for extra_param, value in self.extra_params.items():
            if extra_param in sig.parameters:
                global_params[extra_param] = value
        return global_params

    def perform_action(self):
        """Determine the additional parameters needed for the action,
            and performs the function related to the action.
        """
        sig = inspect.signature(self.function)
        to_songs = []
        if 'to_song' in sig.parameters:
            for song_index in self.copy_mappings:
                song = None if (song_index is None or song_index < 0)\
                    else self.songs[song_index]
                to_songs.append(song)
        if 'song' in sig.parameters:
            if self.songs is None:
                return
            self.signals.action_started.emit(self.job_index,
                                             self.action_index,
                                             len(self.songs))
            for index, song in enumerate(self.songs):
                if 'tag' in sig.parameters:
                    if self.tags is None:
                        return
                    for selected_tag in self.tags:
                        tag = selected_tag.tag
                        if tag is None:
                            return
                        self.method_params['tag'] = tag
                        self.method_params['song'] = song
                        self.function(**self.method_params)
                elif 'tag_selection' in sig.parameters:
                    if self.tags is None:
                        return
                    for selected_tag in self.tags:
                        self.method_params['tag_selection'] = selected_tag
                        self.method_params['song'] = song
                        self.method_params['to_song'] = to_songs[index]
                        self.function(**self.method_params)
                else:
                    self.method_params['song'] = song
                    self.function(**self.method_params)
                self.signals.action_progress.emit(self.job_index,
                                                  self.action_index,
                                                  index + 1)
        else:
            self.function(**self.method_params)
        self.signals.action_finished.emit(self.job_index, self.action_index)
        if self.function == add_values_to_excel:
            tag_workbook.save(excel_file)
# endregion
