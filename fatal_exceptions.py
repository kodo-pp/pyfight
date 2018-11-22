from os import _exit
from traceback import print_exc

def fatal_exceptions(func):
    def resulting_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException:
            print_exc()
            _exit(1)
    return resulting_func

