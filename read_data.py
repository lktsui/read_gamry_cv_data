import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Read data file of Gamry CV format and separate cycles.
def read_cv_datafile(directory, filename, start_line):

    # Set up array for storing curve number
    curves_raw_dataset = []

    data_file = open(os.path.join(directory, filename))

    # Reads all lines starting from index provided by start_line variable
    # Python is 0-indexed so we begin at start_line - 1 since the first line is counted as line zero

    for line in data_file.readlines()[start_line-1:]:

        # Indicates start of a new curve. Generate new ones for the new curve.
        if line.startswith("CURVE"):

            # Generate new arrays
            time_array = []
            voltage_array = []
            current_array = []

            # Append new arrays to curves array
            curves_raw_dataset.append([time_array, voltage_array, current_array])


        # Data header -- Do nothing
        elif line.startswith("\tPt"):
            pass

        # Data unit header -- Do nothing
        elif line.startswith("\t#"):
            pass

        # Line is a data line - Load data
        else:

            # Split line into components using a tab ( \t ) separator
            data_elements = line.split("\t")

            # Data format: [Empty String, Data Point #, Time, V vs. Ref, Current, .... ]
            # Convert all values to floating point and append them to the curve's arrays
            time_array.append(float(data_elements[2]))
            voltage_array.append(float(data_elements[3]))
            current_array.append(float(data_elements[4]))


    # Process into Numpy arrays
    curves_numpy_dataset = []
    for curve_data in curves_raw_dataset:
        curves_numpy_dataset.append({'time':np.array(curve_data[0]),
                                'potential':np.array(curve_data[1]),
                                'current':np.array(curve_data[2]),
        })


    return curves_numpy_dataset

if __name__ == "__main__":
    curve_dataset = read_cv_datafile('data', 'AuWire_100mVs_0_0.6V_AU.DTA', 65)

    sns.set_style('whitegrid')
    colors = sns.color_palette("Set2", 3)

    # Generate figure and axes to plot to
    fig = plt.figure()
    fig.set_size_inches(8,6)
    ax = fig.add_subplot(111)

    ax.plot(curve_dataset[8]['potential'], 1e6*curve_dataset[8]['current'], color=colors[0], label = "Curve 9")
    ax.plot(curve_dataset[9]['potential'], 1e6*curve_dataset[9]['current'], color=colors[1], label = "Curve 10")
    ax.plot(curve_dataset[10]['potential'], 1e6*curve_dataset[10]['current'], color=colors[2], label = "Curve 11")
    ax.legend(fontsize=14)

    ax.tick_params(axis="both", which='major', labelsize=20)
    ax.set_ylabel("Current / $\mu A$", fontsize=24)
    ax.set_xlabel("Potential / V vs RE", fontsize=24)

    plt.tight_layout(pad=3)
    plt.show()





