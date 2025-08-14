"""Module for utilities related to working with datetime values."""

import datetime
import math
from typing import TypedDict

from music_modify.utils.string_utils import singularPlural

MINS_IN_HOUR = 60
SECONDS_IN_MIN = 60
SECONDS_IN_HOUR = SECONDS_IN_MIN * MINS_IN_HOUR
MICROSECONDS_IN_SECOND = 1_000_000.0


class _TimeDict(TypedDict):
    days: int
    hours: int
    minutes: int
    seconds: int
    microseconds: int


def getTimeDict(time_to_format: datetime.timedelta) -> _TimeDict:
    """Calculate the various time fields from a timedelta object."""
    days = time_to_format.days
    seconds_remaining = time_to_format.seconds
    hours, seconds_remaining = divmod(seconds_remaining, SECONDS_IN_HOUR)
    minutes, seconds = divmod(seconds_remaining, SECONDS_IN_MIN)
    microseconds = time_to_format.microseconds

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "microseconds": microseconds,
    }


def convertSecondsAndMicroseconds(
    seconds: int,
    microseconds: int,
    decimal_places: int = 2,
) -> str | None:
    """Create a string representation of the seconds and microseconds together.

    If both are 0, returns `None`.
    Otherwise, returns a string of the form `seconds.microseconds`
    """
    if microseconds == 0:
        if seconds == 0:
            return None
        return singularPlural(seconds, "second")
    microsecond_calc = round(microseconds / MICROSECONDS_IN_SECOND, decimal_places)
    if math.isclose(microsecond_calc, 0.0):
        return None
    second_calc = seconds + microsecond_calc
    return f"{second_calc} seconds"


def formatTime(time_to_format: datetime.timedelta, decimal_places: int = 2) -> str:
    """Converts a timedelta to a readable string."""
    time_dict = getTimeDict(time_to_format)
    parts: list[str] = []
    if (days := time_dict["days"]) > 0:
        parts.append(singularPlural(days, "day"))
    if (hours := time_dict["hours"]) > 0:
        parts.append(singularPlural(hours, "hour"))
    if (mins := time_dict["minutes"]) > 0:
        parts.append(singularPlural(mins, "min"))

    seconds_str = convertSecondsAndMicroseconds(
        time_dict["seconds"],
        time_dict["microseconds"],
        decimal_places,
    )
    if seconds_str:
        parts.append(seconds_str)

    return ", ".join(parts)
