"""Test configuration and fixtures for pytest.

These fixtures are available in all files in the `tests` folder.
"""

from collections.abc import Generator
import os
from os import PathLike
from pathlib import Path
import shutil
import tempfile

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication
import pytest

from music_modify.core.enums import EditorType
from music_modify.custom_types import TagInfo
from music_modify.prefs import Settings

NUM_TEMP_SONGS = 3
"The number of temp songs that should be created."


@pytest.fixture
def num_temp_songs() -> int:
    """Fixture for the number of temp songs, so tests can access this value."""
    return NUM_TEMP_SONGS


@pytest.fixture(scope="session")
def asset_folder(tmp_path_factory: pytest.TempPathFactory) -> Generator[str]:
    """The folder where temp songs should be created."""
    temp_dir = tmp_path_factory.mktemp("tmp_songs")
    yield str(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def song_path(tmp_path_factory: pytest.TempPathFactory) -> Generator[Path]:
    """Path for a single song for testing adding individual songs."""
    original_file = (Path(__file__).parent / "assets/test_song.mp3").absolute()
    temp_dir = tmp_path_factory.mktemp("tmp_song")
    temp_file = temp_dir / "test_song.mp3"
    yield shutil.copyfile(original_file, temp_file)
    shutil.rmtree(temp_dir)


@pytest.fixture
def image_bytes() -> bytes:
    """Fixture that returns the binary image data for the test image."""
    original_file = (Path(__file__).parent / "assets/test_image.jpg").absolute()
    with original_file.open("rb") as f:
        return f.read()


@pytest.fixture(scope="session")
def image_path(
    tmp_path_factory: pytest.TempPathFactory,
) -> Generator[Path]:
    """Fixture that returns a Path for an image."""
    original_file = (Path(__file__).parent / "assets/test_image.jpg").absolute()
    temp_dir = tmp_path_factory.mktemp("tmp_image")
    temp_image = temp_dir / "test_image.jpg"
    yield shutil.copyfile(original_file, temp_image)
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def image_path_no_extension(
    tmp_path_factory: pytest.TempPathFactory,
) -> Generator[Path]:
    """Fixture that returns a Path for an image."""
    original_file = (Path(__file__).parent / "assets/test_image.jpg").absolute()
    temp_dir = tmp_path_factory.mktemp("tmp_image")
    temp_image = temp_dir / "test_image"
    yield shutil.copyfile(original_file, temp_image)
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def song_paths(
    asset_folder: str,
) -> list[PathLike[str]]:
    """Fixture for the temp songs inside the assert folder."""
    original_file = (Path(__file__).parent / "assets/test_song.mp3").absolute()
    files: list[PathLike[str]] = []
    for i in range(1, NUM_TEMP_SONGS + 1):
        new_file = Path(asset_folder) / f"test_song_{i}.mp3"
        temp_file = shutil.copyfile(original_file, new_file)
        files.append(temp_file)
    return files


@pytest.fixture
def temp_settings() -> Generator[Settings]:
    """Fixture that creates a temporary folder for QSettings."""
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
def app_info(qapp: QApplication) -> tuple[str, str, str]:
    """Fixture that creates dummy values for app name and version."""
    org = "Test Kayzels"
    name = "Test Music Modify"
    version = "9.9.9"
    qapp.setOrganizationName(org)
    qapp.setApplicationName(name)
    qapp.setApplicationVersion(version)
    return (org, name, version)


@pytest.fixture
def info_tags() -> list[TagInfo]:
    """Fixture for tags that are used for a SongTableModel."""
    return [
        TagInfo(
            display_name="Title", id3_key="TIT2", editor_type=EditorType.SingleText
        ),
        TagInfo(
            display_name="Involved People",
            id3_key="TIPL",
            editor_type=EditorType.PeopleValue,
        ),
        TagInfo(
            display_name="Composer", id3_key="TCOM", editor_type=EditorType.MultipleText
        ),
    ]


@pytest.fixture
def song_with_tags_path(tmp_path: Path) -> Path:
    """Fixture providing unique copy of MP3 file with pre-existing tags."""
    original_file: Path = (
        Path(__file__).parent / "assets/test_song_with_tags.mp3"
    ).absolute()

    temp_file: Path = tmp_path / "test_song_with_tags_copy.mp3"

    shutil.copyfile(original_file, temp_file)
    return temp_file
