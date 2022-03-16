import sqlite3


def insert_variable_into_table(cid, evaluation, likes, subcount, repliesAmount, name, text, image, link, value):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO Comments
                          (cid, evaluation, subcount, repliesAmount, likes, name, text, image, link, evaluation_value) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        data_tuple = (cid, evaluation, subcount, repliesAmount, likes, name, text, image, link, value)
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


def delete_all_data_in_tables():
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        sqlite_delete = """DELETE FROM Comments;"""
        cursor.execute(sqlite_delete)

        sqlite_delete = """DELETE FROM Replies;"""
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

def query(query, table):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        if query is None:
            sqlite_query = """SELECT * FROM """ + table + """;"""
        else:
            sqlite_query = """SELECT * FROM """ + table + """ WHERE """ + query + """;"""
        cursor.execute(sqlite_query)
        return cursor.fetchall()

        cursor.close()

    except sqlite3.Error as error:
        print(error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def insert_variable_into_replies(ocid, cid):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO Replies
                          (original_comment_id, comment_id) 
                          VALUES (?, ?);"""

        data_tuple = (ocid, cid)
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