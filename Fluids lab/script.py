#%% Data and configurations

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 20)

#%% Straight channels

blue = (0.12156862745098039, 0.4666666666666667, 0.7058823529411765)
orange = (1.0, 0.4980392156862745, 0.054901960784313725)

straight = pd.read_csv('data/straight.csv')

x_err = 0.05
y_err = 0.01
plt.errorbar(straight['Distance'], straight['Velocity'], xerr=x_err*straight['Distance'], yerr=y_err*straight['Velocity'], fmt='.k', color=blue,
             ecolor=blue)

sns.regplot(data=straight, x='Distance', y='Velocity', order=2, ci=0, line_kws={'lw': 1, 'ls': '--'})
plt.text(60, 0.9, 'Quadratic best fit', color=blue)

plt.xlabel('Distance from the edge (μm)')
plt.ylabel('Velocity (mm/s)')
plt.title('Velocity profile for straight channels')
sns.despine()

plt.savefig('plots/velocity_profile', dpi=180)
plt.show()

#%% Pressure head

pressure = pd.read_csv('data/pressure.csv')

# Before the pocket

sns.regplot(data=pressure, x='Distance BL', y='Velocity BL', order=2, ci=0,
            line_kws={'lw': 1, 'ls': '--'})
plt.errorbar(pressure['Distance BL'], pressure['Velocity BL'], xerr=x_err*pressure['Distance BL'], yerr=y_err*pressure['Velocity BL'], fmt='.k', color=blue,
             ecolor=blue)
plt.text(36, 2.4, 'High gravity head', color=orange)
sns.regplot(data=pressure, x='Distance BH', y='Velocity BH', order=2, ci=0,
            line_kws={'lw': 1, 'ls': '--'})
plt.errorbar(pressure['Distance BH'], pressure['Velocity BH'], xerr=x_err*pressure['Distance BH'], yerr=y_err*pressure['Velocity BH'], fmt='.k', color=orange,
             ecolor=orange)
plt.text(25, 1.3, 'Low gravity head', color=blue)

plt.xlabel('Distance from the edge (μm)')
plt.ylabel('Velocity (mm/s)')
plt.title('Velocity profile before change in width for different pressure heads')
sns.despine()

plt.savefig('plots/pressure_before', dpi=180)
plt.show()

# After the pocket

sns.regplot(data=pressure, x='Distance AL', y='Velocity AL', order=2, ci=0,
            line_kws={'lw': 1, 'ls': '--'})
plt.errorbar(pressure['Distance AL'], pressure['Velocity AL'], xerr=x_err*pressure['Distance AL'], yerr=y_err*pressure['Velocity AL'], fmt='.k', color=blue,
             ecolor=blue)
plt.text(110, 2.8, 'High gravity head', color=orange)
sns.regplot(data=pressure, x='Distance AH', y='Velocity AH', order=2, ci=0,
            line_kws={'lw': 1, 'ls': '--'})
plt.errorbar(pressure['Distance AH'], pressure['Velocity AH'], xerr=x_err*pressure['Distance AH'], yerr=y_err*pressure['Velocity AH'], fmt='.k', color=orange,
             ecolor=orange)
plt.text(95, 1.0, 'Low gravity head', color=blue)

plt.xlabel('Distance from the edge (μm)')
plt.ylabel('Velocity (mm/s)')
plt.title('Velocity profile after change in width for different pressure heads')
sns.despine()

plt.savefig('plots/pressure_after', dpi=180)
plt.show()
