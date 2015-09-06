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

Once the task name is input, the pomodoro will start after 5 seconds, during which time it can be cancelled with `Ctrl-C`.

```
Pomodoro starting in 5 seconds...
Pomodoro started at [TIME]
```

When the pomodoro is complete, the `timer_done.wav` file will be played. The default is a short ding sound. It can be replaced with something more to your tastes if desired, although it should remain a `.wav` file.

If after starting the pomodoro is interrupted with `Ctrl-C`, the message `Pomodoro interrupted!` will be printed to the terminal. The start time, task name and duration of the interrupted pomodoro will still be stored in the database. The entry, however, will not be marked as complete.

Exporting pomodoros
-------------------
`pomodoro_export.py` is used to export pomodoros into a csv file. Upon running it, it prints in the terminal:

```
Enter filename for export
> ▯
```

The filename need not end with ".csv", but if it does not it will be automatically appended. The database will be read (I have not yet tested how long a large database will take to export, but it should be quick) and in the terminal it will print:

```
Exported as [NAME].csv
```

This csv can then be opened in a spreadsheet program for analysis. As of this moment there are no plans to add analysis functions to pomodoro.py

Dependencies
------------
There should be only one dependency which is not in the python stdlib - `sox` for its `play` command. On Windows, the `sox` main executable must be used (make sure it is added to the `PATH`). The device number may need to be changed in the `play_complete_sound()` function in `pomodoro.py`.
