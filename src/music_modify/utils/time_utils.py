"""Module for utilities related to working with datetime values."""

import datetime
import re


def formatTime(time_to_format: datetime.timedelta, decimal_places: int = 2) -> str:
    """Converts a timedelta to a readable string"""
    delta_str = str(time_to_format)
    days = 0
    if "day" in delta_str:
        match = re.match(r"(\d+) day[s]?, (.+)", delta_str)
        if match:
            days = int(match.group(1))
            time_part = match.group(2)
        else:
            time_part = delta_str
    else:
        time_part = delta_str

    hours, mins, seconds = time_part.split(":")
    seconds_split = seconds.split(".")
    seconds = seconds_split[0]
    if len(seconds_split) > 1:
        seconds += "." + seconds_split[1][:decimal_places]

    parts: list[str] = []
    if days:
        if days == 1:
            parts.append("1 day")
        else:
            parts.append(f"{days} days")
    if hours != "0":
        hour_int = int(hours)
        if hour_int == 1:
            parts.append("1 hour")
        else:
            parts.append(f"{hour_int} hours")
    if mins != "00":
        min_int = int(mins)
        if min_int == 1:
            parts.append("1 min")
        else:
            parts.append(f"{int(mins)} mins")
    parts.append(f"{seconds} seconds")
    return ", ".join(parts)
