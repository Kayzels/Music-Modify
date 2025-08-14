"""Module that defines the `Settings` class.

It also creates the global `settings` object,
which should be used when wanting to access user preferences.
"""

import logging
from typing import ClassVar, final

from PySide6.QtCore import QSettings

from music_modify.custom_types.songtag import SongTag
from music_modify.custom_types.tag_info import TagInfo

logger = logging.getLogger(__name__)


@final
class Settings:
    """Wrapper for QSettings that provides easier access to defined setting keys."""

    def __init__(self, new_settings: QSettings | None = None) -> None:
        """Create a new Settings object.

        Args:
            new_settings: The settings values that should be read, if present.
        """
        logger.info("In init method for Settings object")
        self._settings: QSettings = (
            # PERF: Is there a way to get this from the QApplication,
            # rather than setting it twice?
            QSettings("Kayzels", "Music Modify")
            if new_settings is None
            else new_settings
        )

        # Store in a cache to prevent needing to call getArray on every cell
        self._table_tags_cache: list[SongTag] | None = None
        self._initializeDefaults()

    default_split_text_entered = ","
    default_split_values_display = "; "
    default_split_values_at = ";"

    @property
    def split_text_entered(self) -> str:
        """The symbol that should split the data typed in.

        For example, with it set to be ",",
        John Smith, Jane Doe should be understood as two separate values.
        """
        return str(
            self._settings.value(
                "Split/split_text_entered",
                Settings.default_split_text_entered,
            ),
        )

    @split_text_entered.setter
    def split_text_entered(self, value: str) -> None:
        self._settings.setValue("Split/split_text_entered", value)

    @property
    def split_values_display(self) -> str:
        r"""The symbol used to separate values when there are multiple items in a field.

        If set to \\, John Smith, Jane Doe would be shown as
        John Smith\\Jane Doe
        """
        return str(
            self._settings.value(
                "Split/split_values_display",
                Settings.default_split_values_display,
            ),
        )

    @split_values_display.setter
    def split_values_display(self, value: str) -> None:
        self._settings.setValue("Split/split_values_display", value)

    @property
    def split_values_at(self) -> str:
        """The symbol used when existing values should be split.

        For example, if an existing field is John Smith; Jane Doe,
        this should split it into separate values.
        """
        return str(
            self._settings.value(
                "Split/split_values_at",
                Settings.default_split_values_at,
            ),
        )

    @split_values_at.setter
    def split_values_at(self, value: str) -> None:
        self._settings.setValue("Split/split_values_at", value)

    default_tags: ClassVar[list[TagInfo]] = [
        TagInfo(display_name="Track", id3_key="TRCK", show_in_table=True),
        TagInfo(display_name="Title", id3_key="TIT2", show_in_table=True),
        TagInfo(display_name="Artist", id3_key="TPE1", show_in_table=True),
        TagInfo(display_name="Album Artist", id3_key="TPE2", show_in_table=True),
        TagInfo(display_name="Album", id3_key="TALB", show_in_table=True),
        TagInfo(display_name="Composer", id3_key="TCOM", show_in_table=True),
        TagInfo(display_name="Lyricist", id3_key="TEXT", show_in_table=True),
        TagInfo(display_name="Language", id3_key="TLAN", show_in_table=True),
        TagInfo(display_name="BPM", id3_key="TBPM", show_in_table=True),
        TagInfo(display_name="Key", id3_key="TKEY", show_in_table=True),
        TagInfo(display_name="Involved People", id3_key="TIPL", show_in_table=True),
        TagInfo(display_name="Musician Credits", id3_key="TMCL", show_in_table=True),
        TagInfo(display_name="Sort Composer", id3_key="TSOC"),
        TagInfo(display_name="Conductor", id3_key="TPE3"),
        TagInfo(display_name="Year", id3_key="TDRC"),
        TagInfo(display_name="Original Album", id3_key="TOAL"),
        TagInfo(display_name="Original Artist", id3_key="TOPE"),
        TagInfo(display_name="Subtitle", id3_key="TIT3"),
        TagInfo(display_name="Disc Number", id3_key="TPOS"),
        TagInfo(display_name="Set Subtitle", id3_key="TSST"),
        TagInfo(display_name="Sort Artist", id3_key="TSOP"),
        TagInfo(display_name="Sort Album Artist", id3_key="TSO2"),
        TagInfo(display_name="Genre", id3_key="TCON"),
        TagInfo(display_name="Publisher", id3_key="TPUB"),
        TagInfo(display_name="Mood", id3_key="TMOO"),
        TagInfo(display_name="Display Composer", id3_key="TXXX:DISPLAY COMPOSER"),
        TagInfo(display_name="Release Date", id3_key="TXXX:RELEASE DATE"),
        TagInfo(display_name="Original Year", id3_key="TXXX:originalyear"),
        TagInfo(display_name="Scrobble Title", id3_key="TXXX:SCROBBLE TITLE"),
        TagInfo(display_name="Track Name", id3_key="TXXX:TRACK NAME"),
        TagInfo(display_name="Song Type", id3_key="TXXX:SONG TYPE"),
        TagInfo(display_name="Scrobble Album", id3_key="TXXX:SCROBBLE ALBUM"),
        TagInfo(display_name="Album Name", id3_key="TXXX:ALBUM NAME"),
        TagInfo(display_name="Album Type", id3_key="TXXX:ALBUM TYPE"),
        TagInfo(display_name="Album Version", id3_key="TXXX:ALBUM VERSION"),
        TagInfo(display_name="Scrobble Artist", id3_key="TXXX:SCROBBLE ARTIST"),
        TagInfo(display_name="Artist Shown", id3_key="TXXX:ARTIST SHOWN"),
        TagInfo(display_name="Display Artist", id3_key="TXXX:DISPLAY ARTIST"),
        TagInfo(display_name="Label", id3_key="TXXX:LABEL"),
        TagInfo(display_name="Performer", id3_key="TXXX:PERFORMER"),
        TagInfo(display_name="Remixer", id3_key="TXXX:REMIXER"),
        TagInfo(display_name="Occasion", id3_key="TXXX:OCCASION"),
        TagInfo(display_name="Keywords", id3_key="TXXX:KEYWORDS"),
        TagInfo(display_name="Tempo", id3_key="TXXX:TEMPO"),
    ]
    "Default values for known tags, if there are no user changes."

    @property
    def table_tags(self) -> list[SongTag]:
        """The tags shown in the main table."""
        if self._table_tags_cache is None:
            self._table_tags_cache = [
                SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
                for tag in self.info_tags
                if tag.show_in_table
            ]
        return self._table_tags_cache

    @property
    def all_tags(self) -> list[SongTag]:
        """`SongTag` version of the tags that are stored in settings.

        Used when a `SongTag` specifically needs to be checked,
        but the majority of the time, we can use `info_tags` instead,
        using `TagInfo` objects.
        """
        return [
            SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
            for tag in self.info_tags
        ]

    @property
    def info_tags(self) -> list[TagInfo]:
        """`TagInfo` version of the tags that are stored in settings.

        Use `all_tags` if needing `SongTag` objects.
        """
        return self._getArray("Tags/info_tags")

    @info_tags.setter
    def info_tags(self, value: list[TagInfo]) -> None:
        self._table_tags_cache = None  # Invalidate cache
        self._setArray("Tags/info_tags", value)

    def _setArray(self, key: str, vals: list[TagInfo]) -> None:
        """Set the QSettings array based on the list of TagInfo.

        Writes the settings file in QSettings array form,
        which then needs to be converted into a list to be usable in Python.
        """
        logger.info(f"Began creating array for {key} with {len(vals)} entries.")

        self._settings.beginGroup(key)
        self._settings.remove("")
        self._settings.endGroup()

        self._settings.beginWriteArray(key)
        for index, tag in enumerate(vals):
            self._settings.setArrayIndex(index)
            self._settings.setValue("display_name", tag.display_name)
            self._settings.setValue("id3_key", tag.id3_key)
            self._settings.setValue("show_in_table", str(tag.show_in_table))
        self._settings.endArray()

    def _getArray(self, key: str) -> list[TagInfo]:
        """Convert the stored QSettings array into a Python list of tags.

        Args:
            key: The name of the array to read from settings.
        """
        size = self._settings.beginReadArray(key)
        tags: list[TagInfo] = []
        for i in range(size):
            self._settings.setArrayIndex(i)
            display_name: str = str(self._settings.value("display_name"))
            id3_key: str = str(self._settings.value("id3_key"))
            show_in_table: bool = self._settings.value("show_in_table") == "True"
            tags.append(
                TagInfo(
                    display_name=display_name,
                    id3_key=id3_key,
                    show_in_table=show_in_table,
                ),
            )
        self._settings.endArray()
        return tags

    def _initializeDefaults(self) -> None:
        """Set the default values for all settings, if they aren't already set."""
        logger.info("Called initialise defaults")
        if not self._settings.contains("Split/split_text_entered"):
            self.split_text_entered = Settings.default_split_text_entered
        else:
            logger.info("Split text entered already set")
        if not self._settings.contains("Split/split_values_display"):
            self.split_values_display = Settings.default_split_values_display
        else:
            logger.info("Split values display already set")
        if not self._settings.contains("Split/split_values_at"):
            self.split_values_at = Settings.default_split_values_at
        else:
            logger.info("Split values at already set")

        size = self._settings.beginReadArray("Tags/info_tags")
        self._settings.endArray()

        if not self._settings.contains("Tags/info_tags") and size == 0:
            logger.info("Setting info tags")
            self.info_tags = Settings.default_tags
        else:
            logger.info("Info Tags already set")

    def resetSplit(self) -> None:
        """Reset the value for the split preferences back to default."""
        logger.info("Called reset split")
        self.split_text_entered = Settings.default_split_text_entered
        self.split_values_at = Settings.default_split_values_at
        self.split_values_display = Settings.default_split_values_display

    def resetTags(self) -> None:
        """Reset the value for the tag list back to default."""
        logger.info("Called reset tags")
        self.info_tags = Settings.default_tags


settings = Settings()
