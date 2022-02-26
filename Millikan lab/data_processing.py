import glob
import pandas as pd
import xlsxreader
import numpy as np
from uncertainties import unumpy

velocity = []
voltage = []

# Reading the files and getting the voltages and velocities
files = sorted([file for file in glob.glob('data/*')])
for file in files:
    temp_file = xlsxreader.readxlsx(file).name
    df = pd.read_csv(temp_file, header=None)
    velocity.append(float(df.iloc[:, 0].max()))
    voltage.append(float(file[file.index('_') + 1:file.index('V')]))

# Setting arrays with uncertainties
velocity_u = np.ones(33)
velocity = unumpy.uarray(velocity, velocity_u)
voltage_u = pd.read_csv('uncertainties.txt', header=None).iloc[:, 0].to_list()
voltage = unumpy.uarray(voltage, voltage_u)

# Converting the velocity to m/s (missing)

constant = 1
Q = constant * (velocity ** 1.5) / voltage



