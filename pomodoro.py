#!/usr/bin/python

"""
Pomodoro.py - Utility to time and track pomodoros

The app on my tablet works well, but it'd be nice to have the information in
a database I can access after a week of intensive work to get some statistics
from it.
"""

import datetime         # To get dates and times of pomodoros for logging
import sqlite3          # Database interactions
from time import sleep  # Waiting for pomodoro to complete
from sys import exit    # Exiting if pomodoro cancelled
import subprocess       # For playing beep sound
import os               # For devnull to hide "play"'s output

POMODORO_DURATION = 0.25 #Length of pomodoro in minutes


def startup(db_name):
    """Open database, return connection"""
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


def do_pomodoro(duration):
    """Main method. Starts up, runs pomodoro and records it"""
    connection = startup("pomodoros.db")

    # Get task name ready for recording
    task = input("Input task name\n> ")
    print("Pomodoro starting in 5 seconds...")
    sleep(5)  # To give a bit of mental preparation time
    #print("...Started.")  # Not sure that's necessary

    start_time = datetime.datetime.now()
    duration_sec = duration * 60  # time.sleep takes duration in seconds

    complete = False  # Used to show whether a pomodoro was interrupted

    while not complete:
        try:
            sleep(duration_sec)  # Wait for length of pomodoro
            print("Pomodoro Complete!")

            # Play ding
            FNULL = open(os.devnull, "w")  # Redirect output to /dev/null
            subprocess.call(["play", "-v", "0.2", "timer_done.wav"],
                            stdout=FNULL,
                            stderr=subprocess.STDOUT)
            complete = True      # End the loop

        except KeyboardInterrupt:
            print("\nPomodoro interrupted!")
            break                # Task not complete but needs to end

    if complete:
        length = datetime.timedelta(minutes=duration)   # Use full length
    else:
        end_time = datetime.datetime.now()              # Pomodoro unfinished 
        length = end_time - start_time                  # So use timedelta
    
    # Use string of length because timedelta is unsupported in sqlite
    row = (start_time, task, str(length), complete)
    #print(row)
    db_insert(connection, row)

    shutdown(connection)

do_pomodoro(POMODORO_DURATION)
