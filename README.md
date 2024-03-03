# CRC Busy Tracker

Personal project to record how busy the GaTech campus gym is at various times throughout the day
Uses live capacity data from https://live.waitz.io/4vxie66a29ct

## Dependencies

Written in Python 3.9.13
Dependencies are listed in requirements.txt and can be installed with

```bash
pip install -r requirements.txt
```

## Python Files

### scrape.py

The webscraping portion

**get_busy_object(now)**:
Scrapes the live capacity data using Firefox WebDriver and returns the percent full, along with time data, in a single object.
If the waitz.io site indicates the CRC is closed, percent_full will be set to -1

### crcdb.py

The database portion

**create_db_and_drop(database_name, table_name)**:
Creates a new database with a table configured to hold data from **scrape.py::get_busy_object**.
If the table already exists, it will be dropped and re-created.

**initialize_db(database_name, table_name)**:
Same as **create_db_and_drop** but does not check if table exists already
