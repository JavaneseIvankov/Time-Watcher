"""
Parser class for friendlier session log output.
"""


def format_time(hours: int, minutes: int, seconds: int):
    buff = ""
    if hours:
        buff += f"{hours}h"
        buff += f"{minutes}m"
        buff += f"{seconds}s"
    elif minutes:
        buff += f"{minutes}m"
        buff += f"{seconds}s"
    elif seconds:
        buff += f"{seconds}s"
    return buff


def parserDispatch(key: str, val: str) -> str:
    callbacks = {
        "start_time": parserDatetime,
        "finish_time": parserDatetime,
        "target_time": parserDatetime,
        "offset": parserTotalSeconds,
        "time_spent": parserTotalSeconds,
        "duration": parserDuration,
    }
    return callbacks[key](val)


def parserDatetime(datetime: str) -> str:
    datetime = datetime.split(".")[0]
    return datetime


def parserDeltatime(deltatime: str) -> str:
    temp = deltatime.split(":")
    hours = int(temp[0])
    minutes = int(temp[1])
    seconds = int(temp[2].split(".")[0])
    return format_time(hours, minutes, seconds)


def parserDuration(total_seconds: str | int) -> str:
    total_seconds = int(total_seconds)
    hours = int(total_seconds / 3600)
    minutes = int(total_seconds % 3600 / 60)
    seconds = int(total_seconds % 60)
    return format_time(hours, minutes, seconds)


def parserTotalSeconds(total_seconds: str) -> str:
    stripped = total_seconds.split(".")[0]
    return parserDuration(int(stripped))
