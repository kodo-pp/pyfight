import time

class ExitLoop(Exception):
    pass


def run_with_fps(fps, func):
    time_per_frame = 1.0 / fps
    last_time = 0
    try:
        while True:
            cur_time = time.time()
            diff = last_time + time_per_frame - cur_time
            if diff > 0:
                time.sleep(diff)
            last_time = cur_time
            func()
    except ExitLoop:
        return

