#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 15:43:33 2018

@author: tnye
"""

# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code'
         )
# Third party imports 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Local imports 
import gmpe

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



# Create list of PGA values
vs30 = np.logspace(1, 3, 250)

# Define variables
rake = np.full_like(vs30, 180)
rrup1 = np.full_like(vs30, 50)
rrup2 = np.full_like(vs30, 100)
rrup3 = np.full_like(vs30, 150)
mag_1 = np.full_like(vs30, 5.5)
mag_2 = np.full_like(vs30, 6.5)
mag_3 = np.full_like(vs30, 7.5)

Ia1, refIa1, sc1 = gmpe.get_FoulserPiggott(mag_1, vs30, rake, rrup1)
Ia2, refIa2, sc2 = gmpe.get_FoulserPiggott(mag_2, vs30, rake, rrup1)
Ia3, refIa3, sc3 = gmpe.get_FoulserPiggott(mag_3, vs30, rake, rrup1)
Ia4, refIa4, sc4 = gmpe.get_FoulserPiggott(mag_1, vs30, rake, rrup2)
Ia5, refIa5, sc5 = gmpe.get_FoulserPiggott(mag_2, vs30, rake, rrup2)
Ia6, refIa6, sc6 = gmpe.get_FoulserPiggott(mag_3, vs30, rake, rrup2)
Ia7, refIa7, sc7 = gmpe.get_FoulserPiggott(mag_1, vs30, rake, rrup3)
Ia8, refIa8, sc8 = gmpe.get_FoulserPiggott(mag_2, vs30, rake, rrup3)
Ia9, refIa9, sc9 = gmpe.get_FoulserPiggott(mag_3, vs30, rake, rrup3)

#####Plot figures#####
# Rrup = 50 km
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(vs30, Ia1, 'k-', label='Magnitude=5.5')
ax.plot(vs30, Ia2, 'r-', label='Magnitude=6.5')
ax.plot(vs30, Ia3, 'g-', label='Magnitude=7.5')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.legend()
ax.set_xlim(10, 1000)
ax.set_ylabel('Arias Intensity (m/s)')
ax.set_xlabel('Vs30 (m/s)')
ax.set_title('Arias Intensity vs Vs30 (rrup=50)')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_fig9vs_50.png', dpi=300)

# Rrup = 100 km
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(vs30, Ia4, 'k-', label='Magnitude=5.5')
ax.plot(vs30, Ia5, 'r-', label='Magnitude=6.5')
ax.plot(vs30, Ia6, 'g-', label='Magnitude=7.5')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.legend()
ax.set_xlim(10, 1000)
ax.set_ylabel('Arias Intensity (m/s)')
ax.set_xlabel('Vs30 (m/s)')
ax.set_title('Arias Intensity vs Vs30 (rrup=100)')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_fig9vs_100.png', dpi=300)

# Rrup = 150 km
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(vs30, Ia7, 'k-', label='Magnitude=5.5')
ax.plot(vs30, Ia8, 'r-', label='Magnitude=6.5')
ax.plot(vs30, Ia9, 'g-', label='Magnitude=7.5')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.legend()
ax.set_xlim(10, 1000)
ax.set_ylabel('Arias Intensity (m/s)')
ax.set_xlabel('Vs30 (m/s)')
ax.set_title('Arias Intensity vs Vs30 (rrup=150)')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_fig9vs_150.png', dpi=300)
    
    
    
 