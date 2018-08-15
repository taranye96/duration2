#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 16:15:06 2018

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


# Import data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Liu_pred.csv')
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']
rrup = df['rrup']

# Obtain Arias intensity observations. 
Ia_obs = df['Ia_arith(m/s)']

# Obtain Arias intensity predictions.
Ia_pred = df['Liu_Ia_pred']

# Take log of both sets of Arias intensity. 
logIa_obs = np.log(Ia_obs)
logIa_pred = np.log(Ia_pred)

# Calculate residuals.
residuals = logIa_obs - logIa_pred


#####Residual Plots#####
# Vs30
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_xlim(90, 1500)
ax.plot(Vs30, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_ylim(-7.5, 7.5)
ax.set_ylabel('Residuals')
ax.set_xlabel('Vs30(m/s)')
ax.set_title('Liu Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu__pred_residuals_vs30.png',
            dpi=300)

# Rupture Distance
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.plot(rrup, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_xlim(0, 600)
ax.set_ylim(-7.5, 7.5)
ax.set_ylabel('Residuals')
ax.set_xlabel('Rrup')
ax.set_title('Liu Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu__pred_residuals_rrup600.png',
            dpi=300)




    