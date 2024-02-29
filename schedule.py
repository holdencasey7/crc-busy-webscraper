import datetime

def is_crc_open_typical(now=datetime.datetime.now()):
    weekday = now.weekday()
    hour = now.hour
    minute = now.minute
    isodate = now.strftime('%Y-%m-%d')
    open = True
    if weekday in [0, 1, 2, 3]:
        # Monday-Thursday
        if hour == 5 and minute <= 30:
            open = False
        elif hour < 5 or hour >= 24:
            open = False
    elif weekday == 4:
        # Friday
        if hour == 5 and minute <= 30:
            open = False
        elif hour < 5 or hour >= 9:
            open = False
    elif weekday == 5:
        # Saturday
        if hour < 9 or hour >= 19:
            open = False
    elif weekday == 6:
        # Sunday
        if hour < 10 or hour >= 20:
            open = False
    return open
    
