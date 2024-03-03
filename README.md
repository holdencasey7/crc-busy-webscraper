# CRC Busy Tracker

Personal project to record how busy the GaTech campus gym is at various times throughout the day.
Uses live capacity data from https://live.waitz.io/4vxie66a29ct .
This project is currently operating on a Raspberry Pi 4 Model B running Raspberry Pi OS, but was tested on a local machine.

## Dependencies

Written in Python 3.9.13
Dependencies are listed in requirements.txt and can be installed with

```bash
pip install -r requirements.txt
```

## Included Files

### scrape.py

The webscraping portion. Uses selenium.

**get_busy_object(now)**:
Scrapes the live capacity data using Firefox WebDriver and returns the percent full, along with time data, in a single object.
If the waitz.io site indicates the CRC is closed, a detected close will occur and percent_full will be set to -1.

### crcdb.py

The database portion. Uses sqlite. Methods to create the database and tables, insert data, read data, and delete data. Methods use SQL queries.

### datacollection.py

The data collection portion. Collect methods use the timer from crctimer.py, which continuously calls scrape_and_insert() for various time lengths. Running this file will call collect_forever(), which is aborted with ^C.

**scrape_and_insert()**:
Calls the scraping method defined in scrape.py and inserts this data using crcdb.py methods.
First checks to see if CRC is closed according to schedule.py, and performs a scheduled close if it is.
Note: A 'scheduled close' occurs when the current time is known to be a time when the CRC is closed as stated on the GaTech webpage. A 'detected close' occurs when the CRC is assumed open, but is actually closed as indicated by waitz.io. This is likely during special events or holidays.

### crctimer.py

A helper class to run the data collection portion every 1 minute

### schedule.py

A helper class to determine if the current time is a scheduled close as indicated on the GaTech posted hours.

### analysis.py

The graphing portion. Uses matplotlib. Contains various methods that produce different graphs representing the collected data.
When run from the command line, plots will be shown and not uploaded to Google Drive.
Dynamic charts will not have a fixed y-axis, fixed or default charts will be fixed 0-100.
Not all plots are necessarily useful or informative. The most effective (in my opinion) are those uploaded to Google Drive in upload.py.
Command line format:

```bash
python analysis.py -p [PLOT_TYPE] [OPTIONAL ARGS: -d [WEEKDAY 0-6] -i [YYYY-MM-DD] ]
```

Plot types -p:

- hb for hourly barchart (need -d WEEKDAY)
- fl for fixed linechart (need -d WEEKDAY)
- dl for dynamic linechart (need -d WEEKDAY)
- fla for fixed linechart weekly averages
- ifl for fixed linechart on a specific date (need -i YYYY-MM-DD)
- ow for overlayed weekdays fixed
- owd for overlayed weekdays dynamic
- ta for total average over all weekdays
- cwa for compare weekday to average (need -d WEEKDAY)
- cdw for compare date to weekday (need -i YYYY-MM-DD -d WEEKDAY)
- cda for compare date to average (need -i YYYY-MM-DD)
- cdd for compare weekday to weekday (need -d WEEKDAY1 -sd WEEKDAY2)

### upload.py

The uploading portion. Uses Google Drive API to upload plots created in analysis.py to a folder in Google Drive.
Authentication must be performed and is obvsiouly not included in the GitHub files.
Hint: files needed include

- settings.yaml
- credentials.json
- token.json

This portion is currently under construction. The goal is to have images uploaded automatically nightly, as opposed to manually.

## Non-Included Files

Files that are produced/needed but not included in the GitHub files.

- **crc.db**: The local database accessed via sqlite
- **Google API Auth**: As detailed in upload.py section, files required to authenticate Google Drive user
- **\*.png**: Images of plots created by analysis.py

## Authors

Created by Holden Casey in 2024.
