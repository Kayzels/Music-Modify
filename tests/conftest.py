from collections.abc import Generator
import os
from os import PathLike
from pathlib import Path
import shutil
import tempfile

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication
import pytest

from music_modify.prefs.prefs import Settings

NUM_TEMP_SONGS = 3


@pytest.fixture
def num_temp_songs() -> int:
    return NUM_TEMP_SONGS


@pytest.fixture(scope="session")
def asset_folder(tmp_path_factory: pytest.TempPathFactory) -> Generator[str]:
    temp_dir = tmp_path_factory.mktemp("tmp_songs")
    yield str(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def song_path(tmp_path_factory: pytest.TempPathFactory) -> Generator[Path]:
    original_file = (Path(__file__).parent / "assets/test_song.mp3").absolute()
    temp_dir = tmp_path_factory.mktemp("tmp_song")
    temp_file = temp_dir / "test_song.mp3"
    yield shutil.copyfile(original_file, temp_file)
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def song_paths(
    asset_folder: str,
) -> list[PathLike[str]]:
    original_file = (Path(__file__).parent / "assets/test_song.mp3").absolute()
    files: list[PathLike[str]] = []
    for i in range(1, NUM_TEMP_SONGS + 1):
        new_file = Path(asset_folder) / f"test_song_{i}.mp3"
        temp_file = shutil.copyfile(original_file, new_file)
        files.append(temp_file)
    return files


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


@pytest.fixture(scope="session")
def app_info(qapp: QApplication) -> tuple[str, str]:
    name = "Test Music Modify"
    version = "9.9.9"
    qapp.setApplicationName(name)
    qapp.setApplicationVersion(version)
    return (name, version)
