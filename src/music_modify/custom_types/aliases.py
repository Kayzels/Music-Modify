"""Aliases for commonly used types,
mainly for the different forms song metadata can take.
"""

# noinspection PyProtectedMember
from mutagen.id3 import ID3TimeStamp

SongLineData = list[str] | list[ID3TimeStamp]
"""Data that is represented in a single line. This should be a single value,
but mutagen wraps that in a list.
"""
SongListData = list[str]
"Data that has multiple values, but not pairs of values."
SongTableData = list[list[str]]
"Data that is a list of people pairs, of the form [role, person]"
SongEditData = str | list[str] | list[list[str]]
"""The forms of data that can be edited directly by the user.
A string for a single field,
a list of strings for fields with multiple values (like composer),
and a list of list of strings for fields with people pairs.
"""
SongGroupData = SongLineData | SongListData | SongTableData | None
"""Optional data that is editable in a widget of some sort.
Note it *does not* include `str`,
as any single string instances are wrapped in a list.
"""
