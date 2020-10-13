"""Module for downloading information from Last.fm
    """
# region Python Imports
from pathlib import Path
from typing import cast, Dict, List, Union
# endregion
# region Custom Imports
import pandas as pd
import requests
from ratelimit import limits, sleep_and_retry
# endregion
# region Project Imports
import config
from songs import Song, SongTag, songtag_functions
from utils import file_utils, util_functions as util_f
# endregion


USER_AGENT = config.USER_AGENT
API_KEY = config.LASTFM_API_KEY


# region Get Data
@sleep_and_retry
@limits(calls=2, period=1)
def get_last_fm_data(payload: Dict[str, str]) -> requests.Response:
    """Download information from Last FM

        Parameters
        ----------
        payload : Dict[str, str] -
            Extra parameters to be sent with the get request

        Returns
        -------
        requests.Response
            JSON Response of data from Last.fm
        """
    headers = {"user-agent": USER_AGENT}
    url = "http://ws.audioscrobbler.com/2.0/"

    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    return requests.get(url, headers=headers, params=payload)
# endregion


# region Map Data
def get_lastfm_mappings() -> pd.core.frame.DataFrame:
    """Get the data from an excel file that states what
        Last.fm Tags should map to

        Returns
        -------
        pd.core.frame.DataFrame
            Dataframe of mappings for Last.fm tags
        """

    relative_path = str(Path("music_modify", "excel", "download_lastfm_mappings.xlsx"))
    excel_file = file_utils.get_resource_path(relative_path)
    # excel_file = Path.cwd()/Path("excel", "download_lastfm_mappings.xlsx")
    dataframe = pd.read_excel(str(excel_file))
    for column in list(dataframe):
        dataframe[column] = dataframe[column].str.split('; ')
    dataframe = dataframe.explode("Last FM Tag", ignore_index=True)
    dataframe = dataframe.set_index('Last FM Tag')
    return dataframe


last_fm_mappings = get_lastfm_mappings()


def get_valid_values(dataframe: pd.core.frame.DataFrame,
                     last_fm_tag: str) -> Union[Dict, Dict[str, List[str]]]:
    """Get the tags that are in the dataframe,
        and map to the correct related tag.

    Parameters
    ----------
    dataframe : pd.core.frame.DataFrame
        Dataframe of last.fm mappings\n
    last_fm_tag : str
        Tag that should be mapped from last.fm

    Returns
    -------
    Union[Dict, Dict[str, List[str]]] -
        Dictionary of tag values:
            format is [tag_name, [tag_value1, tag_value2]]
    """
    vals: Union[Dict, Dict[str, str]] = {}
    if last_fm_tag not in dataframe.index:
        return vals
    vals = cast(Dict[str, List[str]], vals)
    column: str
    is_valid: bool
    for column, is_valid in pd.notna(dataframe.loc[last_fm_tag]).iteritems():
        if is_valid:
            for value in dataframe.loc[last_fm_tag][column]:
                if column in vals:
                    vals[column].append(value)
                else:
                    vals[column] = value
    return vals


def download_lastfm_mappings(song: Song) -> Union[Dict[
                                                   SongTag,
                                                   List[str]],
                                                  None]:
    """Download the data from last_fm and return the values
        that should be added to the song

        Parameters
        ----------
        song : Song -
            Song that should be edited

        Returns
        -------
        Union[Dict[ SongTag, List[str]], None] -
            Values that should be added to the song
        """
    title_tag_name = 'Scrobble Title'
    title_optional_name = 'Title'
    artist_tag_name = 'Scrobble Artist'
    artist_optional_name = 'Artist'
    title_tag = songtag_functions.map_optional_tag(title_tag_name,
                                                   title_optional_name)
    if title_tag is None:
        return None
    title_tag = cast(SongTag, title_tag)
    artist_tag = songtag_functions.map_optional_tag(artist_tag_name,
                                                    artist_optional_name)
    if artist_tag is None:
        return None
    artist_tag = cast(SongTag, artist_tag)
    track_vals = title_tag.get_tag(song.id3)
    if track_vals is None:
        title_tag = songtag_functions.map_tag(title_optional_name)
        if title_tag is None:
            return None
        title_tag = cast(SongTag, title_tag)
        track_vals = title_tag.get_tag(song.id3)
        if track_vals is None:
            return None
    artist_vals = artist_tag.get_tag(song.id3)
    if artist_vals is None:
        artist_tag = songtag_functions.map_tag(artist_optional_name)
        if artist_tag is None:
            return None
        artist_tag = cast(SongTag, artist_tag)
        artist_vals = artist_tag.get_tag(song.id3)
        if artist_vals is None:
            return None
    track_vals = cast(List[str], track_vals)
    artist_vals = cast(List[str], artist_vals)
    track = track_vals[0]
    artist = artist_vals[0]
    payload = {
        'method': 'track.gettoptags',
        'track': track,
        'artist': artist
    }
    response = get_last_fm_data(payload)
    if response.status_code != 200:
        print(f"Invalid. Status Code is {response.status_code}")
        return None
    else:
        data = response.json()
        tags: Union[List[str], List] = []
        try:
            for tag in data['toptags']['tag']:
                tags.append(tag['name'])
            valid_tags: Union[List[Dict], List] = []
            for tag in tags:
                vals = get_valid_values(last_fm_mappings, tag)
                if len(vals) > 0:
                    valid_tags.append(vals)
            valid_tags_dict: Dict[str, Union[List[str], List]] = {}
            for dict_tag_val in valid_tags:
                for key, values in dict_tag_val.items():
                    if key not in valid_tags_dict:
                        valid_tags_dict[key] = []
                    for value in values:
                        if value in valid_tags_dict[key]:
                            continue
                        valid_tags_dict[key].append(value)
            tags_mapped: Union[Dict, Dict[SongTag, List[str]]] = {}
            for tag, values in valid_tags_dict.items():
                mapped_tag = songtag_functions.map_tag(tag)
                if mapped_tag is None:
                    continue
                mapped_tag = cast(SongTag, mapped_tag)
                tags_mapped[mapped_tag] = values
            tags_mapped = cast(Dict[SongTag, List[str]], tags_mapped)
            return tags_mapped
        except KeyError:
            print(f"Key Error. Title: {payload['track']}.\
                  Artist: {payload['artist']}")
            util_f.jprint(data)
            return None
# endregion
