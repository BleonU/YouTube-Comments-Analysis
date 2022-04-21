import sqlite3
from sqlite3 import Error


def main():
    comments = """ CREATE TABLE IF NOT EXISTS Comments (
                                                            cid              text,
                                                            evaluation       text,
                                                            subCount         int,
                                                            repliesAmount    int,
                                                            likes            int,
                                                            name             text,
                                                            text             text,
                                                            image            text,
                                                            link             text,
                                                            evaluation_value int,
                                                            parent           text
                                                        );"""

    replies = """ CREATE TABLE IF NOT EXISTS Replies (
                                                        original_comment_id text,
                                                        comment_id          text
                                                    );"""
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(r"comments.sqlite")
    except Error as e:
        print(e)
    cursor = sqliteConnection.cursor()
    cursor.execute(comments)
    cursor.execute("""create unique index Comments_cid_uindex on Comments (cid);""")
    cursor.execute(replies)


if __name__ == '__main__':
    main()

