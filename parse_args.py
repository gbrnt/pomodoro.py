#!/usr/bin/python

"""
pomodoro.py - Utility to time and track pomodoros

The task name, start time, duration and completeness are recorded in
a database. This can be exported to csv using pomodoro-export.py
"""

import argparse
import datetime

parser = argparse.ArgumentParser(
        description="pomodoro.py - Utility to time and track pomodoros")

parser.add_argument("-e", "--export",
                    nargs=1,
                    metavar="EXPORT_FILENAME",
                    type=str,
                    help="export to file EXPORT_FILENAME")

parser.add_argument("-m", "--month",
                    action="store_true",
                    help="select pomodoros from last complete calendar month")

parser.add_argument("-d", "--dates",
                    nargs=2,
                    type=str,
                    help="select date range pomodoros should fall between, inclusive")

parser.add_argument("-a", "--analyse",
                    nargs="*",
                    type=str,
                    metavar="ANALYSIS_FILENAME",
                    action="store",
                    choices=["breaks",
                             "frequency",
                             "complete",
                             "count",
                             "topic"],
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


def date_range(args):
    """Calculate date range needed from arguments provided"""
    if args.dates:
        try:
            date1 = datetime.datetime.strptime(args.dates[0], "%Y-%m-%d").date()
            date2 = datetime.datetime.strptime(args.dates[1], "%Y-%m-%d").date()
        except ValueError as exception_message:
            print(exception_message)
            exit(0)

        # Make date2 end of day rather than start
        # Otherwise it's treated as the very start of the day
        date2 = date2 + datetime.timedelta(days=1)

    elif args.month:
        current_datetime = datetime.datetime.now()  # Current date
        first_of_month = datetime.date(year=current_datetime.year,
                                       month=current_datetime.month,
                                       day=1)
        date2 = first_of_month

        date1 = date2.replace(month=date2.month - 1)

    else:
        date1, date2 = None, None

    return date1, date2

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
