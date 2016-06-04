__author__ = "Jared B Bowden"
__version__ = 1.2

import glob as glob
import matplotlib.pyplot as plt
import pandas as pd

base_path = "/Users/jaredbowden/Google Drive/cave_in_a_lake/data/sensor_project_data/"
activities = {"strolling": "blue",
              "walking": "purple",
              "biking": "grey",
              "gondolier": "green",
              "car": "orange"}
cut_off = 0.5

# Read in the other data files
file_names = glob.glob(base_path + "*txt")

# Split these path titles to use in chart titles
titles = []

for file in file_names:

    temp_title = file.split("/")[-1]

    titles.append(temp_title.split(".")[-2])

    del temp_title


def absolute_sum_accel(frame):
    """
    Will create a new column with the sum of acceleration in x, y, and z dimensions
    """
    frame["abs_sum"] = abs(frame["x"]) + abs(frame["y"]) + abs(frame["z"])

    return frame

# Read in the files
# TODO read in files with dates
data_files = {}

for file_number, file in enumerate(file_names):

    data_files[file_number] = absolute_sum_accel(pd.read_csv(file,
                                                             comment="#",
                                                             sep=" ",
                                                             header=None,
                                                             names=["x", "y",
                                                                    "z", "?"]))


def get_color(file_name):
    """
    Return activity-specific colors
    """
    for activity in activities:

        if activity in file_name.lower():

            return activities[activity]


fig = plt.figure(figsize=(10, 30))

for file_number in range(len(data_files)):

    plt.subplot(len(data_files), 1, file_number + 1)

    plt.plot(data_files[file_number].index,
             data_files[
                 file_number]["abs_sum"],
             color=get_color(titles[file_number]),
             linewidth=0.5)

    # TODO need to find axes max across files
    # TODO add axes labels
    # TODO consider adding the means and the median to the title, and shifting
    # the descriptive stats to above.
    #plt.ylim(ymax=30, ymin=-30)
    plt.title(titles[file_number])

plt.tight_layout()
plt.show()
plt.close

# TODO let's output this data as a sorted histogram
descriptive_stats = pd.DataFrame(columns=["title", "mean", "median", "std"])

for file_number in range(len(data_files)):

    temp_file = data_files[file_number]
    temp_file = temp_file[temp_file["abs_sum"] >= 0.5]["abs_sum"]

    # Make a temp frame to append
    temp_df = pd.DataFrame(data={"title": [titles[file_number]],
                                 "mean": [round(temp_file.mean(), 2)],
                                 "median": [round(temp_file.median(), 2)],
                                 "std": [round(temp_file.std(), 2)]})

    # Append the temp frame
    descriptive_stats = descriptive_stats.append(temp_df, ignore_index=True)

data_files[0][data_files["abs_sum"] >= 0.5]["abs_sum"]

# TODO this title is not accurate
print "\nDescriptive statistics (acceleration in m/s^2)"
print descriptive_stats.sort_values("mean", ascending=False)

fig = plt.figure(figsize=(5, 20))

for file_number in range(len(data_files)):

    # This is the kinda odd method I've arrived at to set the subplot
    # information
    plt.subplot(len(data_files) * 100 + 10 + int(file_number) + 1)

    # This is lazy
    temp_file = data_files[file_number]
    temp_file = temp_file[temp_file["abs_sum"] >= 0.5]["abs_sum"]

    plt.hist(temp_file, bins=100, normed=True, alpha=0.5)

    # FIXME this is not currently working
    """
    mean = round(temp_file.mean(), 2)
    median = round(temp_file.median(), 2)
    stdev = round(temp_file.std(), 2)
    plt.figtext(0.5, 0.5, str(mean))
    plt.figtext(0.5, 0.6,str(median))
    plt.figtext(0.5, 0.7, str(stdev))
    """

    plt.xlim(0, 10)
    plt.title(titles[file_number])
    plt.ylabel("Proportion of observations")
    plt.xlabel("acceleration (m/s^2)")

    del temp_file

plt.tight_layout()
plt.savefig("/Users/jaredbowden/Desktop/output.png")
plt.close

# TODO add some parametric statistics to compare these groups
stats_frame = pd.DataFrame(columns=["group", "abs_sum"])

for file_number in range(len(data_files)):

    temp_file = data_files[file_number]
    temp_file = temp_file[temp_file["abs_sum"] >= 0.5]["abs_sum"]

    # Make a temp frame to append
    temp_df = pd.DataFrame(
        data={"group": str(titles[file_number]) * len(temp_file),
              "abs_sum": temp_file.values})

    # Append the temp frame
    stats_frame = stats_frame.append(temp_df, ignore_index=True)

# FIXME
print ""
print pairwise_tukeyhsd(stats_frame["abs_sum"].values,
                        stats_frame["group"].values)
