from matplotlib import dates
import matplotlib.pyplot as plot
import crcdb
import datetime
import calendar
import argparse
import sys
from enum import Enum

class PlotTypes(Enum):
    WEEKDAY_FIXED_LINE = "fl"
    DATE_FIXED_LINE = "ifl"
    OVERLAYED_WEEKDAYS_FIXED_LINE = "ow"
    TOTAL_AVERAGES = "ta"

def hourly_barchart_for_weekday(weekday=0):
    crcdb.cleanup()
    data = crcdb.read_hourly_averages_for_weekday(weekday=weekday)
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
 
def dynamic_linechart_for_weekday(weekday=0):
    crcdb.cleanup()
    data = crcdb.read_grouped_weekday(weekday=weekday)
    if len(data) <= 0:
        print("No data for %s" % calendar.day_name[weekday])
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis)
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data for %s" % calendar.day_name[weekday])
    plot.show()

def fixed_linechart_for_weekday(weekday=0, show=False):
    crcdb.cleanup()
    plot.rcParams['figure.figsize'] = [12, 5]
    data = crcdb.read_grouped_weekday(weekday=weekday)
    if len(data) <= 0:
        print("No data for %s" % calendar.day_name[weekday])
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis)
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data for %s" % calendar.day_name[weekday])
    plot.ylim(0,100)
    filename = f"fl-{weekday}.png"
    plot.savefig(filename)
    if show:
        plot.show()
    return filename
    # plot.show()

def fixed_linechart_weekly_averages():
    crcdb.cleanup()
    data = crcdb.read_grouped_rows()
    if len(data) <= 0:
        print("No data")
        return
    x_axis = list((datetime.datetime(2024, 1, day=entry[0], hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].day*60*24 + time[0].hour*60 + time[0].minute))
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

def fixed_linechart_date(date="2020-01-01", show=False):
    crcdb.cleanup()
    plot.rcParams['figure.figsize'] = [12, 5]
    data = crcdb.read_specific_date(date=date)
    if len(data) <= 0:
        print("No data for %s" % date)
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis)
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data for %s" % date)
    plot.ylim(0,100)
    filename = f"ifl-{date}.png"
    plot.savefig(filename)
    if show:
        plot.show()
    return filename
    # plot.show()

def overlay_weekdays(show=False):
    crcdb.cleanup()
    plot.rcParams['figure.figsize'] = [12, 5]
    for i in range(0,7):
        data = crcdb.read_grouped_weekday(weekday=i)
        if len(data) > 0:
            x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
            y_axis = list(entry[3] for entry in data)
            x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
            plot.plot(x_axis, y_axis, label = calendar.day_name[i])
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data Overlay")
    plot.ylim(0,100)
    plot.legend()
    filename = "ow.png"
    plot.savefig(filename)
    if show:
        plot.show()
    return filename
    # plot.show()

def overlay_weekdays_dynamic():
    crcdb.cleanup()
    for i in range(0,7):
        data = crcdb.read_grouped_weekday(weekday=i)
        if len(data) > 0:
            x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
            y_axis = list(entry[3] for entry in data)
            x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
            plot.plot(x_axis, y_axis, label = calendar.day_name[i])
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data Overlay")
    plot.legend()
    plot.show()

def total_averages(show=False):
    crcdb.cleanup()
    plot.rcParams['figure.figsize'] = [12, 5]
    data = crcdb.read_grouped_rows()
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis)
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("Capacity Data Average")
    plot.ylim(0,100)
    filename = "ta.png"
    plot.savefig(filename)
    if show:
        plot.show()
    return filename

def compare_weekday_to_average(weekday=0):
    crcdb.cleanup()
    data = crcdb.read_grouped_rows()
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis, label="Average")
    data = crcdb.read_grouped_weekday(weekday=weekday)
    if len(data) <= 0:
        print("No data for %s" % calendar.day_name[weekday])
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis, label=calendar.day_name[weekday])
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("%s VS Average" % calendar.day_name[weekday])
    plot.ylim(0,100)
    plot.legend()
    plot.show()

def compare_date_to_weekday(date, weekday=0):
    crcdb.cleanup()
    data = crcdb.read_grouped_weekday(weekday=weekday)
    if len(data) <= 0:
        print("No data for %s" % calendar.day_name[weekday])
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis, label=calendar.day_name[weekday])
    data = crcdb.read_specific_date(date=date)
    if len(data) <= 0:
        print("No data for %s" % date)
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis, label=date)
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("%s VS %s" % (date, calendar.day_name[weekday]))
    plot.ylim(0,100)
    plot.legend()
    plot.show()

