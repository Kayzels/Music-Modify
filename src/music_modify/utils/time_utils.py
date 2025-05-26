import datetime


def formatTime(time_to_format: datetime.timedelta, decimal_places: int = 2) -> str:
    """Converts a timedelta to a readable string"""
    time_string = ""
    hours, mins, seconds = str(time_to_format).split(":")
    seconds_split = seconds.split(".")
    seconds = seconds_split[0] + "." + seconds_split[1][:decimal_places]
    if hours == "0":
        if mins == "00":
            time_string = f"{seconds} seconds"
        else:
            time_string = f"{mins} mins, {seconds} seconds"
    else:
        time_string = f"{hours} hours, {mins} mins, {seconds} seconds"
    return time_string
