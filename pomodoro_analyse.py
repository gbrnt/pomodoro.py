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


def only_incomplete(pomodoros):
    return [p for p in pomodoros if p[-1] == "0"]


def only_complete(pomodoros):
    return [p for p in pomodoros if p[-1] == "1"]


def filter_topic(pomodoros, topic):
    """
    Returns pomodoros whose names begin with topic
    The idea of my pomodoro system is that the first word is the topic
    """
    return [p for p in pomodoros if p[1].startswith(topic)]


def analyse_pomodoros(pomodoros, args):
    """Find and print statistics about pomodoros"""

    # Use string for output so that it can be written to file if desired
    output = ""

    # Commonly used stats
    total_pomodoros = len(pomodoros)
    first_pomodoro_start = dt_string_to_datetime(pomodoros[0][0])

    final = pomodoros[-1]
    final_pomodoro_start = dt_string_to_datetime(final[0])
    final_pomodoro_len = len_string_to_timedelta(final[2])
    final_pomodoro_end = final_pomodoro_start + final_pomodoro_len

    total_pomodoro_length = final_pomodoro_end - first_pomodoro_start

    if "breaks" in args.analyse:
        # Find average length of the breaks between pomodoros
        output += "\nAnalysing breaks"

        break_lengths = []
        last_end_time = datetime.timedelta(0)

        for pomo in pomodoros:
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
        average_timedelta = (
                sum(short_breaks, datetime.timedelta(0)) /
                len(short_breaks)
                )

        output += ("\nAverage length of breaks which were less than 1 "
                   "hour: {}\n".format(average_timedelta))

    if "frequency" in args.analyse:
        # A graph here would be nice
        # For now it just works out some frequency stats:
        # Per day, per week, time period

        output += "\nAnalysing frequency of valid pomodoros\n"

        pomodoros = only_complete(pomodoros)

        average_time_per = total_pomodoro_length / total_pomodoros

        output += ("On average, you did a pomodoro every {time} hours "
                   "between {start} and {end}.\n").format(
                           time=average_time_per,
                           start=first_pomodoro_start,
                           end=final_pomodoro_end)

        days = total_pomodoro_length.days
        weeks = days / 7

        pomodoros_per_day = total_pomodoros / days
        pomodoros_per_week = total_pomodoros / weeks

        output += "That's {ppd:.2f} pomodoros per day, or {ppw:.2f} per week!".format(
                ppd=pomodoros_per_day, ppw=pomodoros_per_week)

    if "complete" in args.analyse:
        output += "\nAnalysing completed pomodoros\n"

        complete_pomodoros = only_complete(pomodoros)
        incomplete_pomodoros = only_incomplete(pomodoros)

        total_complete = len(complete_pomodoros)
        total_incomplete = len(incomplete_pomodoros)

        # Percentages are a nice way to present this info
        perc_complete = (total_complete / total_pomodoros) * 100
        perc_incomplete = (total_incomplete / total_pomodoros) * 100

        output += ("Out of {total} total pomodoros:\n"
                   "  You completed {comp} pomodoros "
                   "({perc_comp:.2f}%).\n"
                   "  You left {incomp} incomplete pomodoros "
                   "({perc_incomp:.2f}%).\n"
                   ).format(total=total_pomodoros,
                            comp=total_complete,
                            perc_comp=perc_complete,
                            incomp=total_incomplete,
                            perc_incomp=perc_incomplete)
    
    if "count" in args.analyse:
        # Uses the pomodoro name argument as the type to count.
        # That's kind of hacky - might be a good idea to rework the arguments
        topic = args.name

        output += "\nAnalysing pomodoros for \"{}\"\n".format(topic)

        topic_pomodoros = filter_topic(pomodoros, topic)
        topic_total = len(topic_pomodoros)
        percentage_topic = topic_total / total_pomodoros * 100

        output += ("  {topic_total} pomodoros were done for {topic} "
                   "({percentage:.2f}%)\n"
                   ).format(topic_total=topic_total,
                            topic=topic,
                            percentage=percentage_topic)

    print(output)
