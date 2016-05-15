__author__ = "Jared B Bowden"
__version__ = 1.0

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
fig = plt.figure(figsize=(40,10))

for file_number in range(len(data_files)):

    plt.subplot(len(data_files) * 100 + 10 + int(file_number) + 1)

    plt.plot(data_files[file_number].index, data_files[file_number]["x"], color="green", linewidth=0.5)
    plt.plot(data_files[file_number].index, data_files[file_number]["y"], color="green", linewidth=0.5)
    plt.plot(data_files[file_number].index, data_files[file_number]["z"], color="green", linewidth=0.5)
    plt.ylim(ymax=30, ymin=-30)
    plt.title(titles[file_number])

plt.tight_layout()
plt.show()
plt.close


fig = plt.figure(figsize=(40,10))

for file_number in range(len(data_files)):

    plt.subplot(len(data_files) * 100 + 10 + int(file_number) + 1)

    plt.plot(data_files[file_number].index, data_files[file_number]["abs_sum"], color="green", linewidth=0.5)

    #plt.ylim(ymax=30, ymin=-30)
    plt.title(titles[file_number])

plt.tight_layout()
plt.show()
plt.close


for file_number in range(len(data_files)):

    print titles[file_number]

    temp_file = data_files[file_number]

    print temp_file[temp_file["abs_sum"] >= 3.0]["abs_sum"]."describe()

    print ""

# TODO the next thing I had wanted to do was make some frequency histograms
fig = plt.figure(figsize=(5,20))

# We need to find the max frequency across all the files
max_freq = []

for file_number in range(len(data_files)):

    max_freq.append(data_files[file_number]["abs_sum"].value_counts().max())


for file_number in range(len(data_files)):

    # This is the kinda odd method I've arrived at to set the subplot information
    plt.subplot(len(data_files) * 100 + 10 + int(file_number) + 1)

    plt.hist(data_files[file_number]["abs_sum"], bins=100, normed=True)

    plt.xlim(0, 20)
    plt.ylim(0, max(max_freq) + 10000)
    plt.title(titles[file_number])

plt.tight_layout()
plt.show()
plt.close

# TODO add some parametric statistics to compare these groups
