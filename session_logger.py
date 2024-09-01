from copy import deepcopy

import constants as const
import util

# format specifiers (fs)
fs = {
    "%st": "start_time",
    "%ft": "finish_time",
    "%tt": "target_time",
    "%d": "duration",
    "%o": "offset",
    "%ts": "time_spent",
}
custom_template = const.CUSTOM_TEMPLATE
# chosen_template = const.CHOSEN_TEMPLATE

template = {
    "short": f"%st - %ft (%ts) short",
    "verbose": f"%st - %ft (target dur: %d | offset: %o) verbose",
    "custom": f"{custom_template}",
}


def timedelta_formatter():
    pass


def patch_fs():
    temp = deepcopy(fs)
    for k, v in fs.items():
        temp[k] = util.proc_read(v)
    return temp


def log_write():
    pass


def load_template(_chosen: str) -> str | None:
    try:
        temp = template[_chosen]
    except KeyError:
        print("[load_template] Invalid choice")
        return
    data = patch_fs()
    out = temp
    for k, v in data.items():
        out = out.replace(k, v)
    return out


def log_session():
    out = load_template(util.proc_read("chosen_template"))
    return out


"[%st] -> [%ft] :: Goal duration - %d :: Offset - %o"
