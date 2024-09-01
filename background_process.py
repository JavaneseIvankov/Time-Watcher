import signal

import datetime_util as du
import session_managers as sm
import util


def main():
    util.register_sigterm()  # register process for sigterm handling

    duration = util.proc_read("duration")
    PID = util.get_process_id()
    proc_start_time = util.get_process_start_time(PID)

    util.proc_write("pid", PID)
    util.proc_write("proc_start_time", proc_start_time)

    while int(util.proc_read("proc_status")):
        remaining = du.parse_datetime(util.proc_read("target_time")) - du.time_now()
        status = int(util.proc_read("status"))
        surpassed = int(util.proc_read("surpassed"))
        if remaining <= du.TD_ZERO and status and not surpassed:
            print(remaining)
            print(PID)
            util.send_notification()
            util.play_sound()
            util.proc_write("surpassed", 1)
            # sm.finish_session(du.time_now())
            util.sleep(1)
        elif remaining >= du.TD_ZERO and status:
            print("running")
            util.sleep(1)
        else:
            print("idle")
            util.sleep(1)

    # util.post_process_cleanup()


main()
