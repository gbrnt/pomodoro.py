#!/usr/bin/python

"""
pomodoro.py - Utility to time and track pomodoros

The task name, start time, duration and completeness are recorded in
a database. This can be exported to csv using pomodoro-export.py
"""

import datetime              # Getting dates and times of pomodoros for logging
from time import sleep       # Waiting for pomodoro to complete
import subprocess            # Playing beep sound
import os                    # Devnull to hide "play"'s output
from sys import exit         # Exiting after pomodoro cancelled

# Local imports
import db_interaction as db  # Database interactions
import parse_args
import pomodoro_export
import pomodoro_analyse

POMODORO_DURATION = 25  # Length of pomodoro in minutes
DATABASE_NAME = "pomodoros.db"


def pomodoro_start(connection, name):
    """Get the information ready to start the pomodoro"""
    if name is None:
        # Get task name ready for recording
        try:
            task = input("Input task name\n> ")
        except KeyboardInterrupt:
            print("\nPomodoro cancelled.")
            exit(0)
    else:
        task = name

    try:
        print("Pomodoro \"{}\" starting in 5 seconds...".format(name))
        sleep(5)  # To give a bit of mental preparation time
    except KeyboardInterrupt:
        print("\nPomodoro cancelled.")
        exit(0)

    start_time = datetime.datetime.now()
    start_only_time = str(start_time.time()).split(".")[:-1][0]  # H:M:S
    print("Pomodoro started at {}".format(start_only_time))

    return task, start_time


def play_complete_sound(filename):
    """Play sound to signify completion of the pomodoro"""
    # Play ding
    FNULL = open(os.devnull, "w")  # Redirect output to /dev/null

    if os.name == "nt":
        # The "0" argument number may need to be changed depending on which
        # device you want the sound to play on - sox's default does not always
        # work on windows
        play_args = ["sox", filename, "-t", "waveaudio", "0"]
    else:
        play_args = ["play", "-v", "0.2", filename]

    subprocess.call(play_args,
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


def do_pomodoro(duration, name):
    """Main method. Starts up, runs pomodoro and records it"""
    connection = db.startup("pomodoros.db")
    task, start_time = pomodoro_start(connection, name)
    complete, length = pomodoro_time(start_time, duration)

    # Use string of length because timedelta is unsupported in sqlite
    row = (start_time, task, str(length), complete)
    db.insert(connection, row)

    db.shutdown(connection)

if __name__ == "__main__":
    args = parse_args.parser.parse_args()

    date1, date2 = parse_args.date_range(args)

    # Normal pomodoro
    if not args.export and not args.analyse and not args.list_pomodoros:
        duration = args.time[0]
        
        if args.repeat:
            # Get most recent pomodoro from database
            last_pomodoro = pomodoro_export.get_last_n_pomodoros(DATABASE_NAME)[0]
            name = last_pomodoro[1]
        else:
            name = args.name
        do_pomodoro(duration, name)

    # List pomodoros
    elif args.list_pomodoros:
        if args.list_pomodoros[0] is None:
            num = 5
        else:
            num = args.list_pomodoros[0]
        pomodoro_export.list_pomodoros(DATABASE_NAME, num)

    elif args.export:
        export_name = args.export[0]
        
        if date1 is not None:
            display_date2 = date2 - datetime.timedelta(days=1)
            print("Exporting pomodoros between {0} and {1}".format(date1, display_date2))
            pomodoros = pomodoro_export.get_pomodoros_between_dates(
                    DATABASE_NAME,
                    date1, date2)
            pomodoro_export.pomodoro_export(export_name, pomodoros)

        else:
            print("Exporting all pomodoros")
            pomodoro_export.pomodoro_export(export_name)

    # Analyse pomodoros
    else:
        #print(args.analyse)

        if date1 is not None:
            display_date2 = date2 - datetime.timedelta(days=1)
            print("Analysing pomodoros between {0} and {1}".format(date1,display_date2))
            pomodoros = pomodoro_export.get_pomodoros_between_dates(
                    DATABASE_NAME,
                    date1, date2)
        else:
            print("Analysing all pomodoros")
            pomodoros = pomodoro_export.get_pomodoros(DATABASE_NAME)

        pomodoro_analyse.analyse_pomodoros(pomodoros, args)
