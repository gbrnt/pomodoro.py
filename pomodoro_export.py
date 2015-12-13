#!/usr/bin/python

"""
pomodoro.py - Utility to time and track pomodoros

pomodoro-export.py contains the code for exporting the database to .csv.
This allows the csv to be analysed using another python script or just
something like Libreoffice.
"""

import db_interaction as db

# Length at which to cut off the pomodoro title when printing in terminal
TITLE_CUTOFF_LENGTH = 25


def export_data(csv_name, data_list):
    """Export data to csv file"""
    with open(csv_name, "w+") as csv_file:
        for entry in data_list:
            # Convert to comma-separated string
            entry_csv = ",".join([str(item) for item in entry]) + "\n"
            csv_file.write(entry_csv)

    print("Exported as", csv_name)


def get_pomodoros(db_name):
    """Get the pomodoro data from the database"""
    conn = db.startup(db_name)
    pomodoros = db.get_data(conn)
    db.shutdown(conn)

    return pomodoros


def get_last_n_pomodoros(db_name, num=1):
    """Get the last x pomodoros from the database"""
    connection = db.startup(db_name)
    cur = connection.cursor()
    db_query ="SELECT * FROM pomodoros ORDER BY datetime DESC LIMIT {};".format(num)
    pomodoros = cur.execute(db_query).fetchall()
    db.shutdown(connection)
    
    return pomodoros

def pomodoro_export(filename=None):
    """Get pomodoro data and call export_data to export to file"""
    if filename is None:
        try:
            filename = input("Enter filename for export\n> ")
        except KeyboardInterrupt:
            print("\nExport cancelled.")
            exit(0)

    if filename[-4:] != ".csv":
        filename = filename + ".csv"

    pomodoros = get_pomodoros("pomodoros.db")
    export_data(filename, pomodoros)


def list_pomodoros(db_name, num=5):
    """Get pomodoro data and list it to the terminal"""
    pomodoros = get_last_n_pomodoros(db_name, num)

    for pomo in pomodoros:
        # Title is cut off at TITLE_CUTOFF_LENGTH
        # and any shortness is made up for with " "s
        tcl = TITLE_CUTOFF_LENGTH
        pomo_title = "{{0: <{}}}".format(tcl).format(pomo[1][:tcl])

        # Remove seconds and milliseconds from datetime
        pomo_time = pomo[0][:-10]

        # Print a table
        print(pomo_time + " | " + pomo_title)

if __name__ == "__main__":
    pomodoro_export()
