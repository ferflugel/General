import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import chisquare
from uncertainties import ufloat

BLUE = (0.6313725490196078, 0.788235294117647, 0.9568627450980393)
ORANGE = (1.0, 0.4980392156862745, 0.054901960784313725)

df = pd.read_csv('../experiment/delay.csv')
sns.set_palette('pastel')
sns.scatterplot(data=df, x='units(LC)', y='delay(us)')
x_err = []
plt.errorbar(df['units(LC)'], df['delay(us)'], xerr=0*df['units(LC)'], yerr=0.05 + df['delay(us)'] - df['delay(us)'], fmt='.k', color=BLUE,
             ecolor=BLUE)
sns.despine()
plt.xlabel('LC units (count)')
plt.ylabel('Delay (μs)')
plt.title('LC units vs. Delay', fontweight='bold')
plt.text(24, 0, 'Delay = 3.71 LC units + 0.02')

df['Yo'] = 1
model = sm.OLS(df['units(LC)'], df[['Yo'] + ['delay(us)']]).fit()
print('\n\n', model.summary())
sns.lineplot(x=np.array(range(0, 42)), y= 3.7133 * np.array(range(0, 42)) + 0.0200)

plt.savefig('../figures/lc_units_vs_time.png', dpi=100)
plt.show()

# Theoretical speed
df['v(LC/us)'] = df['units(LC)'] / df['delay(us)']
v_real = df['v(LC/us)'].mean() * 1e6
v_theory = 1 / np.sqrt(0.01e-6 * 1.5e-3)

df['expected'] = 0.02 + 3.7133 * df['units(LC)']
df['chi_square_i'] = (df['delay(us)'] - df['expected']) ** 2 / df['expected']
chi_square = df['chi_square_i'].sum()

# Theoretical velocity
C_0 = ufloat(0.01, 0.0003) * 10**-6
L_0 = ufloat(1.5, 0.015) * 10**-3
v = (1 / (C_0 * L_0)) ** 0.5

