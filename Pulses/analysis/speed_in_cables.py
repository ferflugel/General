import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from uncertainties import unumpy

df = pd.read_csv('../experiment/coaxial.csv')

#%% Velocity analysis

df['velocity(c)'] = 20 * df['cable_length(m)'] / (3 * df['time(ns)'])
velocity_uncertainties = unumpy.uarray(list(df['velocity(c)']), list(df['velocity(c)'] / 100))
mean_velocity = velocity_uncertainties.mean()


#%% Attenuation analysis

df['attenuation(dB/m)'] = 10 * np.log10((df['V_reflected(V)'] / df['V_incident(V)'])**2) / df['cable_length(m)']
attenuation = df[df['termination(ohm)'] == 0]


