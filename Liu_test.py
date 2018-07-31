#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:42:50 2018

@author: tnye
"""

# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import pandas as pd
import numpy as np
import scipy.constants as sp
import matplotlib.pyplot as plt
import seaborn as sns

# Local imports
import gmpe

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

# Import data frame
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/df_fault_dist.csv')

# Obtain PGA arithmetic mean values
pga_arith = df['PGA_arith(cm/s/s)'] # units: cm/s/s
pga_arith = np.multiply(pga_arith, 0.01) # convert to m/s/s
pga_arith = pga_arith / sp.g # convert to g

# Obtain PGA greater of two horizontals
pga_max = df['PGA_max(cm/s/s)'] # units: cm/s/s    
pga_max = pga_max * 0.01 # convert to m/s/s
pga_max = pga_max / sp.g # convert to g

# Obtain magnitudes and Vs30 values
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']

# Predict Ia using Liu GMPE
Liu_Ia = gmpe.get_Liu_array(pga_max, mag, Vs30)


# Get calculated Arias intensity values
arias_arith = df['Ia_arith(m/s)']
arias_max = df['Ia_max(m/s)']

# Get log of PGA and Arias intensities
logPGAmax = np.log10(pga_max)
logLiu = np.log10(Liu_Ia[0])
logArias = np.log10(arias_max)

# Plot figure
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
plt.plot(logPGAmax, logLiu, 'ko', label='Liu Prediction')
plt.plot(logPGAmax, logArias, 'r^', label='calculated Arias')
plt.ylabel('log(Ia) m/s')
plt.xlabel('log(PGA) g')
plt.legend()
plt.title('Liu prediction')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Liu_comparison.png', dpi=300)
#plt.show()