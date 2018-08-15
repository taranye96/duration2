#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:10:19 2018

@author: tnye
"""

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
pga = np.linspace((10**-2), (10**0), 250)

# Define Vs30 values.
vs30_1 = np.full_like(pga, 180)
vs30_2 = np.full_like(pga, 500)
vs30_3 = np.full_like(pga, 760)

# Define Magnitudes.
mag_1 = np.full_like(pga, 4.0)
mag_2 = np.full_like(pga, 6.0)
mag_3 = np.full_like(pga, 8.0)

# Create list of Arias intensity values. 
Ia1, sc1 = gmpe.get_Liu(pga, mag_1, vs30_1)
Ia2, sc2 = gmpe.get_Liu(pga, mag_1, vs30_2)
Ia3, sc3 = gmpe.get_Liu(pga, mag_1, vs30_3)
Ia4, sc4 = gmpe.get_Liu(pga, mag_2, vs30_1)
Ia5, sc5 = gmpe.get_Liu(pga, mag_2, vs30_2)
Ia6, sc6 = gmpe.get_Liu(pga, mag_2, vs30_3)
Ia7, sc7 = gmpe.get_Liu(pga, mag_3, vs30_1)
Ia8, cs8 = gmpe.get_Liu(pga, mag_3, vs30_2)
Ia9, sc9 = gmpe.get_Liu(pga, mag_3, vs30_3)

# Plot figure
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
ax.plot(pga, Ia1, 'k-', label='Vs30=180')
ax.plot(pga, Ia2, 'r-', label='Vs30=500')
ax.plot(pga, Ia3, 'g-', label='Vs30=760')
ax.plot(pga, Ia4, 'k-')
ax.plot(pga, Ia5, 'r-')
ax.plot(pga, Ia6, 'g-')
ax.plot(pga, Ia7, 'k-')
ax.plot(pga, Ia8, 'r-')
ax.plot(pga, Ia9, 'g-')
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.legend()
ax.set_xlim((10**-2), (10**0))
ax.set_ylim((4E-4), (3E1))
ax.set_ylabel('Ia (m/s)')
ax.set_xlabel('PGA(g)')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu_fig3.png', dpi=300)
    
