#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 15:21:19 2018

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
rdist = np.linspace(1, 100, 250)

# Define variables
vs30_1 = 180
vs30_2 = 360
vs30_3 = 760
vs30_4 = 1100

rake = 180
mag = 6

# Create list of Arias intensity values 
Ia_1 = []
Ia_2 = []
Ia_3 = []
Ia_4 = []
refIa = []

for i in range(len(rdist)):
    Ia1 = gmpe.get_FoulserPiggott_single(mag, vs30_1, rake, rdist[i])
    Ia2 = gmpe.get_FoulserPiggott_single(mag, vs30_2, rake, rdist[i])
    Ia3 = gmpe.get_FoulserPiggott_single(mag, vs30_3, rake, rdist[i])
    Ia4 = gmpe.get_FoulserPiggott_single(mag, vs30_4, rake, rdist[i])

    Ia_1.append(Ia1[0])
    Ia_2.append(Ia2[0])
    Ia_3.append(Ia3[0])
    Ia_4.append(Ia4[0])
    refIa.append(Ia4[1])

Amp_Ia1 = np.divide(Ia_1, Ia_4)
Amp_Ia2 = np.divide(Ia_2, Ia_4)
Amp_Ia3 = np.divide(Ia_3, Ia_4)

 
# Plot figure
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(refIa, Amp_Ia1, 'k-', label='180')
ax.plot(refIa, Amp_Ia2, 'r-', label='360')
ax.plot(refIa, Amp_Ia3, 'g-', label='760')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.legend()
#ax.set_xlim(1, 100)
ax.set_ylim(0.001, 10)
ax.set_ylabel('Ia(Vs30) / Ia(Vs30=1100)')
ax.set_xlabel('Reference Ia')
#ax.set_title('Foulser-Piggott Predictions')
#plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_fig9_360.png', dpi=300)
    
 