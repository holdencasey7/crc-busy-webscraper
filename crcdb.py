import sqlite3

db = "crc.db"
table = "busy"
blank_data = {
    "weekday": -1,
    "hour": -1,
    "minutes": -1,
    "busy": -1
}

# Only use this once as it drops the existing table
def create_db_and_drop(database_name=db, table_name=table):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        drop_if_exists_query = "DROP TABLE IF EXISTS %s" % (table_name)
        cursor.execute(drop_if_exists_query)
        create_table_query = "CREATE TABLE %s (weekday INTEGER, hour INTEGER, minute INTEGER, percent_full INTEGER)" % (table_name)
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    
    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')

# Does not drop existing table if it already exists
def initialize_db(database_name=db, table_name=table):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        create_table_query = "CREATE TABLE %s (weekday INTEGER, hour INTEGER, minute INTEGER, percent_full INTEGER)" % (table_name)
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    
    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')

"""
# Assume data is of the form
    busy_at_time = {
        "weekday": current_time.weekday(),
        "hour": current_time.hour,
        "minutes": current_time.minute,
        "busy": integer_busy
    }
"""
def insert_data(database_name=db, table_name=table, data=blank_data):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        weekday, hour, minutes, busy = data.values()
        insert_data_query = "INSERT INTO %s VALUES (%d, %d, %d, %d)" % (table_name, weekday, hour, minutes, busy)
        cursor.execute(insert_data_query)
        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')

# Reads the entire table
def read_rows(database_name=db, table_name=table):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT * FROM %s" % table_name
        rows = cursor.execute(select_query).fetchall()
        print(rows)
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        rows = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
        return rows

# Reads a specific day and hour
def read_specific_time_rows(database_name=db, table_name=table, weekday=0, hour=0):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT * FROM %s WHERE weekday = %d AND hour = %d" % (table_name, weekday, hour)
        rows = cursor.execute(select_query).fetchall()
        print(rows)
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        rows = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
        return rows

# Reads a specific day
def read_specific_day_rows(database_name=db, table_name=table, weekday=0):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT * FROM %s WHERE weekday = %d" % (table_name, weekday)
        rows = cursor.execute(select_query).fetchall()
        print(rows)
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        rows = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
        return rows

# Gets the average for a specific day
def read_specific_day_average(database_name=db, table_name=table, weekday=0):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT AVG(percent_full) FROM %s WHERE weekday = %d" % (table_name, weekday)
        average = cursor.execute(select_query).fetchone()[0]
        print(average)
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        average = -1

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
        return average

# Reads a specific day and averages data in the same hour and minute
def read_grouped_day_rows(database_name=db, table_name=table, weekday=0):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT weekday, hour, minute, AVG(percent_full) FROM %s WHERE weekday = %d GROUP BY hour, minute" % (table_name, weekday)
        rows = cursor.execute(select_query).fetchall()
        print(rows)
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        rows = []

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
        return rows

# Gets the average of a specific hour on a specific day
def read_specific_day_and_hour_average(database_name=db, table_name=table, weekday=0, hour=0):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT AVG(percent_full) FROM %s WHERE weekday = %d AND hour = %d" % (table_name, weekday, hour)
        average = cursor.execute(select_query).fetchone()[0]
        print(average)
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        average = -1

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
        return average

# Reads the hourly averages for a day
def read_hourly_averages_for_day(database_name=db, table_name=table, weekday=0):
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
            print('SQLite Connection closed')
        return averages
    
# Cleans up data, removes invalid (-1) values
def cleanup(database_name=db, table_name=table):
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
            print('SQLite Connection closed')
