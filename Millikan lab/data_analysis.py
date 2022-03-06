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
no_outliers = Q < 3e-18
Q = Q[no_outliers]
sns.histplot(unumpy.nominal_values(Q), binwidth=4e-20,
             color='blue', alpha=0.3)
plt.xlabel('$Q_i$ $(C)$', fontsize=11)
plt.ylabel('Count', fontsize=11)
plt.title('Distribution of $Q_i$')
plt.ticklabel_format(axis="x", style="sci", scilimits=(-19, -19))
sns.despine()
plt.savefig('figures/histogram', dpi=200)
plt.show()

# Now we normalize the values and plot them in a 45 degree line
guess = 1.75e-19
normalized_Q = Q / guess
sns.scatterplot(x=unumpy.nominal_values(normalized_Q),
                y=unumpy.nominal_values(normalized_Q), color='red', alpha=0.2)
plt.locator_params(nbins=12)
plt.xlim(0, 11.9)
plt.ylim(0, 11.9)
plt.title('$Q_i$ normalized by charge')
plt.grid()
sns.despine()
plt.xlabel('$Q_i$ $(C$ $/$ $charge)$', fontsize=11)
plt.ylabel('$Q_i$ $(C$ $/$ $charge)$', fontsize=11)
plt.savefig('figures/symmetry', dpi=200)
plt.show()

# Finding the residuals for the data and determining e
residuals_square = []
e = []
for guess in range(1600, 2000):
    guess = guess * 1e-22
    normalized_Q = Q / guess
    values = unumpy.nominal_values(normalized_Q)
    rounded = np.round(values)
    residuals = values - rounded
    residuals_square.append((residuals ** 2).sum())
    e.append(guess)

sns.lineplot(x=e, y=residuals_square, color='red', alpha=0.4)
plt.xlabel('$e$ (C)')
plt.ylabel('$\Sigma (y - \hat{y})^2$')
plt.title('Minimizing residuals')
plt.vlines(1.8e-19, 1.51, 2.9, ls='--', color='k', lw=1.2)
plt.text(1.717e-19, 2.8, 'Initial guess', fontsize=11)
plt.ylim(1.5, 3)
sns.despine()
plt.savefig('figures/fundamental_charge', dpi=200)
plt.show()

# We now create a plot for residuals
guess = 1.75e-19
normalized_Q = Q / guess
values = unumpy.nominal_values(normalized_Q)
rounded = np.round(values)
residuals = values - rounded
sns.scatterplot(x=rounded, y=residuals, color='blue', alpha=0.3)
plt.axhline(ls='--', color='k', lw='1.2')
plt.xlabel('$\hat{y}$')
plt.ylabel('$y - \hat{y}$')
plt.title('Residuals plot')
plt.ylim(-0.5, 0.5)
sns.despine()
plt.savefig('figures/residuals', dpi=200)
plt.show()

# Values for the radii of the droplets
radii = 9.915e-5 * velocity ** 0.5
radii = radii[no_outliers]
sns.histplot(unumpy.nominal_values(radii), binwidth=3e-8,
             color='blue', alpha=0.3)
plt.xlabel('$R$ $(m)$', fontsize=11)
plt.ylabel('Count', fontsize=11)
plt.title('Distribution of oil drop radii')
plt.ticklabel_format(axis="x", style="sci", scilimits=(-9, -9))
sns.despine()
plt.savefig('figures/radii', dpi=200)
plt.show()

# Correlation between radius and residuals
sns.scatterplot(x=unumpy.nominal_values(radii), y=unumpy.nominal_values(residuals),
                color='red', alpha=0.3)
plt.axhline(ls='--', color='k', lw='1.2')
plt.xlabel('$R$ $(m)$', fontsize=11)
plt.ylabel('$y - \hat{y}$')
plt.title('Residual vs Radius')
plt.ylim(-0.5, 0.5)
plt.ticklabel_format(axis="x", style="sci", scilimits=(-9, -9))
sns.despine()
plt.savefig('figures/radii_vs_residuals', dpi=200)
plt.show()
plt.show()

# Creating a latex table with the data
voltages_table = pd.DataFrame(np.array([list(unumpy.nominal_values(voltage)),
                 list(unumpy.std_devs(voltage))]).transpose(), columns=['a', 'b'])
print(voltages_table.to_latex(index=False))
