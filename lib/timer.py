import time


class Time_D:
    def __init__(self):
        self.start = time.time()
        self.last = self.start

    def delta(self):
        now = time.time()
        delta = now - self.last
        self.last = now
        return delta

    def elapsed(self):
        now = time.time()
        return now - self.start

    def current(self):
        return time.time()
