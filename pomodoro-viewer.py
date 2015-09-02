#!/usr/bin/python

"""
pomodoro-export.py - Export pomodoro.py database to .csv

This allows the csv to be analysed using another python script or just
something like Libreoffice.
"""

import sqlite3      # For database connection


def startup(db_name):
    """Open database, return connection"""
    connection = sqlite3.connect(db_name)
    cur = connection.cursor()

    # Create table on first start
    cur.execute("CREATE TABLE IF NOT EXISTS pomodoros"
                "(datetime, task, length, complete)")

    return connection


def get_data(connection):
    """Convert the data in the database for export"""
    cur = connection.cursor()
    # Fetch all records from the table
    pomo_cursor = cur.execute("SELECT * FROM pomodoros").fetchall()

    return pomo_cursor


def export_data(csv_name, data_list):
    """Export data to csv file"""
    with open(csv_name, "w+") as csv_file:
        for entry in data_list:
            # Convert to comma-separated string
            csv_file.write(",".join(entry) + "\n")

    print("Exported as", csv_name)


def shutdown(connection):
    """Safely close database"""
    connection.commit()
    connection.close()


def pomodoro_export():
    """Run the other methods"""
    filename = input("Enter filename for export\n> ")
    if filename[-4:] != ".csv":
        filename = filename + ".csv"

    conn = startup("pomodoros.db")
    pomodoros = get_data(conn)
    export_data(filename, pomodoros)
    shutdown(conn)

pomodoro_export()
