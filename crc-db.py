import sqlite3

try:
    connection = sqlite3.connect('crc.db')
    cursor = connection.cursor()
 
 
    # Close the cursor
    cursor.close()
 
# Handle errors
except sqlite3.Error as error:
    print('Error occurred - ', error)
 
finally:
    if connection:
        connection.close()
        print('SQLite Connection closed')

