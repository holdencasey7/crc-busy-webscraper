import scrape
import crcdb
import crctimer
import time
import datetime
import schedule

def collect_without_existing_db(length=15):
    """Create a default database, then collect data for specified time"""

    # Create db and drop tables if exist
    crcdb.create_db_and_drop()
    collect(length)
    

def collect(length=15):
    """Collect data for specified time"""

    # Repeat every 1 minute
    crc_timer = crctimer.CRC_Timer()
    crc_timer.start()
    time.sleep(length)
    crc_timer.stop()

def collect_forever():
    """Collect data indefinitely"""

    crc_timer = crctimer.CRC_Timer()
    crc_timer.start()

def scrape_and_insert():
    """Calls the scraping method defined in scrape.py and inserts this data using crcdb.py methods.
    First checks to see if CRC is closed according to schedule.py, and performs a scheduled close if it is."""

    # Get Time
    now = datetime.datetime.now()

    # If open, collect data
    if schedule.is_crc_open_typical(now):
        # Scrape CRC site
        percent_full = scrape.get_busy_object()
        busy_object = {
            "weekday": now.weekday(),
            "hour": now.hour,
            "minute": now.minute,
            "busy": percent_full,
            "isodate": now.strftime('%Y-%m-%d')
        }
        # Insert the data
        crcdb.insert_data(crcdb.db, crcdb.table, busy_object)
    else:
        print("Scheduled Close")

if __name__ == "__main__":
    collect_forever()