#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 16:40:48 2018

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

# Local imports
import gmpe

# Set grpah styles.
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
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_FP.csv')

# Obtain input values from data frame.
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']
rake = df['rake_angle']
Rrup = df['rrup']

# Predict Ia using Foulser-Piggott GMPE.
FP_Ia_mean, Ia_ref, sc = gmpe.get_FoulserPiggott(mag, Vs30, rake, Rrup)

# Obtain Arias intensity observations.
Ia_obs = df['Ia_arith(m/s)']

# Obtain Arias intensity predictions.
Ia_pred = df['FP_Ia']

# Take log of both sets of Arias intensity .
logIa_obs = np.log(Ia_obs)
logIa_pred = np.log(Ia_pred)

# Calculate residuals.
residuals = logIa_obs - logIa_pred


#####Residual Plots#####
# Vs30
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.plot(Vs30, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_xlim(90, 1500)
ax.set_ylim(-7.5, 7.5)
ax.set_ylabel('Residuals')
ax.set_xlabel('Vs30(m/s)')
ax.set_title('FP Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_residuals_vs30.png', dpi=300)

# Rrup
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.plot(Rrup, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_ylim(-7.5, 7.5)
ax.set_xlim(0, 600)
ax.set_ylabel('Residuals')
ax.set_xlabel('Rrup(km)')
ax.set_title('FP Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_residuals_rrup600.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.plot(Rrup, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_ylim(-7.5, 7.5)
ax.set_xlim(0, 100)
ax.set_ylabel('Residuals')
ax.set_xlabel('Rrup(km)')
ax.set_title('FP Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_residuals_rrup100.png', dpi=300)

# Reference Ia
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_xscale('log')
ax.plot(Ia_ref, residuals, 'ko')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_ylim(-7.5, 7.5)
ax.set_ylabel('Residuals')
ax.set_xlabel('Reference Ia')
ax.set_title('FP Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_residuals_refIa.png', dpi=300)
    