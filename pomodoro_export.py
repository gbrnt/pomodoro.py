#!/usr/bin/python

"""
pomodoro-export.py - Export pomodoro.py database to .csv

This allows the csv to be analysed using another python script or just
something like Libreoffice.
"""

import db_interaction as db


def export_data(csv_name, data_list):
    """Export data to csv file"""
    with open(csv_name, "w+") as csv_file:
        for entry in data_list:
            # Convert to comma-separated string
            csv_file.write(",".join(entry) + "\n")

    print("Exported as", csv_name)


def pomodoro_export():
    """Run the other methods"""
    filename = input("Enter filename for export\n> ")
    if filename[-4:] != ".csv":
        filename = filename + ".csv"

    conn = db.startup("pomodoros.db")
    pomodoros = db.get_data(conn)
    export_data(filename, pomodoros)
    db.shutdown(conn)

pomodoro_export()
