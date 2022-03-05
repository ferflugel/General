import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Reading the files
c = pd.read_csv('data/personal_consumption.csv')
i = pd.read_csv('data/investment.csv')
g = pd.read_csv('data/government.csv')
nx = pd.read_csv('data/net_exports.csv')

# Merging all the files
for df in [i, g, nx]:
    c = pd.merge(c, df, how="left", on=["DATE"])
c['Y'] = c['C'] + c['I'] + c['G'] + c['NX']
data = c

# Selecting the correct range of quarters
lower_bound = data['DATE'] >= '2006-07-01'
upper_bound = data['DATE'] <= '2010-10-01'
data = data[lower_bound & upper_bound]

# Plotting line plots of all
sns.set_palette('pastel')
for column in data.columns[1:5]:
    sns.lineplot(data=data, x='DATE', y=column, label=column)
plt.xticks(['2007-01-01', '2008-01-01', '2009-01-01', '2010-01-01'], list(range(2007, 2011)))
plt.xlabel('Year')
plt.ylabel('Contribution to GDP change (percentage points)')
plt.legend(frameon=False, loc=4)
plt.title('Contributions to percentage change in GDP by components')
sns.despine()
plt.savefig('figures/gdp_components', dpi=100)
plt.show()

# Creating a latex table
columns = data.columns.tolist()
data = data[columns[0:1] + columns[5:6] + columns[1:5]]
print(data.to_latex(index=False))

# Creating raw-data for covid period
data = c
lower_bound = data['DATE'] >= '2019-10-01'
upper_bound = data['DATE'] <= '2021-10-01'
data = data[lower_bound & upper_bound]
columns = data.columns.tolist()
data = data[columns[0:1] + columns[5:6] + columns[1:5]]
print(data.to_latex(index=False))
