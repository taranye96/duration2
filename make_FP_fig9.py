#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 13:13:25 2018

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
rdist = np.logspace(0, 2, 250)

# Define variables
vs30 = np.full_like(rdist, 360)
rake = np.full_like(rdist, 180)

# Define Magnitudes
mag_1 = np.full_like(rdist, 5.5)
mag_2 = np.full_like(rdist, 6.5)
mag_3 = np.full_like(rdist, 7.5)

# Create list of Arias intensity values 
#Ia_1 = []
#Ia_2 = []
#Ia_3 = []

Ia1, refIa1 = gmpe.get_FoulserPiggott(mag_1, vs30, rake, rdist)
Ia2, refIa2 = gmpe.get_FoulserPiggott(mag_2, vs30, rake, rdist)
Ia3, refIa3 = gmpe.get_FoulserPiggott(mag_3, vs30, rake, rdist)

#    Ia_1.append(Ia1[0])
#    Ia_2.append(Ia2[0])
#    Ia_3.append(Ia3[0])
 
# Plot figure
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(rdist, Ia1, 'k-', label='Magnitude=5.5')
ax.plot(rdist, Ia2, 'r-', label='Magnitude=6.5')
ax.plot(rdist, Ia3, 'g-', label='Magnitude=7.5')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.legend()
ax.set_xlim(1, 100)
ax.set_ylim(0.001, 10)
ax.set_ylabel('Arias Intensity (m/s)')
ax.set_xlabel('Rrup(km)')
ax.set_title('Foulser-Piggott Predictions')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_fig9_360.png', dpi=300)
    
 