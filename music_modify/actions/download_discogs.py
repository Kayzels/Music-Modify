"""Module for downloading and mapping data from discogs.

    """
# region Python Imports
from pathlib import Path
import re
from typing import cast, Dict, List, Tuple, Union
# endregion
# region Custom Imports
import pandas as pd
from ratelimit import limits, sleep_and_retry
import requests
# endregion
# region Project Imports
import config
from signals import SubactionSignals
from songs import songtag_functions
from utils import file_utils
# endregion


USER_AGENT = config.USER_AGENT
API_KEY = config.DISCOGS_API_KEY
API_SECRET = config.DISCOGS_API_SECRET


# region Get Data
@sleep_and_retry
@limits(calls=50, period=60)
def get_discogs_data(release_id: Union[int, str]) -> requests.Response:
    """Download data from discogs.

        Parameters
        ----------
        release_id : Union[int, str] -
            The ID that should be added to the get request for the data

        Returns
        -------
        requests.Response -
            The response returned by the discogs API
        """
    # TODO: Check master release type, and add as Enum
    headers = {"user-agent": USER_AGENT}
    url = f"https://api.discogs.com/releases/{release_id}"

    params = {
        'key': API_KEY,
        'secret': API_SECRET
    }

    response = requests.get(url, headers=headers, params=params)
    return response


def get_discogs_artist_mappings() -> pd.core.frame.DataFrame:
    """Get the data from an excel file that indicates
        what different discogs roles should be mapped to.

        Returns
        -------
        pd.core.frame.DataFrame
            DataFrame of the download excel file that stores discogs mappings.
        """
    relative_path = str(Path("music_modify", "excel", "download_discogs_mappings.xlsx"))
    # excel_file = Path.cwd()/Path('excel', 'download_discogs_mappings.xlsx')
    excel_file = file_utils.get_resource_path(relative_path)
    dataframe_orig = pd.read_excel(excel_file, index_col=0)
    dataframe_orig.index = dataframe_orig.index.str.lower()
    return dataframe_orig


dataframe = get_discogs_artist_mappings()


def get_value_to_add(artist: Dict[str, str]) -> Union[
                                                List[Tuple[str, str]],
                                                List[Tuple[str, List[str]]]]:
    """Gets which value(s) should be added to the song
        considering the dataframe.

        Parameters
        ----------
        artist : Dict[str, str] -
            Dictionary indicating the information about the artist
            received in the discogs response

        Returns
        -------
        Union[ List[Tuple[str, str]], List[Tuple[str, List[str]]]] -
            The information that should be added.
        """
    values_list: Union[List[Tuple[str, str]],
                       List[Tuple[str, List[str]]],
                       List] = []
    name_pattern = r"\s\(\d*\)"
    role_pattern = r"\s\[(.*)\]"
    role_orig = artist['role']
    roles = role_orig.split(', ')
    for orig_role in roles:
        role_split = re.split(role_pattern, orig_role)
        role = role_split[0].lower()
        role_extra = '' if len(role_split) == 1\
            else f"[{role_split[1].lower()}]"
        name = re.split(name_pattern, artist['name'])[0]
        if role in dataframe.index:
            is_valid: bool
            column: str
            length_str = 'Tag Length'
            for column, is_valid in pd.notna(dataframe.loc[role]).iteritems():
                if is_valid:
                    if column == length_str:
                        continue
                    tag_length = int(dataframe.loc[role, length_str])
                    if tag_length == 2:
                        values_list = cast(List[
                                           Tuple[str, List[str]]],
                                           values_list)
                        role_val = f"{dataframe.loc[role][column]}{role_extra}"
                        value_to_add: Union[List[str], str]
                        value_to_add = [role_val, name]
                    else:
                        values_list = cast(List[
                                            Tuple[str, str]],
                                           values_list)
                        value_to_add = name
                    values_list.append((column,
                                        value_to_add))  # type: ignore
    values_list = cast(Union[List[Tuple[str, str]],
                       List[Tuple[str, List[str]]]], values_list)
    return values_list


