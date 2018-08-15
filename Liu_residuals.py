#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 13:45:29 2018

@author: tnye
"""

# Third party imports
import pandas as pd
import numpy as np
import scipy.constants as sp
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
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Liu.csv')
pga = df['PGA_max(cm/s/s)'] # units: cm/s/s
pga = pga * 0.01 # convert to m/s
pga = pga / sp.g # convert to g
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']
rrup = df['rrup']

# Obtain Arias intensity observations. 
Ia_obs = df['Ia_arith(m/s)']

# Obtain Arias intensity predictions.
Ia_pred = df['Liu_Ia']

# Take log of both sets of Arias intensity. 
logIa_obs = np.log(Ia_obs)
logIa_pred = np.log(Ia_pred)

# Calculate residuals.
residuals = logIa_obs - logIa_pred


#####Residual Plots#####
# PGA
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.plot(pga, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_xlim((10**-4), 2)
ax.set_ylim(-7.5, 7.5)
ax.set_ylabel('Residuals')
ax.set_xlabel('PGA(g)')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu_residuals_pga.png',
            dpi=300)

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
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu_residuals_vs30.png',
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
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu_residuals_rrup600.png',
            dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.plot(rrup, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_xlim(0, 100)
ax.set_ylim(-7.5, 7.5)
ax.set_ylabel('Residuals')
ax.set_xlabel('Rrup')
ax.set_title('Liu Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu_residuals_rrup100.png',
            dpi=300)

# Magnitude
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.plot(mag, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_ylim(-1, 1)
ax.set_ylabel('Residuals')
ax.set_xlabel('Magnitude')
ax.set_title('Liu Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu_residuals_mag.png',
            dpi=300)



    