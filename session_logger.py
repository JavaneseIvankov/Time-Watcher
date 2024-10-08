from copy import deepcopy

import constants as const
import session_log_parser as slp
import util


def tbi():
    # Implement config sourcing
    pass


# format specifiers (fs)
fs = {
    "%st": "start_time",
    "%ft": "finish_time",
    "%tt": "target_time",
    "%d": "duration",
    "%o": "offset",
    "%ts": "time_spent",
}

chosen_path = "/home/arundaya/Documents/Workspace/General_Vault/99 Meta-Functional/992 Pomodoro Logs/992-1 Pomodoro Log.md"
fallback_path = const.SESSION_LOG_PATH
custom_template = const.CUSTOM_TEMPLATE


template = {
    "short": f"%st - %ft (%ts) short",
    "verbose": f"%st - %ft (target dur: %d | offset: %o) verbose",
    "custom": f"{custom_template}",
}


def timedelta_formatter():
    pass


def patch_fs():
    temp = deepcopy(fs)
    for k, v in fs.items():  # key = fs; value = fullspec
        # read values in proc.txt and pipe it to parser
        temp[k] = slp.parserDispatch(v, util.proc_read(v))
    return temp


def load_template(_chosen: str) -> str:
    try:
        temp = template[_chosen]
    except KeyError:
        print("[load_template] Invalid choice")
        return ""
    data = patch_fs()
    out = temp
    for k, v in data.items():
        out = out.replace(k, v)
    return out


def log_session():
    # load_config()
    buff = ""
    out = load_template(util.proc_read("chosen_template")) + "\n"
    path = chosen_path

    buff += prefix_hooks()
    buff += out
    buff += suffix_hooks()

    util.append_file(path, buff)
    print("Session logged")


def prefix_hooks(*args) -> str:
    buff = ""
    for f in args:
        buff += f() + "\n"
    return buff


def suffix_hooks(*args):
    buff = ""
    for f in args:
        buff += f() + "\n"
    return buff


"[%st] -> [%ft] :: Goal duration - %d :: Offset - %o"
