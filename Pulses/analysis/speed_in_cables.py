import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from uncertainties import unumpy
import statsmodels.api as sm

df = pd.read_csv('../experiment/coaxial.csv')

#%% Velocity analysis

BLUE = (0.6313725490196078, 0.788235294117647, 0.9568627450980393)

df['velocity(c)'] = 20 * df['cable_length(m)'] / (3 * df['time(ns)'])
#velocity_uncertainties = unumpy.uarray(list(df['velocity(c)']), list(df['velocity(c)'] / 100))
#mean_velocity = velocity_uncertainties.mean()

sns.set_palette('pastel')

df['Yo'] = 1
model = sm.OLS(df['time(ns)'], df[['Yo'] + ['cable_length(m)']]).fit()
print('\n\n', model.summary())
sns.lineplot(x=np.array(range(0, 85)), y= 10.0035 * np.array(range(0, 85)) + 2.9802, color='k', lw=0.5)

sns.scatterplot(data=df, x='cable_length(m)', y='time(ns)')
plt.errorbar(df['cable_length(m)'], df['time(ns)'], xerr=0*df['cable_length(m)'] + 0.02, yerr=0.05 + 0 * df['time(ns)'], fmt='.k', color=BLUE,
             ecolor=BLUE)

plt.xlabel('Cable length (m)')
plt.ylabel('Time (s)')
plt.title('Cable length vs. Time', fontweight='bold')
plt.text(49, 0, 'Time = 10.00 metres + 2.98')

sns.despine()

plt.savefig('../figures/cable_length_vs_time.png', dpi=100)
plt.show()

df['expected'] = 2.98 + 10.0035 * df['cable_length(m)']
df['chi_square_i'] = (df['time(ns)'] - df['expected']) ** 2 / df['expected']
chi_square = df['chi_square_i'].sum()

#%% Attenuation analysis

attenuation = df[df['termination(ohm)'] == 0]
V_r = unumpy.uarray(np.array(attenuation['V_reflected(V)']), 0.05 * np.ones(5))
V_i = unumpy.uarray(np.array(attenuation['V_incident(V)']), 0.05 * np.ones(5))
A = 10 * unumpy.log10((V_r / V_i)**2) / np.array(attenuation['cable_length(m)'])
A = A.mean()
A.std()



