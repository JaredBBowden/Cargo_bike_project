__author__ = "Jared B Bowden"
__version__ = 1.1

import glob as glob
import matplotlib.pyplot as plt
import pandas as pd

# Read in the other data files
file_names = glob.glob(
    "/Users/jaredbowden/Google Drive/cave in a lake/projects/sensor_project/sensor_data/*txt")

# Split these file names to use for the chart titles
titles = []

for file in file_names:

    temp_title = file.split("/")[-1]

    titles.append(temp_title.split(".")[-2])

    del temp_title


# Read in the files
# TODO read in files with dates
data_files = {}

for file_number, file in enumerate(file_names):

    data_files[file_number] = pd.read_csv(
        file, comment="#", sep=" ", header=None, names=["x", "y", "z", "?"])


# TODO add title specific color
def absolute_sum_accel(frame):
    """
    Will create a new column with the sum of acceleration in x, y, and z dimensions
    """
    frame["abs_sum"] = abs(frame["x"]) + abs(frame["y"]) + abs(frame["z"])

    return

for file_number in range(len(data_files)):

    absolute_sum_accel(data_files[file_number])

# PLOTTING FROM HERE

# OK, let's plot things up
fig = plt.figure(figsize=(40, 10))

for file_number in range(len(data_files)):

    plt.subplot(len(data_files) * 100 + 10 + int(file_number) + 1)

    plt.plot(data_files[file_number].index, data_files[
             file_number]["x"], color="green", linewidth=0.5)
    plt.plot(data_files[file_number].index, data_files[
             file_number]["y"], color="green", linewidth=0.5)
    plt.plot(data_files[file_number].index, data_files[
             file_number]["z"], color="green", linewidth=0.5)
    plt.ylim(ymax=30, ymin=-30)
    plt.title(titles[file_number])

plt.tight_layout()
plt.show()
plt.close


fig = plt.figure(figsize=(40, 10))

for file_number in range(len(data_files)):

    plt.subplot(len(data_files) * 100 + 10 + int(file_number) + 1)

    plt.plot(data_files[file_number].index, data_files[
             file_number]["abs_sum"], color="green", linewidth=0.5)

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
    temp_df = pd.DataFrame(data = {"title": [titles[file_number]],
                                    "mean": [round(temp_file.mean(), 2)],
                                    "median": [round(temp_file.median(), 2)],
                                    "std": [round(temp_file.std(), 2)]})

    # Append the temp frame
    descriptive_stats = descriptive_stats.append(temp_df, ignore_index=True)

print "\nDescriptive statistics (acceleration in m/s^2)"
print descriptive_stats.sort_values("mean", ascending = False)


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
