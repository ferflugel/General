import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)
df = pd.read_csv('data/part_2a.txt', sep='\t', skiprows=2)
print(df.head())

sns.set_palette('pastel')

sns.lineplot(data=df, x='Time(s)', y='Heater Energy (kJ)')
sns.despine()
plt.show()

sns.lineplot(data=df, x='Time(s)', y='T1(Deg C)')
sns.despine()
plt.show()
