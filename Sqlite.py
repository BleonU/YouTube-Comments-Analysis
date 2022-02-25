import sqlite3


def insert_variable_into_table(cid, evaluation, likes, subcount, repliesAmount, name, text):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO Comments
                          (cid, evaluation, subcount, repliesAmount, likes, name, text) 
                          VALUES (?, ?, ?, ?, ?, ?, ?);"""

        data_tuple = (cid, evaluation, subcount, repliesAmount, likes, name, text)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        # print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")


def delete_all_data_in_table():
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        sqlite_delete = """DELETE FROM Comments;"""

        cursor.execute(sqlite_delete)
        sqliteConnection.commit()
        # print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete all data in sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")

def query(filter):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        sqlite_query = """SELECT * FROM Comments WHERE evaluation = '""" + filter + """';"""
        cursor.execute(sqlite_query)
        return cursor.fetchall()
        sqliteConnection.commit()

        # print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print(error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

if __name__ == '__main__':
    query('negative')