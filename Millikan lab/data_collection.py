import glob
import matplotlib.pyplot as plt
import numpy as np
import xlsxreader
import pandas as pd

# Manually collect velocity data (in px/s) and saves in velocities.txt
files = sorted([file for file in glob.glob('raw-data/*')])
for file in files:
    temp_file = xlsxreader.readxlsx(file).name
    df = pd.read_csv(temp_file, header=None)
    voltage = float(file[file.index('_') + 1:file.index('V')])
    y_positions = [float(x) for x in df.iloc[:, 0].to_list() if x != '#NV']
    L = len(y_positions)
    plt.plot(np.linspace(0, (L-1) * 0.1, L), y_positions)
    plt.grid()
    plt.locator_params(nbins=10)
    plt.show()
    velocity = input("Enter velocity: ")
    with open("clean-data/velocities.txt", "a") as file_object:
        file_object.write(f"\n{voltage},{velocity}")

print("Data collection done")
