#!/usr/bin/python

"""
Pomodoro.py - Utility to time and track pomodoros

The task name, start time, duration and completeness are recorded in
a database. This can be exported to csv using pomodoro-export.py
"""

import datetime         # To get dates and times of pomodoros for logging
import sqlite3          # Database interactions
from time import sleep  # Waiting for pomodoro to complete
import subprocess       # For playing beep sound
import os               # For devnull to hide "play"'s output
from sys import exit
import db_interaction as db

POMODORO_DURATION = 25  # Length of pomodoro in minutes


def pomodoro_start():
    """Get the information ready to start the pomodoro"""
    # Get task name ready for recording
    task = input("Input task name\n> ")
    print("Pomodoro starting in 5 seconds...")
    sleep(5)  # To give a bit of mental preparation time

    start_time = datetime.datetime.now()
    start_only_time = str(start_time.time()).split(".")[:-1][0]  # H:M:S
    print("Pomodoro started at {}".format(start_only_time))

    return task, start_time


def play_complete_sound(filename):
    """Play sound to signify completion of the pomodoro"""
    # Play ding
    FNULL = open(os.devnull, "w")  # Redirect output to /dev/null
    subprocess.call(["play", "-v", "0.2", filename],
                    stdout=FNULL,
                    stderr=subprocess.STDOUT)


def pomodoro_time(start_time, duration):
    """Time the pomodoro and return whether it's complete"""
    duration_sec = duration * 60  # time.sleep takes duration in seconds

    complete = False  # Used to show whether a pomodoro was interrupted

    while not complete:
        try:
            sleep(duration_sec)  # Wait for length of pomodoro
            print("Pomodoro Complete!")

            play_complete_sound("timer_done.wav")

            complete = True      # End the loop

        except KeyboardInterrupt:
            print("\nPomodoro interrupted!")
            break                # Task not complete but needs to end

    if complete:    # Use full length
        length = datetime.timedelta(minutes=duration)
    else:           # Pomodoro unfinished so use timedelta
        end_time = datetime.datetime.now()
        length = end_time - start_time

    return complete, length


def do_pomodoro(duration):
    """Main method. Starts up, runs pomodoro and records it"""
    connection = db.startup("pomodoros.db")
    task, start_time = pomodoro_start()
    complete, length = pomodoro_time(start_time, duration)

    # Use string of length because timedelta is unsupported in sqlite
    row = (start_time, task, str(length), complete)
    db.insert(connection, row)

    db.shutdown(connection)

do_pomodoro(POMODORO_DURATION)
