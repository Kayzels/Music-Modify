# pyright: reportPrivateImportUsage=false
from mutagen.id3 import ID3TimeStamp

SongData = str | ID3TimeStamp | list[str] | list[list[str]] | None
SongEditData = str | list[str] | list[list[str]]
SongLineData = list[str] | list[ID3TimeStamp]
SongListData = list[str]
SongTableData = list[list[str]]
SongGroupData = SongLineData | SongListData | SongTableData | None
