"""Tests for time utilities."""

from datetime import timedelta

import pytest

from music_modify.utils.time_utils import (
    convertSecondsAndMicroseconds,
    formatTime,
    getTimeDict,
)

_timedelta1 = timedelta(hours=1, minutes=5, seconds=10.45)
_timedelta2 = timedelta(
    weeks=1,
    days=3,
    hours=2,
    minutes=1,
    seconds=12,
    milliseconds=9,
    microseconds=15,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(
            _timedelta1,
            {
                "days": 0,
                "hours": 1,
                "minutes": 5,
                "seconds": 10,
                "microseconds": 450_000,
            },
        ),
        pytest.param(
            _timedelta2,
            {
                "days": 10,
                "hours": 2,
                "minutes": 1,
                "seconds": 12,
                "microseconds": 9015,
            },
        ),
    ],
)
def test_getTimeDict(value: timedelta, expected: dict[str, int]) -> None:
    """Test that timedelta values are correctly converted to dicts."""
    assert getTimeDict(value) == expected


@pytest.mark.parametrize(
    ("seconds", "microseconds", "decimal_places", "expected"),
    [
        pytest.param(0, 0, None, None, id="no_seconds_or_microseconds"),
        pytest.param(1, 0, None, "1 second", id="single_second"),
        pytest.param(2, 0, None, "2 seconds", id="multiple_seconds"),
        pytest.param(0, 20, None, None, id="no_seconds_low_microseconds"),
        pytest.param(0, 9015, None, "0.01 seconds", id="microseconds_rounded"),
        pytest.param(
            2, 100_000, None, "2.1 seconds", id="seconds_microseconds_rounded"
        ),
        pytest.param(
            2, 115_000, 2, "2.12 seconds", id="seconds_microseconds_rounded_2_places"
        ),
        pytest.param(
            2, 115_000, 3, "2.115 seconds", id="seconds_microseconds_rounded_3_places"
        ),
    ],
)
def test_convertSecondsAndMicroseconds(
    seconds: int, microseconds: int, decimal_places: int | None, expected: str | None
) -> None:
    """Test that seconds and microseconds are rounded and returned correctly."""
    if decimal_places is not None:
        result = convertSecondsAndMicroseconds(seconds, microseconds, decimal_places)
    else:
        result = convertSecondsAndMicroseconds(seconds, microseconds)
    assert result == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(_timedelta1, "1 hour, 5 mins, 10.45 seconds", id="no_day"),
        pytest.param(
            _timedelta2, "10 days, 2 hours, 1 min, 12.01 seconds", id="with_day"
        ),
    ],
)
def test_formatTime(value: timedelta, expected: str) -> None:
    """Test that a timedelta is formatted in the correct way."""
    assert formatTime(value) == expected
