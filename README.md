pomodoro.py
===========
Utility to time and track pomodoros

Doing pomodoros
---------------
The main program can be run with `./pomodoro.py` or `python pomodoro.py`. Tested with Python 3, but there shouldn't be anything that doesn't work in python 2 (ok that's a lie - I just checked and `input()` needs to be changed to `raw_input()`.

You'll be greeted with:

```
Input task name
> ▯
```

Alternatively, add the pomodoro name after the command - for example `python pomodoro.py "Example pomodoro name"`. As in the example, if the name is multiple words long quotation marks will need to be used. This may change in future updates.

Once the task name is input, the pomodoro will start after 5 seconds, during which time it can be cancelled with `Ctrl-C`.

```
Pomodoro starting in 5 seconds...
Pomodoro started at [TIME]
```

When the pomodoro is complete, the `timer_done.wav` file will be played. The default is a short ding sound. It can be replaced with something more to your tastes if desired, although it should remain a `.wav` file.

If after starting the pomodoro is interrupted with `Ctrl-C`, the message `Pomodoro interrupted!` will be printed to the terminal. The start time, task name and duration of the interrupted pomodoro will still be stored in the database. The entry, however, will not be marked as complete.

Exporting pomodoros
-------------------
Pomodoro export functionality is used to export the pomodoro data from the database to a .csv file. The quickest way to do this is to run `python pomodoro.py -e EXPORT_FILENAME`. Alternatively, you can run `python pomodoro_export.py` and you will be prompted for a file name:

```
Enter filename for export
> ▯
```

The filename need not end with ".csv", but if it does not it will be automatically appended. The database will be read (I have not yet tested how long a large database will take to export, but it should be quick) and in the terminal it will print:

```
Exported as [NAME].csv
```

This csv can then be opened in a spreadsheet program for analysis. In future some basic analysis functions may be added.

Full help message
-----------------
This is the full help message obtained from running `python pomodoro.py -h`:

```
usage: pomodoro.py [-h] [-e EXPORT_FILENAME] [-m] [-d DATES DATES]
                   [-a [ANALYSIS_FILENAME]] [-r] [-l [N]] [-t POMODORO_LENGTH]
                   [NAME]

pomodoro.py - Utility to time and track pomodoros

positional arguments:
  NAME                  pomodoro name or export filename

optional arguments:
  -h, --help            show this help message and exit
  -e EXPORT_FILENAME, --export EXPORT_FILENAME
                        export to file EXPORT_FILENAME
  -m, --month           select pomodoros from last month
  -d DATES DATES, --dates DATES DATES
                        select dates pomodoros should fall between, inclusive
  -a [ANALYSIS_FILENAME], --analyse [ANALYSIS_FILENAME]
                        analyse pomodoros, with optional export to file
                        ANALYSIS_FILENAME
  -r, --repeat          Repeat last pomodoro
  -l [N], --list_pomodoros [N]
                        list last N pomodoros
  -t POMODORO_LENGTH, --time POMODORO_LENGTH
                        set pomodoro length in minutes
```

Dependencies
------------
There should be only one dependency which is not in the python stdlib - `sox` for its `play` command. On Windows, the `sox` main executable must be used (make sure it is added to the `PATH`). The device number may need to be changed in the `play_complete_sound()` function in `pomodoro.py`.