def get_between_tracks(start_track: str,
                       end_track: str,
                       tracklist: Union[
                           List[Dict[str, str]],
                           List[Dict[str, List[str]]]
                       ]) -> Union[List[str], List]:
    """Get the tracks that exist between the given start and end tracks.

        Parameters
        ----------
        start_track : str -
            The first track that is part of these tracks\n
        end_track : str -
            The last track that is part of these tracks\n
        tracklist : Union[List[Dict[str, str]], List[Dict[str, List[str]]]] -
            All the tracks that exist in this release

        Returns
        -------
        Union[List[str], List]
            The tracks that are in between the start and end tracks, inclusive
        """

    # Union[List[Dict[str, str]], List[Dict[str, [Dict[str, str]]]]]
    between_tracks: Union[List[str], List] = []
    start_index = 0
    end_index = len(tracklist) - 1
    for index, track in enumerate(tracklist):
        track = cast(Dict[str, str], track)
        if track['position'] == start_track:
            start_index = index
        if track['position'] == end_track:
            end_index = index
    tracklist = cast(List[Dict[str, str]], tracklist)
    for track in tracklist[start_index: end_index + 1]:
        track = cast(Dict[str, str], track)
        between_tracks.append(track['position'])
    return between_tracks
# endregion


# region Map Data
def _map_tracklist(tracklist,
                   discogs_dict,
                   job_index: int,
                   action_index: int,
                   subaction_index: int,
                   subaction_signals: SubactionSignals):
    """Map the data from the discogs response to individual songs.

        Parameters
        ----------
        tracklist : List[Dict[str, Any]] -
            The tracklist in the discogs response\n
        discogs_dict : Dict[] -
            Dictionary of individual songs from discogs response.
        """
    for index, track in enumerate(tracklist):
        discogs_track = {}  # type: ignore
        if track['type_'] != 'track':
            continue
        track_position = track['position']
        discogs_dict[track_position] = discogs_track
        if 'extraartists' in track:
            extraartists = track['extraartists']
            for artist in extraartists:
                values = get_value_to_add(artist)
                for pair in values:
                    column = pair[0]
                    value_to_add = pair[1]
                    if column is None:
                        continue
                    if column in discogs_track:
                        discogs_track[column].append(value_to_add)
                    else:
                        discogs_track[column] = [value_to_add]
        subaction_signals.subaction_progress.emit(job_index,
                                                  action_index,
                                                  subaction_index,
                                                  index + 1)


def _map_extraartists(extra_artists: List[Dict[str, str]],
                      discogs_dict: Union[Dict,
                                          Dict[str, Dict[str, List[str]]],
                                          Dict[str, Dict[str, List[List[str]]]]
                                          ],
                      tracklist: Union[
                           List[Dict[str, str]],
                           List[Dict[str, List[str]]]],
                      job_index: int,
                      action_index: int,
                      subaction_index: int,
                      subaction_signals: SubactionSignals
                      ):
    """Map the artists at the bottom of a discogs release
        to the songs they are associated with

        Parameters
        ----------
        extra_artists : List[Dict[str, str]] -
            The artists that should be mapped\n
        discogs_dict : Dict[] -
            Dictionary of individual songs from discogs response.\n
        tracklist : List[] -
            The list of songs from a discogs release
        """
    for index, artist in enumerate(extra_artists):
        values = get_value_to_add((artist))
        for pair in values:
            column = pair[0]
            value_to_add = pair[1]
            if column is None:
                continue
            if artist['tracks'] == '':
                for track in discogs_dict.values():
                    if column in track:
                        track[column].append(value_to_add)  # type: ignore
                    else:
                        track[column] = [value_to_add]  # type: ignore
            else:
                tracks_split = artist['tracks'].split(', ')
                tracks = []
                to_values = (' to ', ' - ')
                for track_mapping in tracks_split:
                    if not any(to_value in track_mapping
                               for to_value in to_values):
                        tracks.append(track_mapping)
                        continue
                    else:
                        try:
                            for to_value in to_values:
                                between_tracks: List[str] = []
                                if track_mapping.find(to_value) == -1:
                                    continue
                                else:
                                    first_track = track_mapping\
                                        .split(to_value)[0]
                                    last_track = track_mapping\
                                        .split(to_value)[1]
                                    between_tracks = \
                                        get_between_tracks(
                                                           first_track,
                                                           last_track,
                                                           tracklist)
                                for track in between_tracks:
                                    tracks.append(track)
                        except IndexError:
                            continue
                for track_position in tracks:
                    if track_position in discogs_dict:
                        track = discogs_dict[track_position]
                        if column in track:
                            track[column].append(value_to_add)  # type: ignore
                        else:
                            track[column] = [value_to_add]  # type: ignore
                    elif track_position == '':
                        continue
        subaction_signals.subaction_progress.emit(job_index,
                                                  action_index,
                                                  subaction_index,
                                                  index + 1)


