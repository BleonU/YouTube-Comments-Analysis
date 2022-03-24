import sqlite3


def insertVariableIntoComments(cid, evaluation, likes, subcount, repliesAmount, name, text, image, link, value, parent):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()

        sqlite_insert_with_param = """INSERT INTO Comments
                          (cid, evaluation, subcount, repliesAmount, likes, name, text, image, link, evaluation_value, parent) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        data_tuple = (cid, evaluation, subcount, repliesAmount, likes, name, text, image, link, value, parent)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def deleteAllDataInTables():
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()

        sqlite_delete = """DELETE FROM Comments;"""
        cursor.execute(sqlite_delete)

        sqlite_delete = """DELETE FROM Replies;"""
        cursor.execute(sqlite_delete)

        sqliteConnection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete all data in sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def update(table, value, query):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()

        sqlite_update = """UPDATE """ + table + """ SET """ + value + """ WHERE """ + query + """;"""
        cursor.execute(sqlite_update)
        sqliteConnection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update data in sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def query(column, query, table):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()
        if query is None:
            sqlite_query = """SELECT """ + column + """ FROM """ + table + """;"""
        else:
            sqlite_query = """SELECT """ + column + """ FROM """ + table + """ WHERE """ + query + """;"""
        cursor.execute(sqlite_query)
        return cursor.fetchall()

    except sqlite3.Error as error:
        print(error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def insertVariableIntoReplies(ocid, cid):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('comments.sqlite')
        cursor = sqliteConnection.cursor()

        sqlite_insert_with_param = """INSERT INTO Replies
                          (original_comment_id, comment_id) 
                          VALUES (?, ?);"""

        data_tuple = (ocid, cid)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()