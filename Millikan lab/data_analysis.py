from functions import *
import glob
import xlsxreader
import numpy as np
from uncertainties import unumpy
import matplotlib.pyplot as plt
import seaborn as sns

velocity = []
voltage = []

# Reading the files and getting the voltages and velocities
files = sorted([file for file in glob.glob('data/*')])
for file in files:
    temp_file = xlsxreader.readxlsx(file).name
    df = pd.read_csv(temp_file, header=None)
    velocity.append(get_terminal_velocity(df.iloc[:, 0].to_list()))
    voltage.append(float(file[file.index('_') + 1:file.index('V')]))

# Setting arrays with uncertainties
velocity_u = np.ones(33)
velocity = unumpy.uarray(velocity, velocity_u)
voltage_u = pd.read_csv('uncertainties.txt', header=None).iloc[:, 0].to_list()
voltage = unumpy.uarray(voltage, voltage_u)

# Converting the velocity to m/s (missing)
velocity = velocity * (0.001/540) * 10  # conversion: (0.001 m / 540 px) * (10 frames / second)
constant = 1
Q = constant * (velocity ** 1.5) / voltage

# Plotting in a histogram of Q
mean_uncertainty = unumpy.std_devs(Q).mean()
sns.histplot(unumpy.nominal_values(Q), binwidth=mean_uncertainty/2, kde=True, color='k', kde_kws={'bw_adjust': 0.2})
sns.despine()
plt.show()
