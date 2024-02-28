from matplotlib import dates
import matplotlib.pyplot as plot
import crcdb
import datetime
import calendar
import argparse
import sys

def hourly_barchart_for_weekday(weekday=0):
    crcdb.cleanup()
    data = crcdb.read_hourly_averages_for_day(weekday=weekday)
    if len(data) <= 0:
        print("No data for %s" % calendar.day_name[weekday])
        return
    x_axis = list((entry[0] for entry in data))
    y_axis = list((entry[1] for entry in data))
    plot.bar(x_axis, y_axis)
    plot.xlabel("Hour")
    plot.ylabel("Percent Full")
    plot.title("Hourly Averages for %s" % calendar.day_name[weekday])
    plot.show()

# Y axis will be min data - max data   
def dynamic_linechart_for_weekday(weekday=0):
    crcdb.cleanup()
    data = crcdb.read_grouped_day_rows(weekday=weekday)
    if len(data) <= 0:
        print("No data for %s" % calendar.day_name[weekday])
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    plot.plot(x_axis, y_axis)
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data for %s" % calendar.day_name[weekday])
    plot.show()

# Y axis fixed to 0-100
def fixed_linechart_for_weekday(weekday=0):
    crcdb.cleanup()
    data = crcdb.read_grouped_day_rows(weekday=weekday)
    if len(data) <= 0:
        print("No data for %s" % calendar.day_name[weekday])
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    plot.plot(x_axis, y_axis)
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data for %s" % calendar.day_name[weekday])
    plot.ylim(0,100)
    plot.show()

def fixed_linechart_weekly_averages():
    crcdb.cleanup()
    data = crcdb.read_grouped_rows()
    if len(data) <= 0:
        print("No data for")
        return
    x_axis = list((datetime.datetime(2024, 1, day=entry[0], hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    plot.plot(x_axis, y_axis)
    pos = dates.HourLocator(interval=12)
    fmt = dates.DateFormatter("%d - Hour %H")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data")
    plot.ylim(0,100)
    plot.show()


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--plot", help="Plot Type")
parser.add_argument("-d", "--weekday", help="Weekday 0-6", type=int)
args = parser.parse_args()
if args.weekday and ((args.weekday < 0) or (args.weekday) > 6):
    print("Invalid Weekday. Must be [0,6]")
    sys.exit("ERROR: Invalid Weekday")
if (args.plot is None) or args.plot == "":
    print("""Plot types -p:
        hb for hourly barchart (need -d WEEKDAY)
        fl for fixed linechart (need -d WEEKDAY)
        dl for dynamic linechart (need -d WEEKDAY)
        fla for fixed linechart weekly averages""")
    sys.exit("ERROR: Invalid Plot Type")
elif (args.plot == "hb"):
    hourly_barchart_for_weekday(args.weekday)
elif (args.plot == "fl"):
    fixed_linechart_for_weekday(args.weekday)
elif (args.plot == "dl"):
    dynamic_linechart_for_weekday(args.weekday)
elif (args.plot == "fla"):
    fixed_linechart_weekly_averages()
else:
    print("Invalid Plot Type")
    print("""Plot types -p:
        hb for hourly barchart (need -d WEEKDAY)
        fl for fixed linechart (need -d WEEKDAY)
        dl for dynamic linechart (need -d WEEKDAY)
        fla for fixed linechart weekly averages""")
    sys.exit("ERROR: Invalid Plot Type")
    