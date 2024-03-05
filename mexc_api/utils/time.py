import time


def epoch_time() -> int:
    return int(time.time())

def timestamp() -> int:
    return int(time.time() * 1000)
