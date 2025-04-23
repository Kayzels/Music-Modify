from typing import final

from PySide6.QtCore import QSettings

from music_modify.custom_types.songtag import SongTag


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

    default_file_tags: list[SongTag] = [
        SongTag(display_name="Track", id3_key="TRCK"),
        SongTag(display_name="Title", id3_key="TIT2"),
        SongTag(display_name="Artist", id3_key="TPE1"),
        SongTag(display_name="Album Artist", id3_key="TPE2"),
        SongTag(display_name="Album", id3_key="TALB"),
        SongTag(display_name="Composer", id3_key="TCOM"),
        SongTag(display_name="Lyricist", id3_key="TEXT"),
        SongTag(display_name="Language", id3_key="TLAN"),
        SongTag(display_name="BPM", id3_key="TBPM"),
        SongTag(display_name="Key", id3_key="TKEY"),
        SongTag(display_name="Involved People", id3_key="TIPL"),
        SongTag(display_name="Musician Credits", id3_key="TMCL"),
    ]

    @property
    def file_tags(self) -> list[SongTag]:
        """The tags shown in the main table."""
        return self._getArray("Tags/file_tags")

    @file_tags.setter
    def file_tags(self, value: list[SongTag]):
        """Should be a list of FileTag instead of SongTag,
        so that it's usable in settings.
        Otherwise you'd need to convert to FileTag, and then back into SongTag later."""
        self._setArray("Tags/file_tags", value)

    default_standard_tags: list[SongTag] = default_file_tags + [
        SongTag(display_name="Sort Composer", id3_key="TSOC"),
        SongTag(display_name="Conductor", id3_key="TPE3"),
        SongTag(display_name="Year", id3_key="TDRC"),
        SongTag(display_name="Original Album", id3_key="TOAL"),
        SongTag(display_name="Original Artist", id3_key="TOPE"),
        SongTag(display_name="Subtitle", id3_key="TIT3"),
        SongTag(display_name="Disc Number", id3_key="TPOS"),
        SongTag(display_name="Set Subtitle", id3_key="TSST"),
        SongTag(display_name="Sort Artist", id3_key="TSOP"),
        SongTag(display_name="Sort Album Artist", id3_key="TSO2"),
        SongTag(display_name="Genre", id3_key="TCON"),
        SongTag(display_name="Publisher", id3_key="TPUB"),
        SongTag(display_name="Mood", id3_key="TMOO"),
    ]

    @property
    def standard_tags(self) -> list[SongTag]:
        """The tags that are generally defined for music files."""
        return self._getArray("Tags/standard_tags")

    @standard_tags.setter
    def standard_tags(self, value: list[SongTag]):
        """Should be a list of FileTag instead of SongTag,
        so that it's usable in settings.
        Otherwise you'd need to convert to FileTag, and then back into SongTag later."""
        self._setArray("Tags/standard_tags", value)

    default_custom_tags: list[SongTag] = [
        SongTag(display_name="Display Composer", id3_key="TXXX:DISPLAY COMPOSER"),
        SongTag(display_name="Release Date", id3_key="TXXX:RELEASE DATE"),
        SongTag(display_name="Original Year", id3_key="TXXX:originalyear"),
        SongTag(display_name="Scrobble Title", id3_key="TXXX:SCROBBLE TITLE"),
        SongTag(display_name="Track Name", id3_key="TXXX:TRACK NAME"),
        SongTag(display_name="Song Type", id3_key="TXXX:SONG TYPE"),
        SongTag(display_name="Scrobble Album", id3_key="TXXX:SCROBBLE ALBUM"),
        SongTag(display_name="Album Name", id3_key="TXXX:ALBUM NAME"),
        SongTag(display_name="Album Type", id3_key="TXXX:ALBUM TYPE"),
        SongTag(display_name="Album Version", id3_key="TXXX:ALBUM VERSION"),
        SongTag(display_name="Scrobble Artist", id3_key="TXXX:SCROBBLE ARTIST"),
        SongTag(display_name="Artist Shown", id3_key="TXXX:ARTIST SHOWN"),
        SongTag(display_name="Display Artist", id3_key="TXXX:DISPLAY ARTIST"),
        SongTag(display_name="Label", id3_key="TXXX:LABEL"),
        SongTag(display_name="Performer", id3_key="TXXX:PERFORMER"),
        SongTag(display_name="Remixer", id3_key="TXXX:REMIXER"),
        SongTag(display_name="Occasion", id3_key="TXXX:OCCASION"),
        SongTag(display_name="Keywords", id3_key="TXXX:KEYWORDS"),
        SongTag(display_name="Tempo", id3_key="TXXX:TEMPO"),
    ]

    @property
    def custom_tags(self) -> list[SongTag]:
        """Additional tags which are not common.
        These tags always start with TXXX."""
        return self._getArray("Tags/custom_tags")

    @custom_tags.setter
    def custom_tags(self, value: list[SongTag]):
        """Should be a list of FileTag instead of SongTag,
        so that it's usable in settings.
        Otherwise you'd need to convert to FileTag, and then back into SongTag later."""
        self._setArray("Tags/custom_tags", value)

    @property
    def all_tags(self) -> list[SongTag]:
        return self.standard_tags + self.custom_tags

    def _setArray(self, key: str, vals: list[SongTag]):
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
