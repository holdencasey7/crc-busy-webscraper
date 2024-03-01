import scrape
import crcdb
import crctimer
import time
import datetime
import schedule

def collect_without_existing_db(length=15):
    # Create db and drop tables if exist
    crcdb.create_db_and_drop()
    collect(length)
    

def collect(length=15):
    # Repeat every 1 minute
    crc_timer = crctimer.CRC_Timer()
    crc_timer.start()
    time.sleep(length)
    crc_timer.stop()

def scrape_and_insert():
    # Get Time
    now = datetime.datetime.now()

    # If open, collect data
    if schedule.is_crc_open_typical(now):
        # Scrape CRC site
        busy_object = scrape.get_busy_object(now)
        # Insert the data
        crcdb.insert_data(crcdb.db, crcdb.table, busy_object)
    else:
        print("Scheduled Close")

if __name__ == "__main__":
    while True:
        collect(60*60*3)