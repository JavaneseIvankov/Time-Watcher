import os
import constants as const
import datetime_util as du
import util
from time import sleep

sec = 3
min = 0

start = du.set_start()
dur = du.calculate_delta(min, sec)
sleep_time = 1

if sec == 0:
    sleep_time = 55
i = 0

pid = os.getpid()
print(pid)


def action():
    util.play_sound(const.SOUND_PATH)
    util.send_notification()


while True:
    end = du.time_now()
    action()
    start = end
    sleep(min * 60 + sec)
