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

    # Use string for output so that it can be written to file if desired
    output = ""

    if "breaks" in args.analyse:
        # Analyse the lengths of the breaks between pomodoros
        output = output + "\nAnalysing breaks\n"

        break_lengths = []
        last_end_time = datetime.timedelta(0)

        for n, pomo in enumerate(pomodoros):
            start_time = dt_string_to_datetime(pomo[0])
            length = len_string_to_timedelta(pomo[2])

            # We need the end time to find the time between pomodoros
            end_time = start_time + length

            break_lengths.append(end_time - last_end_time)
            last_end_time = end_time

        # First element is date of first one, so ignore it
        break_lengths = break_lengths[1:] 

        # Exclude breaks over a threshold (1 hour)
        # Over this threshold it's not really a break
        max_break_length = datetime.timedelta(hours=1)
        short_breaks = [b for b in break_lengths if b <= max_break_length]

        # Simple averaging - sum divided by number
        # Timedelta of 0 prevents TypeError
        average_timedelta = sum(short_breaks, datetime.timedelta(0)) / len(short_breaks)

        output = output + "\nAverage length of breaks which were less than 1 hour: {}\n".format(average_timedelta)
    
    if "frequency" in args.analyse:
        # Analyse the frequency of pomodoros
        pass

    if "complete" in args.analyse:
        # Analyse the number of complete and incomplete pomodoros
        pass

    print(output)
