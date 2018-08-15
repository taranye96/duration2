#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 12:53:43 2018

@author: tnye
"""


# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import pandas as pd
import numpy as np
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
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_multiGMPE.csv')
pga_obs = np.array(df['PGA_max(cm/s/s)'])
pga_pred = np.array(df['multiPGAgal'])
sa0_1_obs = np.array(df['SA(0.1)_rotd50'])
sa0_1_pred = np.array(df['multiSA(0.1)gal'])
sa1_obs = np.array(df['SA(1)_rotd50'])
sa1_pred = np.array(df['multiSA(1)gal'])


# Plot PGA
x = [0.1, 1000]
y = x
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(.1, 10E2)
ax.set_ylim(.1, 10E2)
plt.plot(pga_obs, pga_pred, 'ko')
plt.plot(x, y, 'r-')
plt.ylabel('Predicted PGA')
plt.xlabel('Observed PGA m/s')
plt.title('PGA Predicted vs Observed')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/multiGMPE_comparison_pga.png', dpi=300)

# Plot SA(0.1)
x = [10E-3, 1001]
y = x
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(10E-3, 10E1)
ax.set_ylim(10E-3, 10E1)
plt.plot(sa0_1_obs, sa0_1_pred, 'ko')
plt.plot(x, y, 'r-')
plt.ylabel('Predicted SA(0.1)')
plt.xlabel('Observed SA(0.1)')
plt.title('SA(0.1) Predicted vs Observed')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/multiGMPE_comparison_sa(0.1).png', dpi=300)

# Plot SA(1)
x = [10E-3, 100]
y = x
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(10E-3, 10E1)
ax.set_ylim(10E-3, 10E1)
plt.plot(sa1_obs, sa1_pred, 'ko')
plt.plot(x, y, 'r-')
plt.ylabel('Predicted SA(1)')
plt.xlabel('Observed SA(1)')
plt.title('SA(1) Predicted vs Observed')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/multiGMPE_comparison_sa(1).png', dpi=300)
