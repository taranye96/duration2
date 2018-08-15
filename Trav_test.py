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

# Read in data frame. 
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Trav.csv')

# Obtain Vs30 Values.
Vs30 = df['Vs30(m/s)']
Rrup = df['rrup']

# Obtain observed Arias intensity values.
Ia_obs = df['Ia_arith(m/s)']

# Get predicted Arias intensity values.
Ia_pred = df['Trav_Ia']

# Plot figure
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
plt.plot(Vs30, Ia_pred, 'ko', label='FP Prediction')
plt.plot(Vs30, Ia_obs, 'r^', label='observed Arias')
plt.ylabel('Arias Intensity m/s')
plt.xlabel('Vs30 m/s')
plt.legend()
plt.title('Observations vs Trav predictions')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Trav_comparison_vs30.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
plt.plot(Rrup, Ia_pred, 'ko', label='FP Prediction')
plt.plot(Rrup, Ia_obs, 'r^', label='observed Arias')
plt.ylabel('Arias Intensity m/s')
plt.xlabel('Rrup km')
plt.legend()
plt.title('Observations vs Trav predictions')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Trav_comparison_rrup.png', dpi=300)

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
plt.title('Travasarou Predicted vs Observed')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Trav_comparison.png', dpi=300)