"""Tests for time utilities."""

from datetime import timedelta

from music_modify.utils.time_utils import (
    convertSecondsAndMicroseconds,
    formatTime,
    getTimeDict,
)


def test_getTimeDict() -> None:
    """Test that timedelta values are correctly converted to dicts."""
    td1 = timedelta(hours=1, minutes=5, seconds=10.45)
    assert getTimeDict(td1) == {
        "days": 0,
        "hours": 1,
        "minutes": 5,
        "seconds": 10,
        "microseconds": 450_000,
    }
    td2 = timedelta(
        weeks=1,
        days=3,
        hours=2,
        minutes=1,
        seconds=12,
        milliseconds=9,
        microseconds=15,
    )
    assert getTimeDict(td2) == {
        "days": 10,
        "hours": 2,
        "minutes": 1,
        "seconds": 12,
        "microseconds": 9015,
    }


def test_convertSecondsAndMicroseconds() -> None:
    """Test that seconds and microseconds are rounded and returned correctly."""
    assert convertSecondsAndMicroseconds(0, 0) is None
    assert convertSecondsAndMicroseconds(1, 0) == "1 second"
    assert convertSecondsAndMicroseconds(2, 0) == "2 seconds"
    assert convertSecondsAndMicroseconds(0, 20) is None
    assert convertSecondsAndMicroseconds(0, 9015) == "0.01 seconds"
    assert convertSecondsAndMicroseconds(2, 100_000) == "2.1 seconds"
    assert convertSecondsAndMicroseconds(2, 107_000, 2) == "2.11 seconds"
    assert convertSecondsAndMicroseconds(2, 105_000, 3) == "2.105 seconds"


def test_formatTime() -> None:
    """Test that a timedelta is formatted in the correct way."""
    td1 = timedelta(hours=1, minutes=5, seconds=10.45)
    td2 = timedelta(
        weeks=1,
        days=3,
        hours=2,
        minutes=1,
        seconds=12,
        milliseconds=9,
        microseconds=15,
    )
    assert formatTime(td1) == "1 hour, 5 mins, 10.45 seconds"
    assert formatTime(td2) == "10 days, 2 hours, 1 min, 12.01 seconds"