def _map_labels(labels,
                discogs_dict,
                job_index: int,
                action_index: int,
                subaction_index: int,
                subaction_signals: SubactionSignals):
    """Map the labels that are associated with a
        discogs release to all the songs in the dict.

        Parameters
        ----------
        labels : List[Dict[str, str]] -
            List of the labels associated with a discogs release,
            from the discogs response.\n
        discogs_dict : Dict[str, Dict[str, List[str]]] -
            Dict of mapped discogs tracks
        """
    for label in labels:
        for index, track in enumerate(discogs_dict.values()):
            if 'Publisher' in track:
                track['Publisher'].append(label['name'])
            else:
                track['Publisher'] = [label['name']]
            subaction_signals.subaction_progress.emit(job_index,
                                                      action_index,
                                                      subaction_index,
                                                      index + 1)


def _map_genres(genres,
                discogs_dict,
                job_index: int,
                action_index: int,
                subaction_index: int,
                subaction_signals: SubactionSignals):
    """Map the genres of a discogs release
        to all the songs in the dict

        Parameters
        ----------
        genres : List[str] -
            The genres that should be mapped.\n
        discogs_dict : Dict[] -
            Dictionary of individual songs from discogs response.\n
        """
    for genre in genres:
        for index, track in enumerate(discogs_dict.values()):
            if 'Genre' in track:
                track['Genre'].append(genre)
            else:
                track['Genre'] = [genre]
            subaction_signals.subaction_progress.emit(job_index,
                                                      action_index,
                                                      subaction_index,
                                                      index + 1)


def map_discogs_tags(response: requests.Response,
                     job_index: int,
                     action_index: int,
                     subaction_signals: SubactionSignals) -> List:
    """Map the data received from a discogs response to a list of songs
        indicating the individual songs in a discogs release

        Parameters
        ----------
        response : requests.Response
            The discogs response that is received

        Returns
        -------
        List
            A list of individual songs in a discogs release,
            ordered according to the tracklist on discogs
        """
    data = response.json()
    discogs_tracks: Union[Dict,
                          Dict[str, Dict[str, List[str]]],
                          Dict[str, Dict[str, List[List[str]]]]
                          ] = {}
    # region Map Tracklist
    subaction_index = 0
    subaction_signals.subaction_started.emit(job_index,
                                             action_index,
                                             subaction_index,
                                             len(data['tracklist']))
    _map_tracklist(data['tracklist'],
                   discogs_tracks,
                   job_index,
                   action_index,
                   subaction_index,
                   subaction_signals)
    subaction_signals.subaction_finished.emit(job_index,
                                              action_index,
                                              subaction_index)
    # endregion
    # region Global Extra Artists
    subaction_index = 1
    subaction_signals.subaction_started.emit(job_index,
                                             action_index,
                                             subaction_index,
                                             len(data['extraartists']))
    _map_extraartists(data['extraartists'],
                      discogs_tracks,
                      data['tracklist'],
                      job_index,
                      action_index,
                      subaction_index,
                      subaction_signals)
    subaction_signals.subaction_finished.emit(job_index,
                                              action_index,
                                              subaction_index)
    # endregion
    # region Labels
    subaction_index = 2
    subaction_signals.subaction_started.emit(job_index,
                                             action_index,
                                             subaction_index,
                                             len(data['labels']))
    _map_labels(data['labels'],
                discogs_tracks,
                job_index,
                action_index,
                subaction_index,
                subaction_signals)
    subaction_signals.subaction_finished.emit(job_index,
                                              action_index,
                                              subaction_index)
    # endregion
    # region Genres
    subaction_index = 3
    genres = []
    if 'genres' in data:
        genres = data['genres']
    if 'styles' in data:
        genres.extend(data['styles'])
    subaction_signals.subaction_started.emit(job_index,
                                             action_index,
                                             subaction_index,
                                             len(genres))
    _map_genres(genres,
                discogs_tracks,
                job_index,
                action_index,
                subaction_index,
                subaction_signals)
    subaction_signals.subaction_finished.emit(job_index,
                                              action_index,
                                              subaction_index)
    # endregion

    discogs_songs = []
    for track in discogs_tracks.values():
        mapped_track = {}
        for tag, values in track.items():
            mapped_track[songtag_functions.map_tag(tag)] = values
        discogs_songs.append(mapped_track)
    return discogs_songs
# endregion
