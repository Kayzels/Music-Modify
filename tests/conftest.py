from collections.abc import Generator
import os
from os import PathLike
from pathlib import Path
import tempfile

from PySide6.QtCore import QSettings
import pytest

from music_modify.prefs.prefs import Settings


@pytest.fixture
def song_path() -> Path:
    return Path("tests/assets/test_song_1.mp3").absolute()


@pytest.fixture
def song_paths() -> list[PathLike[str]]:
    return [
        Path("tests/assets/test_song_1.mp3").absolute(),
        Path("tests/assets/test_song_2.mp3").absolute(),
        Path("tests/assets/test_song_3.mp3").absolute(),
    ]


@pytest.fixture
def asset_folder() -> PathLike[str]:
    return Path("tests/assets/").absolute()


@pytest.fixture
def temp_settings() -> Generator[Settings]:
    # Create a temp file and keep it until the fixture is done
    fd, path = tempfile.mkstemp()
    os.close(fd)

    try:
        settings = QSettings(path, QSettings.Format.IniFormat)
        test_settings = Settings(settings)
        yield test_settings
    finally:
        Path(path).unlink()
