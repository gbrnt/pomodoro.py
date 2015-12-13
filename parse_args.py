#!/usr/bin/python

"""
pomodoro.py - Utility to time and track pomodoros

The task name, start time, duration and completeness are recorded in
a database. This can be exported to csv using pomodoro-export.py
"""

import argparse

parser = argparse.ArgumentParser(
        description="pomodoro.py - Utility to time and track pomodoros")

parser.add_argument("-e", "--export",
                    nargs=1,
                    metavar="EXPORT_FILENAME",
                    type=str,
                    help="export to file EXPORT_FILENAME")

parser.add_argument("-m", "--month",
                    action="store_true",
                    help="select pomodoros from last month")

parser.add_argument("-d", "--dates",
                    nargs=2,
                    type=str,
                    help="select dates pomodoros should fall between, inclusive")

parser.add_argument("-a", "--analyse",
                    nargs="?",
                    type=str,
                    metavar="ANALYSIS_FILENAME",
                    action="append",
                    help="analyse pomodoros, with optional export to file ANALYSIS_FILENAME")

parser.add_argument("-r", "--repeat",
                    action="store_true",
                    help="Repeat last pomodoro")

# None if not present, [None] if blank -l
parser.add_argument("-l", "--list_pomodoros",
                    nargs="?",
                    type=int,
                    metavar="N",
                    action="append",
                    help="list last N pomodoros")

parser.add_argument("-t", "--time",
                    nargs=1,
                    type=int,
                    metavar="POMODORO_LENGTH",
                    default=[25],
                    help="set pomodoro length in minutes")

parser.add_argument("name",
                    nargs="?",
                    type=str,
                    metavar="NAME",
                    help="pomodoro name or export filename")

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)

# Check to see whether it's a normal pomodoro
# if not args.export and not args.analyse:
