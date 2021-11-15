# %% Functions, settings, and visualization

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from uncertainties import ufloat
from uncertainties import unumpy as unp

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
    return ufloat(1000 * heat_loss, 1)


heat_loss_A = get_heat_loss('data/part_2a.txt', 200)
heat_loss_B = get_heat_loss('data/part_2b.txt', 200)
heat_loss_C = get_heat_loss('data/part_2c.txt', 200)
heat_loss_D = get_heat_loss('data/part_2d.txt', 200)


#%% Walls heat loss for each case

def inch_to_m(x):
    return 0.0254 * x


def get_walls_loss(file, start_time, gas_temp):
    data = pd.read_csv(file, sep='\t', skiprows=2)
    data = data[data['Time(s)'] > start_time]
    wall_temp = data['Wall Temp(Deg C)'].mean()
    k, l, r1, r2 = ufloat(0.185, 0.015), inch_to_m(ufloat(11.25, 0.001)), inch_to_m(ufloat(8 - 3/8, 0.045)), inch_to_m(ufloat(8, 0.045))
    walls_loss = 2 * k * np.pi * l * (ufloat(gas_temp, 0.1) - ufloat(wall_temp, 0.1)) / unp.log(r2/r1)
    return walls_loss


# Calculating the loss through the wall
walls_loss_A = get_walls_loss('data/part_2a.txt', 200, 40)
walls_loss_B = get_walls_loss('data/part_2b.txt', 200, 40)
walls_loss_C = get_walls_loss('data/part_2c.txt', 200, 60)
walls_loss_D = get_walls_loss('data/part_2d.txt', 200, 60)

# Calculating the loss through top and bottom
edge_loss_A = heat_loss_A - walls_loss_A
edge_loss_B = heat_loss_B - walls_loss_B
edge_loss_C = heat_loss_C - walls_loss_C
edge_loss_D = heat_loss_D - walls_loss_D
