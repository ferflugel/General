# %% Functions, settings, and visualization

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)

df = pd.read_csv('data/part_2d.txt', sep='\t', skiprows=2)
print(df.head())

sns.set_palette('pastel')

sns.lineplot(data=df, x='Time(s)', y='Heater Energy (kJ)')
sns.despine()
plt.show()

sns.lineplot(data=df, x='Time(s)', y='T1(Deg C)')
sns.despine()
plt.show()


# %% Heat loss for each case

def get_heat_loss(file, start_time):
    data = pd.read_csv(file, sep='\t', skiprows=2)
    data = data[data['Time(s)'] > start_time]
    dq = (data['Heater Energy (kJ)'].max() - data['Heater Energy (kJ)'].min())
    dt = (data['Time(s)'].max() - data['Time(s)'].min())
    heat_loss = dq / dt
    return heat_loss


heat_loss_A = get_heat_loss('data/part_2a.txt', 200)
heat_loss_B = get_heat_loss('data/part_2b.txt', 120)
heat_loss_C = get_heat_loss('data/part_2c.txt', 150)
heat_loss_D = get_heat_loss('data/part_2d.txt', 150)


#%% Walls heat loss for each case

def inch_to_m(x):
    return 0.0254 * x


# Outside temperature = 21.7C for all cases
def get_walls_loss(temperature):
    k, l, r1, r2 = 0.185, inch_to_m(11.25), inch_to_m(8 - 3/8), inch_to_m(8)
    walls_loss = 2 * k * np.pi * l * (temperature - 21.7) / np.log(r2/r1)
    return walls_loss / 1000


walls_loss_A, edge_loss_A = get_walls_loss(40), heat_loss_A - get_walls_loss(40)
walls_loss_B, edge_loss_B = get_walls_loss(40), heat_loss_B - get_walls_loss(40)
walls_loss_C, edge_loss_C = get_walls_loss(60), heat_loss_C - get_walls_loss(60)
walls_loss_D, edge_loss_D = get_walls_loss(60), heat_loss_D - get_walls_loss(60)

#%% Calculating cv for air


