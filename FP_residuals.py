#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 16:40:48 2018

@author: tnye
"""

# Third party imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set grpah styles
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
Vs30 = df['Vs30(m/s)']
Rrup = df['rrup']

# Obtain Arias intensity observations 
Ia_obs = df['Ia_arith(m/s)']

# Obtain Arias intensity predictions
Ia_pred = df['FP_Ia']

# Take log of both sets of Arias intensity 
logIa_obs = np.log10(Ia_obs)
logIa_pred = np.log10(Ia_pred)

# Calculate residuals
residuals = logIa_obs - logIa_pred


#####Residual Plots#####
# Vs30
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.plot(Vs30, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_ylabel('Residuals')
ax.set_xlabel('Vs30(m/s)')
ax.set_title('FP Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_residuals_vs30.png', dpi=300)

# Rrup
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
#ax.set_xscale('log')
ax.plot(Rrup, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_ylabel('Residuals')
ax.set_xlabel('Rrup(km)')
ax.set_title('FP Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_residuals_rrup.png', dpi=300)
    