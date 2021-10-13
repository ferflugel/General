import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sm

BLUE = (0.12156862745098039, 0.4666666666666667, 0.7058823529411765)

# x, y, and uncertainty should be np arrays
def chi_square(x, y, uncertainty, function):
    chi_square_i = ((y - function(x)) / uncertainty)**2
    return chi_square_i.sum()


#%% Plots and analysis for the ammeter

# Data reading
ammeter = pd.read_csv('data/ammeter.csv')

# Plotting
plt.errorbar(ammeter['I'], ammeter['V'], xerr=ammeter['dI'], yerr=ammeter['dV'], fmt='.',
             color=BLUE)
sns.regplot(data=ammeter, x='I', y='V', order=1, ci=0, line_kws={'lw': 1, 'ls': '--', 'color': 'k'})
sns.despine()
plt.ylim(6.495, 6.505)
plt.ylabel('V (V)')
plt.xlabel('I (A)')
plt.title('V = 6.5000 + 0.0000 I')
plt.text(0.02, 6.5008, 'R$^2$ = 1.00\nχ$^2$ = 0.00')
plt.savefig('plots/option_1', dpi=180)
plt.show()

# Linear regression
ammeter['const'] = 1
model = sm.OLS(ammeter['V'], ammeter[['I'] + ['const']]).fit()
print(model.summary())

# Getting chi square
def fit_function(x):
    y = 6.5000 + 0 * x
    return y


X, Y, UNC = np.array(ammeter['I']), np.array(ammeter['V']), np.array(ammeter['dV'])
print(f'Variance: {Y.std()**2}')
print(f'Chi square: {chi_square(X, Y, UNC, fit_function)}')

#%% Plots and analysis for the voltmeter

# Data reading
voltmeter = pd.read_csv('data/voltmeter.csv')

# Plotting
plt.errorbar(voltmeter['I'], voltmeter['V'], xerr=voltmeter['dI'], yerr=voltmeter['dV'], fmt='.',
             color=BLUE)
sns.regplot(data=voltmeter, x='I', y='V', order=1, ci=0, line_kws={'lw': 1, 'ls': '--', 'color': 'k'})
sns.despine()
plt.ylim(6.495, 6.505)
plt.ylabel('V (V)')
plt.xlabel('I (A)')
plt.title('V = 6.5001 - 0.0334 I')
plt.text(0.02, 6.5, 'R$^2$ = 0.80\nχ$^2$ = 0.61')
plt.savefig('plots/option_2', dpi=180)
plt.show()

# Linear regression
voltmeter['const'] = 1
model = sm.OLS(voltmeter['V'], voltmeter[['I'] + ['const']]).fit()
print(model.summary())

# Finding chi square
X, Y, UNC = np.array(ammeter['I']), np.array(ammeter['V']), np.array(ammeter['dV'])

# Getting chi square
def fit_function2(x):
    y = 6.5001 - 0.0334 * x
    return y


X2, Y2, UNC2 = np.array(voltmeter['I']), np.array(voltmeter['V']), np.array(voltmeter['dV'])
print(f'Variance: {Y2.std()**2}')
print(f'Chi square: {chi_square(X2, Y2, UNC2, fit_function2)}')