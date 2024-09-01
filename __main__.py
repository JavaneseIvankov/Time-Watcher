import argparse

import datetime_util as du
import session_managers as sm
import util


def parse_raw_duration(args) -> tuple[int, int]:
    minutes = str()
    seconds = str()
    temp = str()

    for c in args.raw_duration:
        if c == "m":
            minutes += temp
            temp = str()
            continue
        if c == "s":
            seconds += temp
            temp = str()
            continue
        temp += c

        if not minutes:
            minutes = "0"
        if not seconds:
            seconds = "0"

    return (int(minutes), int(seconds))


def main():
    parser = argparse.ArgumentParser(
        prog="Pomo-CLI",
        description="Pomodoro program with CLI interface, focuses on simplicity and effectiveness",
    )
    parser.add_argument(
        "-Lt", "--loadtemplate", dest="load_signal", action="store_true"
    )
    parser.add_argument("-ts", "--timeset", dest="raw_duration", action="store")
    parser.add_argument("-s", "--start", dest="start_flag", action="store_true")
    parser.add_argument("-f", "--finish", dest="finish_flag", action="store_true")
    parser.add_argument("-t", "--terminate", dest="terminate_flag", action="store_true")
    parser.add_argument("-p", "--pause", dest="pause_flag", action="store_true")

    args = parser.parse_args()
    if args.raw_duration:
        parsed_duration = parse_raw_duration(args)

        try:
            min = parsed_duration[0]
        except ValueError:
            min = 0

        try:
            sec = parsed_duration[1]
        except ValueError:
            sec = 0

    else:
        min = 0
        sec = int(util.proc_read("duration"))

    start_time = du.set_start(seconds=-1)
    duration = du.get_timedelta_seconds(min, sec)
    int_duration = min * 60 + sec
    target_time = start_time + duration

    start_flag = args.start_flag
    finish_flag = args.finish_flag
    pause_flag = args.pause_flag
    terminate_flag = args.terminate_flag

    du.time_set(int_duration)

    status = util.proc_read("status")

    # Input Routing
    if start_flag:
        if status == "1":
            ovw = input(
                "Currently you already have running session, want to overwrite? (y/n)\n\t:"
            )
            if ovw.lower() == "y":
                sm.start_session(int_duration, start_time, target_time)
            else:
                exit()
        else:
            sm.start_session(int_duration, start_time, target_time)

    elif finish_flag:
        if status == "1":
            sm.finish_session(du.time_now())
        else:
            print("You currently have no running session")
            exit()

    elif terminate_flag:
        if util.proc_read("pid") != "-1":
            time_now = du.time_now()
            if status == "1":
                sm.finish_session(time_now)
            sm.terminate_session()
        else:
            print("You currently have no running session")
            exit()

    elif pause_flag:
        sm.pause_session()


main()
