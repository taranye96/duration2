#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 17:31:50 2018

@author: tnye
"""

# Standard library imports 
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import numpy as np
import matplotlib.pyplot as plt

# Local imports
import baker_spectral


# Create array of spectral acceleration periods (s)
T = np.logspace(np.log10(0.05), np.log10(5), 250)

# Calcualte correlation coefficients
P = []
for i in range(len(T)):
    p = baker_spectral.get_Baker_eq6(T[i])
    P.append(p)

# Plot one against the other
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
ax.set_xscale('log')
plt.plot(T, P, 'ko')
plt.ylabel('Correlation coefficient')
plt.xlabel('Spectral acceleration period (s)')
ax.set_xlim(0.05, 5)
ax.set_ylim(0, 1)
plt.title('Baker 2007 figure 4')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Baker_fig.png', dpi=300)
