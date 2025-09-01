"""Tests for Settings."""

from music_modify.custom_types import SongTag, TagInfo
from music_modify.prefs.prefs import Settings


def _set_split_values(settings: Settings) -> None:
    settings.split_text_entered = "-"
    settings.split_values_at = "-"
    settings.split_values_display = "-"


def _set_tag_values(settings: Settings) -> None:
    settings.info_tags = [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]


def test_Settings_init(temp_settings: Settings) -> None:
    """Test that a Settings object is created correctly."""
    # Test _initializeDefaults
    assert temp_settings.split_text_entered == Settings.default_split_text_entered
    assert temp_settings.split_values_display == Settings.default_split_values_display
    assert temp_settings.split_values_at == Settings.default_split_values_at
    assert temp_settings.info_tags == Settings.default_tags

    # Test all_tags
    assert temp_settings.all_tags == [
        SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
        for tag in Settings.default_tags
    ]

    # Test table tags
    assert temp_settings.table_tags == [
        SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
        for tag in Settings.default_tags
        if tag.show_in_table
    ]


def test_Settings_set_split(temp_settings: Settings) -> None:
    """Test that setting the properties for split values works."""
    _set_split_values(temp_settings)
    assert temp_settings.split_text_entered == "-"
    assert temp_settings.split_values_at == "-"
    assert temp_settings.split_values_display == "-"


def test_Settings_set_tag(temp_settings: Settings) -> None:
    """Test that settings the properties for tags works."""
    _set_tag_values(temp_settings)
    assert temp_settings.info_tags == [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]
    assert temp_settings.table_tags == [SongTag(id3_key="TIT2", display_name="Title")]


def test_Settings_resetSplit(temp_settings: Settings) -> None:
    """Test that resetting split values changes back to the original default ones."""
    _set_split_values(temp_settings)
    temp_settings.resetSplit()
    assert temp_settings.split_text_entered == Settings.default_split_text_entered
    assert temp_settings.split_values_at == Settings.default_split_values_at
    assert temp_settings.split_values_display == Settings.default_split_values_display


def test_resetTags(temp_settings: Settings) -> None:
    """Test that resetting tags changes back to the original default ones."""
    _set_tag_values(temp_settings)
    temp_settings.resetTags()

    # Test all_tags
    assert temp_settings.all_tags == [
        SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
        for tag in Settings.default_tags
    ]

    # Test table tags
    assert temp_settings.table_tags == [
        SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
        for tag in Settings.default_tags
        if tag.show_in_table
    ]
