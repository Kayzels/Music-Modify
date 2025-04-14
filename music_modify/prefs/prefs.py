from PySide6.QtCore import QSettings
from typing import cast, final
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
        SongTag("Track", "TRCK"),
        SongTag("Title", "TIT2"),
        SongTag("Artist", "TPE1"),
        SongTag("Album Artist", "TPE2"),
        SongTag("Album", "TALB"),
        SongTag("Composer", "TCOM"),
        SongTag("Lyricist", "TEXT"),
        SongTag("Language", "TLAN"),
        SongTag("BPM", "TBPM"),
        SongTag("Key", "TKEY"),
        SongTag("Involved People", "TIPL"),
        SongTag("Musician Credits", "TMCL"),
    ]

    @property
    def file_tags(self) -> list[SongTag]:
        """The tags shown in the main table."""
        return cast(
            list[SongTag],
            self._settings.value("Tags/file_tags", _Settings.default_file_tags),
        )

    @file_tags.setter
    def file_tags(self, value: list[SongTag]):
        self._settings.setValue("Tags/file_tags", value)

    default_standard_tags: list[SongTag] = default_file_tags + [
        SongTag("Sort Composer", "TSOC"),
        SongTag("Conductor", "TPE3"),
        SongTag("Year", "TDRC"),
        SongTag("Original Album", "TOAL"),
        SongTag("Original Artist", "TOPE"),
        SongTag("Subtitle", "TIT3"),
        SongTag("Disc Number", "TPOS"),
        SongTag("Set Subtitle", "TSST"),
        SongTag("Sort Artist", "TSOP"),
        SongTag("Sort Album Artist", "TSO2"),
        SongTag("Genre", "TCON"),
        SongTag("Publisher", "TPUB"),
        SongTag("Mood", "TMOO"),
    ]

    @property
    def standard_tags(self) -> list[SongTag]:
        """The tags that are generally defined for music files."""
        return cast(
            list[SongTag],
            self._settings.value("Tags/file_tags", _Settings.default_standard_tags),
        )

    @standard_tags.setter
    def standard_tags(self, value: list[SongTag]):
        self._settings.setValue("Tags/standard_tags", value)

    default_custom_tags: list[SongTag] = [
        SongTag("Display Composer", "TXXX:DISPLAY COMPOSER"),
        SongTag("Release Date", "TXXX:RELEASE DATE"),
        SongTag("Original Year", "TXXX:originalyear"),
        SongTag("Scrobble Title", "TXXX:SCROBBLE TITLE"),
        SongTag("Track Name", "TXXX:TRACK NAME"),
        SongTag("Song Type", "TXXX:SONG TYPE"),
        SongTag("Scrobble Album", "TXXX:SCROBBLE ALBUM"),
        SongTag("Album Name", "TXXX:ALBUM NAME"),
        SongTag("Album Type", "TXXX:ALBUM TYPE"),
        SongTag("Album Version", "TXXX:ALBUM VERSION"),
        SongTag("Scrobble Artist", "TXXX:SCROBBLE ARTIST"),
        SongTag("Artist Shown", "TXXX:ARTIST SHOWN"),
        SongTag("Display Artist", "TXXX:DISPLAY ARTIST"),
        SongTag("Label", "TXXX:LABEL"),
        SongTag("Performer", "TXXX:PERFORMER"),
        SongTag("Remixer", "TXXX:REMIXER"),
        SongTag("Occasion", "TXXX:OCCASION"),
        SongTag("Keywords", "TXXX:KEYWORDS"),
        SongTag("Tempo", "TXXX:TEMPO"),
    ]

    @property
    def custom_tags(self) -> list[SongTag]:
        """Additional tags which are not common.
        These tags always start with TXXX."""
        return cast(
            list[SongTag],
            self._settings.value("Tags/file_tags", _Settings.default_custom_tags),
        )

    @custom_tags.setter
    def custom_tags(self, value: list[SongTag]):
        self._settings.setValue("Tags/custom_tags", value)

    @property
    def all_tags(self) -> list[SongTag]:
        return self.standard_tags + self.custom_tags

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
