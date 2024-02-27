import matplotlib.pyplot as plot
import crcdb

def hourly_summary_for_weekday(weekday=0):
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
    

hourly_summary_for_weekday(1)