def compare_date_to_average(date):
    crcdb.cleanup()
    data = crcdb.read_grouped_rows()
    if len(data) <= 0:
        print("No data")
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis, label="Average")
    data = crcdb.read_specific_date(date=date)
    if len(data) <= 0:
        print("No data for %s" % date)
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis, label=date)
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("%s VS Average" % date)
    plot.ylim(0,100)
    plot.legend()
    plot.show()

def compare_date_to_date():
    return

def compare_weekday_to_weekday(day1=0, day2=1):
    crcdb.cleanup()
    data = crcdb.read_grouped_weekday(weekday=day1)
    if len(data) <= 0:
        print("No data for %s" % calendar.day_name[day1])
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis, label=calendar.day_name[day1])
    data = crcdb.read_grouped_weekday(weekday=day2)
    if len(data) <= 0:
        print("No data for %s" % calendar.day_name[day2])
        return
    x_axis = list((datetime.datetime(2024, 1, 1, hour=entry[1], minute=entry[2]) for entry in data))
    y_axis = list(entry[3] for entry in data)
    x_axis, y_axis = zip(*sorted(zip(x_axis, y_axis), key=lambda time: time[0].hour*60 + time[0].minute))
    plot.plot(x_axis, y_axis, label=calendar.day_name[day2])
    pos = dates.HourLocator()
    fmt = dates.DateFormatter("%H:%M")
    plot.gca().xaxis.set(major_locator=pos, major_formatter=fmt)
    plot.grid(axis='x')
    plot.xlabel("Time")
    plot.ylabel("Percent Full")
    plot.title("%s VS %s" % (calendar.day_name[day1], calendar.day_name[day2]))
    plot.ylim(0,100)
    plot.legend()
    plot.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--plot", help="Plot Type")
    parser.add_argument("-d", "--weekday", help="Weekday 0-6", type=int)
    parser.add_argument("-i", "--isodate", help="YYYY-MM-DD", type=str)
    parser.add_argument("-sd", "--secondweekday", help="Second Weekday to Compare", type=int)
    args = parser.parse_args()
    helper_string = """Plot types -p:
        hb for hourly barchart (need -d WEEKDAY)
        fl for fixed linechart (need -d WEEKDAY)
        dl for dynamic linechart (need -d WEEKDAY)
        fla for fixed linechart weekly averages
        ifl for fixed linechart on a specific date (need -i YYYY-MM-DD)
        ow for overlayed weekdays fixed
        owd for overlayed weekdays dynamic
        ta for total average over all weekdays
        cwa for compare weekday to average (need -d WEEKDAY)
        cdw for compare date to weekday (need -i YYYY-MM-DD -d WEEKDAY)
        cda for compare date to average (need -i YYYY-MM-DD)
        cdd for compare weekday to weekday (need -d WEEKDAY1 -sd WEEKDAY2)"""

    if args.weekday and ((args.weekday < 0) or (args.weekday) > 6):
        print("Invalid Weekday. Must be [0,6]")
        sys.exit("ERROR: Invalid Weekday")
    if (args.plot is None) or args.plot == "":
        print(helper_string)
        sys.exit("ERROR: Invalid Plot Type")
    elif (args.plot == "hb"):
        hourly_barchart_for_weekday(args.weekday)
    elif (args.plot == "fl"):
        fixed_linechart_for_weekday(args.weekday, show=True)
    elif (args.plot == "dl"):
        dynamic_linechart_for_weekday(args.weekday)
    elif (args.plot == "fla"):
        fixed_linechart_weekly_averages()
    elif (args.plot == "ifl"):
        fixed_linechart_date(args.isodate, show=True)
    elif (args.plot == "ow"):
        overlay_weekdays(show=True)
    elif (args.plot == "ta"):
        total_averages(show=True)
    elif (args.plot == "cwa"):
        compare_weekday_to_average(args.weekday)
    elif (args.plot == "cdw"):
        compare_date_to_weekday(args.isodate, args.weekday)
    elif (args.plot == "cda"):
        compare_date_to_average(args.isodate)
    elif (args.plot == "cdd"):
        compare_weekday_to_weekday(args.weekday, args.secondweekday)
    elif (args.plot == "owd"):
        overlay_weekdays_dynamic()
    else:
        print("Invalid Plot Type")
        print(helper_string)
        sys.exit("ERROR: Invalid Plot Type")
        
if __name__=="__main__":
    main()