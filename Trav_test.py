#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 13:26:21 2018

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



# Obtain Vs30 Values
Vs30 = df['Vs30(m/s)']
Rrup = df['rrup']

# Obtain observed Arias intensity values
Ia_obs = df['Ia_arith(m/s)']

# Get predicted Arias intensity values
Ia_pred = df['Trav_Ia']

# Get log of Arias intensities and Vs30 values
logVs30 = np.log10(Vs30)
logFP = np.log10(Ia_pred)
logArias = np.log10(Ia_obs)
logRrup = np.log10(Rrup)

# Plot figure
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
plt.plot(logVs30, logFP, 'ko', label='FP Prediction')
plt.plot(logVs30, logArias, 'r^', label='observed Arias')
plt.ylabel('log(Ia) m/s')
plt.xlabel('log(Vs30) (m/s)')
plt.legend()
plt.title('Observations vs Trav predictions')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Trav_comparison_vs30.png', dpi=300)