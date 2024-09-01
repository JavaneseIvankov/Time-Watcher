""" Reusable utility that don't require datetime module, also contain constants (which only used in this module)"""

import os
import signal
import subprocess
import time

import constants as const
import psutil

const_pool = const.CONSTANTS_POOL


def sleep(sec: float):
    time.sleep(sec)


def play_sound(path: str | None = None):
    if not path:
        path = const.SOUND_PATH
    subprocess.Popen(["mpg123", "-q", f"{path}"])


def send_notification():
    subprocess.run(["dunstify", "-r", "9999", f"Time's up!"])


def retry_timeout(interval: int, attempt_timeout: int, callback):
    for i in range(attempt_timeout):
        if callback():
            return True
        time.sleep(interval)
    return False


def append_file(path: str, value: str):
    with open(file=path, mode="a") as f:
        f.write(value)


def write_specific_line(
    path: str, line_number: int, value: str
):  # only ovw not creating new line
    with open(file=path, mode="r") as f:
        lines = f.readlines()

    lines[line_number] = value + "\n"

    with open(file=path, mode="w") as f:
        f.writelines(lines)


def get_from_line(path: str, line_number: int) -> str:
    with open(file=path, mode="r") as f:
        lines = f.readlines()

    return lines[line_number]


def get_lines(path: str) -> list:
    with open(file=path, mode="r") as f:
        lines = f.readlines()
        return lines


def proc_read(attribute: str) -> str:
    try:
        return get_from_line(
            path=const.PROC_FILE_PATH, line_number=const_pool[attribute]
        ).replace("\n", "")
    except KeyError as e:
        print(f"Invalid parameter, e: {e}")
        return ""


def proc_write(attribute: str, value):
    try:
        value = str(value)
    except Exception as e:
        print(e)
        return
    try:
        write_specific_line(
            path=const.PROC_FILE_PATH, line_number=const_pool[attribute], value=value
        )
    except KeyError as e:
        print(f"Invalid parameter, e: {e}")


def get_process_id():
    return os.getpid()


def get_process_start_time(pid) -> float | None:
    if pid == -1:
        print("It seems that process hasn't started yet")
        return

    try:
        process = psutil.Process(pid)
        start_time = process.create_time()
        return start_time
    except psutil.NoSuchProcess:
        # print(f"get_process_start_time: No process found with PID {pid}.")
        pass
    except psutil.AccessDenied:
        print(f"Access denied to information about process with PID {pid}.")
    except Exception as e:
        print(f"get_process_start_time: An error occurred: {e}")


def start_proc() -> int:
    try:
        proc_write("proc_status", 1)
        subprocess.run(
            f"nohup python3 {const.PROC_PATH} > {const.PROC_LOG_PATH} 2>&1 &",
            shell=True,
        )
        return 0
    except Exception as e:
        print(f"Error occured: {e}")
        proc_write("proc_status", 0)
        return 1


def terminate_proc(pid):
    if pid == -1:  # early return for pid -1, avoiding any critical unwanted effect.
        return

    try:
        proc_write("proc_status", 0)
        time.sleep(2)
        os.kill(pid, 15)
        print(f"Termination signal (SIGTERM) sent to process with PID {pid}.")
    except ProcessLookupError:
        # print(f"force_terminate: No process found with PID {pid}.")
        pass
    except PermissionError:
        print(f"Permission denied to terminate process with PID {pid}.")
    except Exception as e:
        print(f"terminate: An error occurred: {e}")


def post_process_cleanup():
    proc_write("proc_status", 0)
    proc_write("surpassed", 0)
    proc_write("status", 0)
    proc_write("pid", -1)
    proc_write("proc_start_time", 0)


def term_handler(
    signum, stack
):  # NOTE: This still leave some garbage values in the proc file
    post_process_cleanup()


def register_sigterm():
    signal.signal(signal.SIGTERM, term_handler)
