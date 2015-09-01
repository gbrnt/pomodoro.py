#!/usr/bin/python

"""
Pomodoro.py - Utility to time and track pomodoros

The app on my tablet works well, but it'd be nice to have the information in
a database I can access after a week of intensive work to get some statistics
from it.
"""

import datetime    # To get dates and times of pomodoros for logging
import sqlite3


def startup(db_name):
    """Open database"""
    connection = sqlite3.connect(db_name)
    cur = connection.cursor()

    # Create table on first start
    cur.execute("CREATE TABLE IF NOT EXISTS pomodoros"
                "(datetime, task, length, complete)")

    return connection


def db_insert(connection, row_data):
    """Insert a row into the pomodoros table in the database"""
    cur = connection.cursor()
    cur.execute("INSERT INTO pomodoros VALUES (?,?,?,?)", row_data)


def shutdown(connection):
    """Safely close database"""
    connection.commit()
    connection.close()


def db_test_run():
    example_row = (datetime.datetime.now(),
                   "Doing things",
                   25,
                   True)

    conn = startup("pomodoros.db")
    db_insert(conn, example_row)
    shutdown(conn)

db_test_run()
