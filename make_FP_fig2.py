#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 11:45:32 2018

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


# Create list of PGA values.
rrup = np.linspace(1, 100, 250)

# Define variables.
vs30 = np.full_like(rrup, 800)
rake = np.full_like(rrup, 180)

# Define Magnitudes.
mag_1 = np.full_like(rrup, 5.5)
mag_2 = np.full_like(rrup, 6.5)
mag_3 = np.full_like(rrup, 7.5)

# Create list of Arias intensity values. 
Ia1 = gmpe.get_Travasarou(mag_1, vs30, rake, rrup)
Ia2 = gmpe.get_Travasarou(mag_2, vs30, rake, rrup)
Ia3 = gmpe.get_Travasarou(mag_3, vs30, rake, rrup)
 
# Plot figure
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(rrup, Ia1, 'k-', label='Magnitude=5.5')
ax.plot(rrup, Ia2, 'r-', label='Magnitude=6.5')
ax.plot(rrup, Ia3, 'g-', label='Magnitude=7.5')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.legend()
ax.set_xlim(1, 100)
ax.set_ylim(0.01, 10)
ax.set_ylabel('Arias Intensity (m/s)')
ax.set_xlabel('Rrup(km)')
ax.set_title('Travasarou Predictions')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_fig2.png', dpi=300)
    
 