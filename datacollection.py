import scrape
import crcdb
import crctimer
import time

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

    # Read the data
    crcdb.read_rows()



if __name__ == "__main__":
    collect(60*60*3)