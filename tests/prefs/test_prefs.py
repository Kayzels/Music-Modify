import os
import tempfile

import pytest
from PySide6.QtCore import QSettings

from music_modify.custom_types import SongTag, TagInfo
from music_modify.prefs.prefs import _Settings  # pyright: ignore[reportPrivateUsage]


@pytest.fixture
def temp_settings():
    # Create a temp file and keep it until the fixture is done
    fd, path = tempfile.mkstemp()
    os.close(fd)

    try:
        settings = QSettings(path, QSettings.Format.IniFormat)
        test_settings = _Settings(settings)
        yield test_settings
    finally:
        os.remove(path)


def set_split_values(settings: _Settings):
    settings.split_text_entered = "-"
    settings.split_values_at = "-"
    settings.split_values_display = "-"


def set_tag_values(settings: _Settings):
    settings.info_tags = [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]


def test_init(temp_settings: _Settings):
    # Test _initializeDefaults
    assert temp_settings.split_text_entered == _Settings.default_split_text_entered
    assert temp_settings.split_values_display == _Settings.default_split_values_display
    assert temp_settings.split_values_at == _Settings.default_split_values_at
    assert temp_settings.info_tags == _Settings.default_tags

    # Test all_tags
    assert temp_settings.all_tags == [
        SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
        for tag in _Settings.default_tags
    ]

    # Test table tags
    assert temp_settings.table_tags == [
        SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
        for tag in _Settings.default_tags
        if tag.show_in_table
    ]


def test_set_split(temp_settings: _Settings):
    set_split_values(temp_settings)
    assert temp_settings.split_text_entered == "-"
    assert temp_settings.split_values_at == "-"
    assert temp_settings.split_values_display == "-"


def test_set_tag(temp_settings: _Settings):
    set_tag_values(temp_settings)
    assert temp_settings.info_tags == [
        TagInfo(id3_key="TIT2", display_name="Title", show_in_table=True),
        TagInfo(id3_key="TPE2", display_name="Artist", show_in_table=False),
    ]
    assert temp_settings.table_tags == [SongTag(id3_key="TIT2", display_name="Title")]


def test_resetSplit(temp_settings: _Settings):
    set_split_values(temp_settings)
    temp_settings.resetSplit()
    assert temp_settings.split_text_entered == _Settings.default_split_text_entered
    assert temp_settings.split_values_at == _Settings.default_split_values_at
    assert temp_settings.split_values_display == _Settings.default_split_values_display


def test_resetTags(temp_settings: _Settings):
    set_tag_values(temp_settings)
    temp_settings.resetTags()

    # Test all_tags
    assert temp_settings.all_tags == [
        SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
        for tag in _Settings.default_tags
    ]

    # Test table tags
    assert temp_settings.table_tags == [
        SongTag(display_name=tag.display_name, id3_key=tag.id3_key)
        for tag in _Settings.default_tags
        if tag.show_in_table
    ]
