"""
Pomodoro.py - Utility to time and track pomodoros

db_interaction.py contains the common database interaction code for
pomodoro.py and pomodoro-export.py
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


def insert(connection, row_data):
    """Insert a row into the pomodoros table in the database"""
    cur = connection.cursor()
    cur.execute("INSERT INTO pomodoros VALUES (?,?,?,?)", row_data)


def shutdown(connection):
    """Safely close database"""
    connection.commit()
    connection.close()
