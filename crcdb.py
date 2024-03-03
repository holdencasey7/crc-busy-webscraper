import sqlite3

db = "crc.db" # User specific
table = "busy_new" # User specific
blank_data = {
    "weekday": -1,
    "hour": -1,
    "minute": -1,
    "busy": -1,
    "isodate": '2020-01-01'
}

# Only use this once as it drops the existing table
def create_db_and_drop(database_name=db, table_name=table):
    """Creates a new database with a table configured to hold data from scrape.py -> get_busy_object().
    If the table already exists, it will be dropped and re-created."""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        drop_if_exists_query = "DROP TABLE IF EXISTS %s" % (table_name)
        cursor.execute(drop_if_exists_query)
        create_table_query = "CREATE TABLE %s (weekday INTEGER, hour INTEGER, minute INTEGER, percent_full INTEGER, isodate VARCHAR(11))" % (table_name)
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    
    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: CreateDBAndDrop')

def initialize_db(database_name=db, table_name=table):
    """Same as create_db_and_drop() but does not check if table exists already.
    Does not drop existing table."""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        create_table_query = "CREATE TABLE %s (weekday INTEGER, hour INTEGER, minute INTEGER, percent_full INTEGER, isodate VARCHAR(11))" % (table_name)
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    
    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: InitializeDB')

def insert_data(database_name=db, table_name=table, data=blank_data):
    """Inserts data into the given table. Assumes data is of the form from scrape.py -> get_busy_object().\n
    Assume data is of the form:\n
    busy_at_time = {
        "weekday": 1,
        "hour": 13,
        "minute": 54,
        "busy": 38,
        "isodate": '2024-01-01',
    }"""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        weekday, hour, minute, busy, isodate = data.values()
        insert_data_query = """INSERT INTO %s VALUES (%d, %d, %d, %d, "%s")""" % (table_name, weekday, hour, minute, busy, str(isodate))
        cursor.execute(insert_data_query)
        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: InsertData')

def insert_data_mass(database_name=db, table_name=table, data_list=[]):
    """Inserts multiple items at a time in a single sqlite connection."""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        for data in data_list:
            weekday, hour, minute, busy, isodate = data.values()
            insert_data_query = """INSERT INTO %s VALUES (%d, %d, %d, %d, "%s")""" % (table_name, weekday, hour, minute, busy, str(isodate))
            cursor.execute(insert_data_query)
        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: InsertDataMass')

def read_rows(database_name=db, table_name=table):
    """Returns a list of the rows of a table."""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT * FROM %s" % table_name
        rows = cursor.execute(select_query).fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        rows = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadRows')
        return rows

def read_specific_weekday_hour(database_name=db, table_name=table, weekday=0, hour=0):
    """Returns rows with specific weekday and hour"""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT * FROM %s WHERE weekday = %d AND hour = %d" % (table_name, weekday, hour)
        rows = cursor.execute(select_query).fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        rows = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadSpecificWeekdayHour')
        return rows

def read_specific_weekday(database_name=db, table_name=table, weekday=0):
    """Returns rows with specific weekday"""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT * FROM %s WHERE weekday = %d" % (table_name, weekday)
        rows = cursor.execute(select_query).fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        rows = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadSpecificWeekday')
        return rows

def read_specific_weekday_average(database_name=db, table_name=table, weekday=0):
    """Returns average for a specific weekday"""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT AVG(percent_full) FROM %s WHERE weekday = %d" % (table_name, weekday)
        average = cursor.execute(select_query).fetchone()[0]
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        average = -1

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadSpecificWeekdayAverage')
        return average

def read_grouped_weekday(database_name=db, table_name=table, weekday=0):
    """Returns rows with a specific weekday, where entries with the same hour and minute will be averaged."""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT weekday, hour, minute, AVG(percent_full) FROM %s WHERE weekday = %d GROUP BY hour, minute" % (table_name, weekday)
        rows = cursor.execute(select_query).fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        rows = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadGroupedWeekday')
        return rows

def read_specific_weekday_and_hour_average(database_name=db, table_name=table, weekday=0, hour=0):
    """Returns the average of a specific weekday and hour"""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT AVG(percent_full) FROM %s WHERE weekday = %d AND hour = %d" % (table_name, weekday, hour)
        average = cursor.execute(select_query).fetchone()[0]
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        average = -1

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadSpecificWeekdayAndHourAverage')
        return average

def read_grouped_rows(database_name=db, table_name=table):
    """Returns all rows where elements with the same weekday, hour, and minute are averaged"""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT weekday, hour, minute, AVG(percent_full) FROM %s GROUP BY weekday, hour, minute" % table_name
        averages = cursor.execute(select_query).fetchall()
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
        averages = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadGroupedRows')
        return averages
    
def read_hourly_averages_for_weekday(database_name=db, table_name=table, weekday=0):
    """Returns rows of the hourly averages for a specific weekday"""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT hour, AVG(percent_full) FROM %s WHERE weekday = %d GROUP BY hour" % (table_name, weekday)
        averages = cursor.execute(select_query).fetchall()
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
        averages = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadHourlyAveragesForWeekday')
        return averages
    
def read_specific_date(database_name=db, table_name=table, date='2020-01-01'):
    """Returns rows with a specific date"""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = """SELECT * FROM %s WHERE isodate = "%s" """ % (table_name, date)
        rows = cursor.execute(select_query).fetchall()
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
        rows = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadSpecificDate')
        return rows
    
def read_specific_date_average(database_name=db, table_name=table, date='2020-01-01'):
    """Returns the average from a specific date"""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = """SELECT AVG(percent_full) FROM %s WHERE isodate = "%s" GROUP BY weekday""" % (table_name, date)
        average = cursor.execute(select_query).fetchone()[0]
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
        average = -1

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: ReadSpecificDateAverage')
        return average
    
def cleanup(database_name=db, table_name=table):
    """Removes invalid percent_full values. Typically introduced when CRC is detected closed or when unable to load website."""

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        delete_query = "DELETE FROM %s WHERE percent_full = -1" % table_name
        cursor.execute(delete_query)
        connection.commit()
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed: Cleanup')
