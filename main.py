import scrape
import crcdb
import crctimer
import time

def main():
    # Create db and drop tables if exist
    crcdb.create_db_and_drop()

    # Repeat every 1 minute
    crc_timer = crctimer.CRC_Timer()
    crc_timer.start()
    time.sleep(200)
    crc_timer.stop()

    # Read the data
    crcdb.read_rows()



if __name__ == "__main__":
    main()