from matplotlib import dates
import matplotlib.pyplot as plot
import crcdb
import datetime

def hourly_barchart_for_weekday(weekday=0):
    crcdb.cleanup()
    data = crcdb.read_hourly_averages_for_day(weekday=weekday)
    print(data)
    x_axis = list((entry[0] for entry in data))
    y_axis = list((entry[1] for entry in data))
    plot.bar(x_axis, y_axis)
    plot.xlabel("Hour")
    plot.ylabel("Percent Full")
    plot.title("Hourly Averages for Weekday %s" % weekday)
    plot.show()
    
def linechart_for_weekday(weekday=0):
    crcdb.cleanup()
    data = crcdb.read_specific_day_rows(weekday=weekday)
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    plot.plot(x_axis, y_axis)
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data for Weekday %s" % weekday)
    plot.show()

hourly_barchart_for_weekday(1)
# linechart_for_weekday(1)