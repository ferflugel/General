import pandas as pd
import numpy as np
from uncertainties import unumpy
import matplotlib.pyplot as plt
import seaborn as sns

# Import data and convert to correct units before calculating Q
data = pd.read_csv('clean-data/velocities.txt')
data['velocity'] = data['velocity'] * (0.001/540)  # conversion: (0.001 m / 540 px)
velocity = np.array(data['velocity'].tolist())
voltage = np.array(data['voltage'].tolist())

# Setting arrays with uncertainties
velocity_u = np.ones(33) * 0.1 * (0.001/540)
velocity = unumpy.uarray(abs(velocity), velocity_u)
voltage_u = pd.read_csv('clean-data/voltage_uncertainties.txt', header=None).iloc[:, 0].to_list()
voltage = unumpy.uarray(voltage, voltage_u)

# Calculates Q using the velocities and voltages
constant = 2.024e-10
Q = constant * (velocity ** 1.5) / voltage

# Plotting in an initial histogram of Q
sns.set_style('white')
mean_uncertainty = unumpy.std_devs(Q).mean()
sns.histplot(unumpy.nominal_values(Q), binwidth=mean_uncertainty, kde=True,
             color='cornflowerblue', kde_kws={'bw_adjust': 0.3})
plt.xlabel('$Q_i$', fontsize=11)
plt.ylabel('Count', fontsize=11)
plt.title('Distribution of $Q_i$')
sns.despine()
plt.show()

# We now take get rid of the three outliers and re-plot it
Q = Q[Q < 3e-18]
sns.histplot(unumpy.nominal_values(Q), binwidth=4e-20,
             color='blue', alpha=0.3)
plt.xlabel('$Q_i$ $(C)$', fontsize=11)
plt.ylabel('Count', fontsize=11)
plt.title('Distribution of $Q_i$')
plt.ticklabel_format(axis="x", style="sci", scilimits=(-19, -19))
sns.despine()
plt.show()

# Now we normalize the values and plot them in a 45 degree line
guess = 1.9e-19
normalized_Q = Q / guess
sns.scatterplot(x=unumpy.nominal_values(normalized_Q),
                y=unumpy.nominal_values(normalized_Q), color='red', alpha=0.2)
plt.locator_params(nbins=11)
plt.xlim(0, 10.9)
plt.ylim(0, 10.9)
plt.title('$Q_i$ normalized by charge')
plt.grid()
sns.despine()
plt.xlabel('$Q_i$ $(C$ $/$ $charge)$', fontsize=11)
plt.ylabel('$Q_i$ $(C$ $/$ $charge)$', fontsize=11)
plt.show()
