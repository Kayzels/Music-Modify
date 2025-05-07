# pyright: reportPrivateImportUsage=false
from mutagen.id3 import ID3TimeStamp

# SongData = list[str] | list[ID3TimeStamp] | list[list[str]] | None

SongData = str | ID3TimeStamp | list[str] | list[list[str]] | None
SongEditData = str | list[str] | list[list[str]]
SongLineData = list[str] | list[ID3TimeStamp] | None
SongListData = list[str] | None
SongTableData = list[list[str]] | None
SongGroupData = SongLineData | SongListData | SongTableData
