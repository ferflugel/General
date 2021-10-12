import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
plt.xlabel('I (mA)')
plt.title('Voltage vs current for Option 1')
plt.show()

# Linear regression
ammeter['const'] = 1
model = sm.OLS(ammeter['V'], ammeter[['I'] + ['const']]).fit()
print(model.summary())

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
plt.xlabel('I (mA)')
plt.title('Voltage vs current for Option 2')
plt.show()

# Linear regression
voltmeter['const'] = 1
model = sm.OLS(voltmeter['V'], voltmeter[['I'] + ['const']]).fit()
print(model.summary())
