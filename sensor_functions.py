__author__ = "Jared B Bowden"
__version__ = 1.2

import glob as glob
import pandas as pd
import matplotlib.pyplot as plt


def drop_start_and_stop(frame):
    """
    From what I can tell, the app (at its current settings) takes samples at
    200 / second

    Let's drop 2 minutes from the front of each recording session, and 5
    minutes off the end (I'm not so good at remembering to turn things off)

    5 minutes = 300 seconds * 200 = 60,000 lines
    2 minutes = 120 seconds * 200 = 24,000 lines
    """
    end = frame.shape[0] - 60000

    return frame.ix[24000:end, :]


def absolute_sum_accel(frame):
    """
    Will create a new column with the sum of acceleration in x, y, and z dimensions
    """
    frame["abs_sum"] = abs(frame["x"]) + abs(frame["y"]) + abs(frame["z"])

    return frame


def get_color(file_name):
    """
    Return activity-specific colors
    """
    activities = {"strolling": "blue",
                  "walking": "red",
                  "bike": "grey",
                  "gondolier": "green",
                  "car": "orange"}

    for activity in activities:

        if activity in file_name.lower():

            return activities[activity]
