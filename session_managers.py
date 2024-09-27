import datetime as d

import datetime_util as du
import session_logger as sl
import util


def start_session(duration: int, start_time: d.datetime, target_time: d.datetime):
    PID = int(util.proc_read("pid"))
    valid_proc_start_time = float(util.proc_read("proc_start_time"))

    proc_start_time = util.get_process_start_time(
        PID
    )  # this variable value will be None if the PID is invalid

    if (
        not proc_start_time
        or (proc_start_time != valid_proc_start_time)
        or valid_proc_start_time == "0"
    ):
        # possible invalid states for the background_process
        util.proc_write("status", 1)
        util.proc_write("surpassed", 0)
        print("Starting new background process...")
        return_code = util.start_proc()
    else:
        util.proc_write("status", 1)
        util.proc_write("surpassed", 0)
        return_code = 0
        print("Using existing background process")

    if return_code == 1:  # set status to 0 if proc failed to start
        util.proc_write("status", 0)
        util.proc_write("surpassed", 1)
        print("Oops! Something went wrong, cannot start background process")
    else:
        util.proc_write("duration", duration)
        util.proc_write("start_time", start_time)
        util.proc_write("target_time", target_time)
        util.sleep(0.5)
        PID = int(util.proc_read("pid"))
        print(f"Background process running with PID {PID}")


def terminate_session():
    PID = int(util.proc_read("pid"))
    valid_proc_start_time = float(util.proc_read("proc_start_time"))
    proc_start_time = util.get_process_start_time(PID)

    if proc_start_time == valid_proc_start_time:
        util.terminate_proc(PID)
        print("Background process sucessfully terminated")
        util.post_process_cleanup()
    else:
        print(
            f"Associated background process with PID {PID}, is invalid, process.txt might be corrupt or invalid"
        )


def finish_session(time_now: d.datetime):
    target_time = du.parse_datetime(util.proc_read("target_time"))
    start_time = du.parse_datetime(util.proc_read("start_time"))
    offset = time_now - target_time
    time_spent = target_time - start_time + offset

    util.proc_write("status", 0)
    util.proc_write("finish_time", time_now)
    util.proc_write("offset", offset.total_seconds())
    util.proc_write("time_spent", time_spent.total_seconds())

    sl.log_session()

    print(
        f"You've finished a session, time spent: {du.substract_time(start_time, time_now)}"
    )


def pause_session():
    util.proc_write("status", 0)
    pass
