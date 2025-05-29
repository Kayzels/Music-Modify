from os import PathLike
from pathlib import Path

import pytest


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
