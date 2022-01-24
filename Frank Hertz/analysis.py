import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import find_peaks

# Reads data from file
data_1 = pd.read_csv('data/data_1.txt', sep='\t')

# Plotting the data and minima
sns.lineplot(x=data_1['CH1 (V)  '], y=100 * data_1['CH2 (V)'])
peaks, _ = find_peaks((-1) * data_1['CH2 (V)'].to_numpy(), distance=75)
plt.plot(data_1['CH1 (V)  '][peaks], 100 * data_1['CH2 (V)'][peaks], "x")

# Showing the plot
sns.despine()
plt.show()
