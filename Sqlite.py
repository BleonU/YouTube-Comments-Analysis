import sqlite3


def insert_variable_into_table(comment_id, votes, positives, negatives):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO comments
                          (comment_id, votes, positives, negatives) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (comment_id, votes, positives, negatives)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
