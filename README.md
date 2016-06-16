pomodoro.py
===========
Utility to time and track pomodoros

Why you'd want to use it/why I made it

Doing pomodoros
---------------

Analysing pomodoros
-------------------

Exporting pomodoros
-------------------

Full help message
-----------------
This is the full help message obtained from running `python pomodoro.py -h`:

```
usage: pomodoro.py [-h] [-e EXPORT_FILENAME] [-m] [-d DATES DATES]
                   [-a [ANALYSIS_FILENAME [ANALYSIS_FILENAME ...]]] [-r]
                   [-l [N]] [-t POMODORO_LENGTH]
                   [NAME]

pomodoro.py - Utility to time and track pomodoros

positional arguments:
  NAME                  pomodoro name or export filename

optional arguments:
  -h, --help            show this help message and exit
  -e EXPORT_FILENAME, --export EXPORT_FILENAME
                        export to file EXPORT_FILENAME
  -m, --month           select pomodoros from last complete calendar month
  -d DATES DATES, --dates DATES DATES
                        select date range pomodoros should fall between,
                        inclusive
  -a [ANALYSIS_FILENAME [ANALYSIS_FILENAME ...]], --analyse [ANALYSIS_FILENAME [ANALYSIS_FILENAME ...]]
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

Future features
---------------

