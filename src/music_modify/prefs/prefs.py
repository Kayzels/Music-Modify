"""Module that defines the `Settings` class.

It also creates the global `settings` object,
which should be used when wanting to access user preferences.
"""

import logging
from typing import ClassVar, final

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from music_modify.custom_types.enums import EditorType
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
        self._settings: QSettings | None = None

        # Store in a cache to prevent needing to call getArray on every cell
        self._table_tags_cache: list[SongTag] | None = None

        if new_settings is not None:
            self._settings = new_settings
            self._initializeDefaults()

    def configureForApplication(self) -> None:
        """Configure the QSettings object using info from the QApplication.

        Uses the organization and application name from the QApplication instance.

        This should only be called once the QApplication has been initialized.
        """
        if self._settings is not None:
            logger.warning("QSettings already configured. Skipping re-configuration.")
            return

        app = QApplication.instance()
        if app is None:
            logger.error("Called configure when there was not a QApplication instance.")
            return

        self._settings = QSettings(app.organizationName(), app.applicationName())
        self._initializeDefaults()

    def _getQSettings(self) -> QSettings:
        """Returns insternal QSettings object, raising an error if not initialized."""
        if self._settings is None:
            raise RuntimeError(
                "Settings have not been configured for the application. "
                + "Call configureForApplication() after QApplication is initialized."
            )
        return self._settings

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
            self._getQSettings().value(
                "Split/split_text_entered",
                Settings.default_split_text_entered,
            ),
        )

    @split_text_entered.setter
    def split_text_entered(self, value: str) -> None:
        self._getQSettings().setValue("Split/split_text_entered", value)

    @property
    def split_values_display(self) -> str:
        r"""The symbol used to separate values when there are multiple items in a field.

        If set to \\, John Smith, Jane Doe would be shown as
        John Smith\\Jane Doe
        """
        return str(
            self._getQSettings().value(
                "Split/split_values_display",
                Settings.default_split_values_display,
            ),
        )

    @split_values_display.setter
    def split_values_display(self, value: str) -> None:
        self._getQSettings().setValue("Split/split_values_display", value)

    @property
    def split_values_at(self) -> str:
        """The symbol used when existing values should be split.

        For example, if an existing field is John Smith; Jane Doe,
        this should split it into separate values.
        """
        return str(
            self._getQSettings().value(
                "Split/split_values_at",
                Settings.default_split_values_at,
            ),
        )

    @split_values_at.setter
    def split_values_at(self, value: str) -> None:
        self._getQSettings().setValue("Split/split_values_at", value)

    default_tags: ClassVar[list[TagInfo]] = [
        TagInfo(
            display_name="Track",
            id3_key="TRCK",
            show_in_table=True,
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Title",
            id3_key="TIT2",
            show_in_table=True,
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Artist",
            id3_key="TPE1",
            show_in_table=True,
            editor_type=EditorType.MultipleText,
        ),
        TagInfo(
            display_name="Album Artist",
            id3_key="TPE2",
            show_in_table=True,
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Album",
            id3_key="TALB",
            show_in_table=True,
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Composer",
            id3_key="TCOM",
            show_in_table=True,
            editor_type=EditorType.MultipleText,
        ),
        TagInfo(
            display_name="Lyricist",
            id3_key="TEXT",
            show_in_table=True,
            editor_type=EditorType.MultipleText,
        ),
        TagInfo(
            display_name="Language",
            id3_key="TLAN",
            show_in_table=True,
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="BPM",
            id3_key="TBPM",
            show_in_table=True,
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Key",
            id3_key="TKEY",
            show_in_table=True,
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Involved People",
            id3_key="TIPL",
            show_in_table=True,
            editor_type=EditorType.PeopleValue,
        ),
        TagInfo(
            display_name="Musician Credits",
            id3_key="TMCL",
            show_in_table=True,
            editor_type=EditorType.PeopleValue,
        ),
        TagInfo(
            display_name="Sort Composer",
            id3_key="TSOC",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Conductor", id3_key="TPE3", editor_type=EditorType.SingleText
        ),
        TagInfo(display_name="Year", id3_key="TDRC", editor_type=EditorType.SingleText),
        TagInfo(
            display_name="Original Album",
            id3_key="TOAL",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Original Artist",
            id3_key="TOPE",
            editor_type=EditorType.MultipleText,
        ),
        TagInfo(
            display_name="Subtitle", id3_key="TIT3", editor_type=EditorType.SingleText
        ),
        TagInfo(
            display_name="Disc Number",
            id3_key="TPOS",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Set Subtitle",
            id3_key="TSST",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Sort Artist",
            id3_key="TSOP",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Sort Album Artist",
            id3_key="TSO2",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Genre", id3_key="TCON", editor_type=EditorType.MultipleText
        ),
        TagInfo(
            display_name="Publisher", id3_key="TPUB", editor_type=EditorType.SingleText
        ),
        TagInfo(
            display_name="Mood", id3_key="TMOO", editor_type=EditorType.MultipleText
        ),
        TagInfo(
            display_name="Display Composer",
            id3_key="TXXX:DISPLAY COMPOSER",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Release Date",
            id3_key="TXXX:RELEASE DATE",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Original Year",
            id3_key="TXXX:originalyear",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Scrobble Title",
            id3_key="TXXX:SCROBBLE TITLE",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Track Name",
            id3_key="TXXX:TRACK NAME",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Song Type",
            id3_key="TXXX:SONG TYPE",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Scrobble Album",
            id3_key="TXXX:SCROBBLE ALBUM",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Album Name",
            id3_key="TXXX:ALBUM NAME",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Album Type",
            id3_key="TXXX:ALBUM TYPE",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Album Version",
            id3_key="TXXX:ALBUM VERSION",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Scrobble Artist",
            id3_key="TXXX:SCROBBLE ARTIST",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Artist Shown",
            id3_key="TXXX:ARTIST SHOWN",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Display Artist",
            id3_key="TXXX:DISPLAY ARTIST",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Label",
            id3_key="TXXX:LABEL",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Performer",
            id3_key="TXXX:PERFORMER",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Remixer",
            id3_key="TXXX:REMIXER",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Occasion",
            id3_key="TXXX:OCCASION",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Keywords",
            id3_key="TXXX:KEYWORDS",
            editor_type=EditorType.SingleText,
        ),
        TagInfo(
            display_name="Tempo",
            id3_key="TXXX:TEMPO",
            editor_type=EditorType.SingleText,
        ),
    ]
    "Default values for known tags, if there are no user changes."

    @property
    def table_tags(self) -> list[SongTag]:
        """The tags shown in the main table."""
        if self._table_tags_cache is None:
            self._table_tags_cache = [
                SongTag(
                    display_name=tag.display_name,
                    id3_key=tag.id3_key,
                    editor_type=tag.editor_type,
                )
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
            SongTag(
                display_name=tag.display_name,
                id3_key=tag.id3_key,
                editor_type=tag.editor_type,
            )
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

        qsettings = self._getQSettings()

        qsettings.beginGroup(key)
        qsettings.remove("")
        qsettings.endGroup()

        qsettings.beginWriteArray(key)
        for index, tag in enumerate(vals):
            qsettings.setArrayIndex(index)
            qsettings.setValue("display_name", tag.display_name)
            qsettings.setValue("id3_key", tag.id3_key)
            qsettings.setValue("show_in_table", str(tag.show_in_table))
            qsettings.setValue("editor_type", tag.editor_type.name)
        qsettings.endArray()

    def _getArray(self, key: str) -> list[TagInfo]:
        """Convert the stored QSettings array into a Python list of tags.

        Args:
            key: The name of the array to read from settings.
        """
        qsettings = self._getQSettings()

        size = qsettings.beginReadArray(key)
        tags: list[TagInfo] = []
        for i in range(size):
            qsettings.setArrayIndex(i)
            display_name: str = str(qsettings.value("display_name"))
            id3_key: str = str(qsettings.value("id3_key"))
            show_in_table: bool = qsettings.value("show_in_table") == "True"
            editor_type_str: str = str(
                qsettings.value("editor_type", EditorType.Automatic.name)
            )
            editor_type_enum: EditorType = getattr(
                EditorType, editor_type_str, EditorType.Automatic
            )
            tags.append(
                TagInfo(
                    display_name=display_name,
                    id3_key=id3_key,
                    show_in_table=show_in_table,
                    editor_type=editor_type_enum,
                ),
            )
        qsettings.endArray()
        return tags

    def _initializeDefaults(self) -> None:
        """Set the default values for all settings, if they aren't already set."""
        qsettings = self._getQSettings()
        if not qsettings.contains("Split/split_text_entered"):
            self.split_text_entered = Settings.default_split_text_entered
        if not qsettings.contains("Split/split_values_display"):
            self.split_values_display = Settings.default_split_values_display
        if not qsettings.contains("Split/split_values_at"):
            self.split_values_at = Settings.default_split_values_at

        size = qsettings.beginReadArray("Tags/info_tags")
        qsettings.endArray()

        if not qsettings.contains("Tags/info_tags") and size == 0:
            logger.info("Setting info tags")
            self.info_tags = Settings.default_tags

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
