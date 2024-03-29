#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:42:50 2018

@author: tnye
"""

# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import pandas as pd
import numpy as np
import scipy.constants as sp
import matplotlib.pyplot as plt
import seaborn as sns

# Set graph styles
sns.set_style("ticks",
    {
     'axes.axisbelow': True,
     'axes.facecolor': 'white',
     'axes.grid': True,
     'axes.labelcolor': '.15',
     'figure.facecolor': 'white',
     'grid.color': '.8',
     'grid.linestyle': '-',
     'image.cmap': 'rocket',
     'lines.solid_capstyle': 'round',
     'patch.edgecolor': 'w',
     'patch.force_edgecolor': True,
     'text.color': '.15',
     'xtick.color': '.15',
     'xtick.direction': 'out',
     'xtick.top': True,
     'xtick.bottom': True,
     'ytick.left': True,
     'ytick.right': True,
     'ytick.color': '.15',
     'ytick.direction': 'out'
     }
    )


# Import data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Liu.csv')

# Obtain PGA arithmetic mean values.
pga_arith = df['PGA_arith(cm/s/s)'] # units: cm/s/s
pga_arith = np.multiply(pga_arith, 0.01) # convert to m/s/s
pga_arith = pga_arith / sp.g # convert to g

# Obtain PGA greater of two horizontals.
pga_max = df['PGA_max(cm/s/s)'] # units: cm/s/s    
pga_max = pga_max * 0.01 # convert to m/s/s
pga_max = pga_max / sp.g # convert to g

# Obtain magnitudes and Vs30 values.
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']

# Obtain Liu Predictions.
Ia_pred = df['Liu_Ia']


# Get calculated Arias intensity values.
Ia_obs = df['Ia_arith(m/s)']
arias_max = df['Ia_max(m/s)']

# Get log of PGA and Arias intensities.
logPGAmax = np.log10(pga_max)
logLiu = np.log10(Ia_pred)
logArias = np.log10(Ia_obs)

# Plot both against pga
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
plt.plot(logPGAmax, logLiu, 'ko', label='Liu Prediction')
plt.plot(logPGAmax, logArias, 'r^', label='calculated Arias')
plt.ylabel('log(Ia) m/s')
plt.xlabel('log(PGA) g')
plt.legend()
plt.title('Liu prediction')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu_comparison.png', dpi=300)

# Plot one against the other
x = [10E-7, 10]
y = x
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(10E-7, 10)
ax.set_ylim(10E-7, 10)
plt.plot(Ia_obs, Ia_pred, 'ko')
plt.plot(x, y, 'r-')
plt.ylabel('Predicted Arias m/s')
plt.xlabel('Observed Arias m/s')
plt.title('Liu Predicted vs Observed')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu_comparison2.png', dpi=300)








