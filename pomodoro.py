#!/usr/bin/python

"""
Pomodoro.py - Utility to time and track pomodoros

The app on my tablet works well, but it'd be nice to have the information in
a database I can access after a week of intensive work to get some statistics
from it.
"""

import datetime    # To get dates and times of pomodoros for logging
import sqlite3     # Database interactions
from time import sleep

POMODORO_DURATION = 25  # Length of pomodoro in minutes


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
    """Insert a test row into the database"""
    example_row = (datetime.datetime.now(),
                   "Doing things",
                   25,
                   True)

    conn = startup("pomodoros.db")
    db_insert(conn, example_row)
    shutdown(conn)

def do_pomodoro(task, duration):
    #Get time
    #Start timing for duration
    #If pomodoro interrupted, record duration as current time
    #Play ding when pomodoro is complete
    #Create row for pomodoro
    #Insert row into database
    time = datetime.datetime.now()
    duration_sec = duration * 60
    complete = False

    while not complete:
        try:
            sleep(duration_sec)
            print("DONE!")
            complete = True
        except KeyboardInterrupt:
            print("Interrupted!")
            complete = "Interrupted"

do_pomodoro("Thing", 1)
