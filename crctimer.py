import threading
import time
from datacollection import scrape_and_insert

class Timer(threading.Thread):

    def __init__(self):
        self._timer_runs = threading.Event()
        self._timer_runs.set()
        super().__init__()

    def run(self):
        while self._timer_runs.is_set():
            self.timer()
            time.sleep(self.__class__.interval)

    def stop(self):
        self._timer_runs.clear()


class CRC_Timer(Timer):
    interval = 60*1
    def timer(self):
        scrape_and_insert()
