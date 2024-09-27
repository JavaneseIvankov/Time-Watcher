from os import path
from pathlib import Path

CUSTOM_TEMPLATE = "[%st] -> [%ft] :: Goal duration - %d :: Time spent - %ts"


# Path(s) constants
ROOT_DIR = Path(__file__).parent
SOUND_PATH = f"{ROOT_DIR}/default-sound.mp3"
FALLBACK_SESSION_LOG_PATH = f"{path.join(Path.home(), 'timer_log.txt')}"
PROC_FILE_PATH = f"{ROOT_DIR}/process.txt"
PROC_PATH = f"{ROOT_DIR}/background_process.py"
PROC_LOG_PATH = f"{ROOT_DIR}/process_log.log"

# Line number constants for proc file (DO NOT CHANGE)
CHOSEN_TEMPLATE = 0  # default val= custom
SESSION_LOG_PATH = 1  # default val= 0

PID = 2  # default val= -1
PROC_START_TIME = 3  # default val= 0
PROC_STATUS = 4  # default val= 0

SURPASSED = 5  # default val= 0
STATUS = 6  # default val= 0
DURATION = 7  # default val= 0
START_TIME = 8  # default val= 0
TARGET_TIME = 9  # default val= 0

OFFSET = 10  # default val= 0
FINISH_TIME = 11  # default val= 0
TIME_SPENT = 12

CONSTANTS_POOL = {
    "chosen_template": CHOSEN_TEMPLATE,
    "pid": PID,
    "proc_start_time": PROC_START_TIME,
    "proc_status": PROC_STATUS,
    "surpassed": SURPASSED,
    "status": STATUS,
    "duration": DURATION,
    "start_time": START_TIME,
    "target_time": TARGET_TIME,
    "offset": OFFSET,
    "finish_time": FINISH_TIME,
    "time_spent": TIME_SPENT,
}
