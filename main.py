import scrape
import crcdb

def main():
    # Create db and drop tables if exist
    crcdb.create_db_and_drop(crcdb.db, crcdb.table)

    # Scrape CRC site
    busy_object = scrape.get_busy_object()

    # Insert the data
    crcdb.insert_data(crcdb.db, crcdb.table, busy_object)

    # Read the data
    crcdb.read_rows(crcdb.db, crcdb.table)


if __name__ == "__main__":
    main()