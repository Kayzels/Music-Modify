from dataclasses import dataclass
from PySide6.QtCore import QSettings
from typing import final
from music_modify.custom_types.songtag import SongTag


@dataclass(order=True, frozen=True)
class FileTag:
    display_name: str
    id3_key: str


@final
class _Settings:
    def __init__(self):
        self._settings: QSettings = QSettings("Kayzels", "Music Modify")
        self._initializeDefaults()

    @property
    def split_text_entered(self) -> str:
        """The symbol that should split the data typed in.
        For example, with it set to be ",",
        John Smith, Jane Doe should be understood as two separate values."""
        return str(self._settings.value("Split/split_text_entered", ","))

    @split_text_entered.setter
    def split_text_entered(self, value: str):
        self._settings.setValue("Split/split_text_entered", value)

    @property
    def split_values_display(self) -> str:
        """The symbol that should be used in the table to show when
        there are multiple items in a field.
        If set to \\, John Smith, Jane Doe would be shown as
        John Smith\\Jane Doe
        """
        return str(self._settings.value("Split/split_values_display", r"\\"))

    @split_values_display.setter
    def split_values_display(self, value: str):
        self._settings.setValue("Split/split_values_display", value)

    @property
    def split_values_at(self) -> str:
        """The symbol used when existing values should be split.
        For example, if an existing field is John Smith; Jane Doe,
        this should split it into separate values.
        """
        return str(self._settings.value("Split/split_values_at", ";"))

    @split_values_at.setter
    def split_values_at(self, value: str):
        self._settings.setValue("Split/split_values_at", value)

    default_file_tags: list[FileTag] = [
        FileTag(display_name="Track", id3_key="TRCK"),
        FileTag(display_name="Title", id3_key="TIT2"),
        FileTag(display_name="Artist", id3_key="TPE1"),
        FileTag(display_name="Album Artist", id3_key="TPE2"),
        FileTag(display_name="Album", id3_key="TALB"),
        FileTag(display_name="Composer", id3_key="TCOM"),
        FileTag(display_name="Lyricist", id3_key="TEXT"),
        FileTag(display_name="Language", id3_key="TLAN"),
        FileTag(display_name="BPM", id3_key="TBPM"),
        FileTag(display_name="Key", id3_key="TKEY"),
        FileTag(display_name="Involved People", id3_key="TIPL"),
        FileTag(display_name="Musician Credits", id3_key="TMCL"),
    ]

    @property
    def file_tags(self) -> list[SongTag]:
        """The tags shown in the main table."""
        return self._getArray("Tags/file_tags")

    @file_tags.setter
    def file_tags(self, value: list[FileTag]):  # pyright: ignore[reportPropertyTypeMismatch]
        """Should be a list of FileTag instead of SongTag,
        so that it's usable in settings.
        Otherwise you'd need to convert to FileTag, and then back into SongTag later."""
        self._setArray("Tags/file_tags", value)

    default_standard_tags: list[FileTag] = default_file_tags + [
        FileTag(display_name="Sort Composer", id3_key="TSOC"),
        FileTag(display_name="Conductor", id3_key="TPE3"),
        FileTag(display_name="Year", id3_key="TDRC"),
        FileTag(display_name="Original Album", id3_key="TOAL"),
        FileTag(display_name="Original Artist", id3_key="TOPE"),
        FileTag(display_name="Subtitle", id3_key="TIT3"),
        FileTag(display_name="Disc Number", id3_key="TPOS"),
        FileTag(display_name="Set Subtitle", id3_key="TSST"),
        FileTag(display_name="Sort Artist", id3_key="TSOP"),
        FileTag(display_name="Sort Album Artist", id3_key="TSO2"),
        FileTag(display_name="Genre", id3_key="TCON"),
        FileTag(display_name="Publisher", id3_key="TPUB"),
        FileTag(display_name="Mood", id3_key="TMOO"),
    ]

    @property
    def standard_tags(self) -> list[SongTag]:
        """The tags that are generally defined for music files."""
        return self._getArray("Tags/standard_tags")

    @standard_tags.setter
    def standard_tags(self, value: list[FileTag]):  # pyright: ignore[reportPropertyTypeMismatch]
        """Should be a list of FileTag instead of SongTag,
        so that it's usable in settings.
        Otherwise you'd need to convert to FileTag, and then back into SongTag later."""
        self._setArray("Tags/standard_tags", value)

    default_custom_tags: list[FileTag] = [
        FileTag(display_name="Display Composer", id3_key="TXXX:DISPLAY COMPOSER"),
        FileTag(display_name="Release Date", id3_key="TXXX:RELEASE DATE"),
        FileTag(display_name="Original Year", id3_key="TXXX:originalyear"),
        FileTag(display_name="Scrobble Title", id3_key="TXXX:SCROBBLE TITLE"),
        FileTag(display_name="Track Name", id3_key="TXXX:TRACK NAME"),
        FileTag(display_name="Song Type", id3_key="TXXX:SONG TYPE"),
        FileTag(display_name="Scrobble Album", id3_key="TXXX:SCROBBLE ALBUM"),
        FileTag(display_name="Album Name", id3_key="TXXX:ALBUM NAME"),
        FileTag(display_name="Album Type", id3_key="TXXX:ALBUM TYPE"),
        FileTag(display_name="Album Version", id3_key="TXXX:ALBUM VERSION"),
        FileTag(display_name="Scrobble Artist", id3_key="TXXX:SCROBBLE ARTIST"),
        FileTag(display_name="Artist Shown", id3_key="TXXX:ARTIST SHOWN"),
        FileTag(display_name="Display Artist", id3_key="TXXX:DISPLAY ARTIST"),
        FileTag(display_name="Label", id3_key="TXXX:LABEL"),
        FileTag(display_name="Performer", id3_key="TXXX:PERFORMER"),
        FileTag(display_name="Remixer", id3_key="TXXX:REMIXER"),
        FileTag(display_name="Occasion", id3_key="TXXX:OCCASION"),
        FileTag(display_name="Keywords", id3_key="TXXX:KEYWORDS"),
        FileTag(display_name="Tempo", id3_key="TXXX:TEMPO"),
    ]

    @property
    def custom_tags(self) -> list[SongTag]:
        """Additional tags which are not common.
        These tags always start with TXXX."""
        return self._getArray("Tags/custom_tags")

    @custom_tags.setter
    def custom_tags(self, value: list[FileTag]):  # pyright: ignore[reportPropertyTypeMismatch]
        """Should be a list of FileTag instead of SongTag,
        so that it's usable in settings.
        Otherwise you'd need to convert to FileTag, and then back into SongTag later."""
        self._setArray("Tags/custom_tags", value)

    @property
    def all_tags(self) -> list[SongTag]:
        return self.standard_tags + self.custom_tags

    def _setArray(self, key: str, vals: list[FileTag]):
        self._settings.beginWriteArray(key)
        for index, tag in enumerate(vals):
            self._settings.setArrayIndex(index)
            self._settings.setValue("display_name", tag.display_name)
            self._settings.setValue("id3_key", tag.id3_key)
        self._settings.endArray()

    def _getArray(self, key: str) -> list[SongTag]:
        size = self._settings.beginReadArray(key)
        tags: list[SongTag] = []
        for i in range(size):
            self._settings.setArrayIndex(i)
            display_name: str = str(self._settings.value("display_name"))
            id3_key: str = str(self._settings.value("id3_key"))
            tags.append(SongTag(display_name=display_name, id3_key=id3_key))
        self._settings.endArray()
        return tags

    def _initializeDefaults(self):
        if not self._settings.contains("Split/split_text_entered"):
            self.split_text_entered = ","
        if not self._settings.contains("Split/split_values_display"):
            self.split_values_display = r"\\"
        if not self._settings.contains("Split/split_values_at"):
            self.split_values_at = ";"
        if not self._settings.contains("Tags/file_tags"):
            self.file_tags = _Settings.default_file_tags
        if not self._settings.contains("Tags/standard_tags"):
            self.standard_tags = _Settings.default_standard_tags
        if not self._settings.contains("Tags/custom_tags"):
            self.custom_tags = _Settings.default_custom_tags


settings = _Settings()
