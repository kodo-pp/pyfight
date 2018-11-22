import time
from pygame.time import Clock

class ExitLoop(Exception):
    pass


def run_with_fps(fps, func):
    clock = Clock()
    try:
        while True:
            func()
            clock.tick(fps)
    except ExitLoop:
        return

