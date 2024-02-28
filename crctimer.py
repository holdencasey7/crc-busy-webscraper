import threading
import time
import scrape
import crcdb

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
    interval = 60*5
    def timer(self):
        scrape_and_insert()


def scrape_and_insert():
    # Scrape CRC site
    busy_object = scrape.get_busy_object()

    # Insert the data
    crcdb.insert_data(crcdb.db, crcdb.table, busy_object)