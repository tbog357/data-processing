import time


def time_since(start_time):
    return time.time() - start_time

def join_strings_by_vertical_bar(*strings):
    return "|".join(strings)

def delay(seconds):
    time.sleep(seconds)