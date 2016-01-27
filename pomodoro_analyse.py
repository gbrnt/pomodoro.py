"""
pomodoro.py - Utility to time and track pomodoros

The task name, start time, duration and completeness are recorded in
a database. This can be exported to csv using pomodoro-export.py
"""

import datetime


def dt_string_to_datetime(string):
    """Convert pomodoro's datetime string to a datetime"""
    dt = datetime.datetime.strptime(
            string,
            "%Y-%m-%d %H:%M:%S.%f")
    return dt

def len_string_to_timedelta(string):
    """Convert pomodoro's length string to a timedelta"""
    length_list = [float(i) for i in string.split(":")]
    td = datetime.timedelta(hours=length_list[0],
                            minutes=length_list[1],
                            seconds=length_list[2])
    return td

def analyse_pomodoros(pomodoros, args):
    """Find and print statistics about pomodoros"""

    if "breaks" in args.analyse:
        # Analyse the lengths of the breaks between pomodoros

        break_lengths = []

        for n, pomo in enumerate(pomodoros):
            start_time = dt_string_to_datetime(pomo[0])
            length = len_string_to_timedelta(pomo[2])
            end_time = start_time + length
    
    if "frequency" in args.analyse:
        # Analyse the frequency of pomodoros
        pass

    if "complete" in args.analyse:
        # Analyse the number of complete and incomplete pomodoros
        pass
