import time


def time_since(start_time):
    return time.time() - start_time

def join_strings(*elements):
    return "|".join(elements)

def delay(seconds):
    time.sleep(seconds)