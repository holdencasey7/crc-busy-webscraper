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

#### scrape.py

**get_busy_object(now)**
Scrapes the live capacity data using Firefox WebDriver and returns the percent full, along with time data, in a single object
If the waitz.io site indicates the CRC is closed, percent_full will be set to -1
