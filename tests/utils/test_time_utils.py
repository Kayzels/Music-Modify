from datetime import timedelta
from music_modify.utils.time_utils import formatTime

def test_formatTime():
    td1 = timedelta(hours=1, minutes=5, seconds=10.45)
    td2 = timedelta(weeks=1,days=3,hours=2,minutes=1,
                            seconds=12,milliseconds=9,microseconds=15)
    assert formatTime(td1) == "1 hour, 5 mins, 10.45 seconds"
    assert formatTime(td2) == "10 days, 2 hours, 1 min, 12.00 seconds"