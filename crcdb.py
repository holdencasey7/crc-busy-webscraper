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

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')

def read_specific_date_rows(database_name=db, table_name=table, weekday=0, hour=0, minute=0):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        select_query = "SELECT percent_full FROM %s WHERE weekday = %d AND hour = %d AND minute = %d" % (table_name, weekday, hour, minute)
        rows = cursor.execute(select_query).fetchall()
        print(rows)
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)

    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
