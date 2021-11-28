import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from uncertainties import unumpy
from uncertainties import ufloat

BLUE = (0.6313725490196078, 0.788235294117647, 0.9568627450980393)
ORANGE = (1.0, 0.4980392156862745, 0.054901960784313725)

# Loading the data into arrays
df = pd.read_csv('data.txt')
voltage = np.array(df['voltage(V)'])
current = np.array(df['current(A)'])
radius = np.array(df['diameter(cm)']) / 200

# Adding uncertainties
voltage = unumpy.uarray(voltage, np.ones(15) * 0.3)
current = unumpy.uarray(current, np.ones(15) * 0.0005)
radius = unumpy.uarray(radius, np.ones(15) * 0.0005)

# Finding the magnetic field by the coil
n, R = 130, ufloat(0.155, 0.00025)
B_c = (0.8 ** 1.5) * 4 * np.pi * 1e-7 * n * current / R

# Note that Y = sqrt(2V) / r
Y = ((2 * voltage) ** 0.5) / radius

# Regression
df['Y_0'] = 1
df['B_c'] = unumpy.nominal_values(B_c)
model = sm.OLS(pd.Series(unumpy.nominal_values(Y)), df[['B_c', 'Y_0']]).fit()
print('\n\n', model.summary())

a = 3.847e+05
b = 42.3101

a_error = ufloat(3.847e+05, 2 * 7165.711)
b_error = ufloat(42.3101, 2 * 8.026)

# Plotting
sns.set_palette('pastel')
sns.set_style('white')
plt.errorbar(unumpy.nominal_values(B_c), unumpy.nominal_values(Y), xerr=unumpy.std_devs(B_c), yerr=unumpy.std_devs(Y), fmt='.', color=BLUE,
             ecolor=BLUE, elinewidth=0.6, capsize=2)
x_range = np.array([0.00057, 0.00165])
sns.lineplot(x=x_range, y=a * x_range + b, color='k', lw=0.6)

plt.xlabel('B$_c$ (T)')
plt.ylabel('$\sqrt{2V}/r$ ($\sqrt{V}/m$)')
plt.title('$\sqrt{2V}/r$ vs B$_c$')

sns.despine()
plt.savefig('mass_to_charge_plot.png', dpi=150)
plt.show()

charge_to_mass = a_error ** 2
B_e = b_error / a_error

expected = a * B_c + b
chi_square = (Y - expected) ** 2 / expected
chi_square = chi_square.sum()
