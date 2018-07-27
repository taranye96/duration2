#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 16:27:17 2018

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

# Local imports
import gmpe

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

# Import data frame
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/add_FP.csv')

# Obtain Vs30 Values
Vs30 = df['Vs30(m/s)']
Rrup = df['rrup']

# Obtain observed Arias intensity values
Ia_obs = df['Ia_arith(m/s)']

# Get predicted Arias intensity values
Ia_pred = df['FP_Ia']

# Get log of Arias intensities and Vs30 values
logVs30 = np.log10(Vs30)
logFP = np.log10(Ia_pred)
logArias = np.log10(Ia_obs)
logRrup = np.log10(Rrup)

# Plot figure
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
plt.plot(Rrup, logFP, 'ko', label='FP Prediction')
plt.plot(Rrup, logArias, 'r^', label='observed Arias')
plt.ylabel('log(Ia) m/s')
plt.xlabel('log(Rrup) km')
plt.legend()
plt.title('Observations vs FP predictions')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_comparison_rrup.png', dpi=300)
