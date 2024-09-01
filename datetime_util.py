""" Reusable methods that require datetime module """

import datetime as d

import util

date = d.datetime(d.MINYEAR, 1, 1)  # Global object
TD_ZERO = d.timedelta(0)


def time_now():
    return date.now()


def set_start(
    hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0
) -> d.datetime:
    return date.now() + d.timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        milliseconds=milliseconds,
        microseconds=microseconds,
    )


def get_timedelta_seconds(minute: int = 0, second: int = 0) -> d.timedelta:
    total_in_seconds = minute * 60 + second
    return d.timedelta(days=0, seconds=total_in_seconds)


def substract_time(start: d.datetime | str, end: d.datetime | str) -> d.timedelta:
    if isinstance(start, str):
        start = parse_datetime(start)
    if isinstance(end, str):
        end = parse_datetime(end)
    return end - start


def track_offset(start: d.datetime | str, end: d.datetime | str, delta: d.timedelta):
    substracted = substract_time(start, end)
    return substracted - delta


def parse_datetime(datetime_string: str) -> d.datetime:
    return date.strptime(datetime_string, "%Y-%m-%d %H:%M:%S.%f")


def foo():
    pass


def time_set(seconds: int):
    util.proc_write("duration", seconds)
