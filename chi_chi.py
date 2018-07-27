#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 11:26:28 2018

@author: tnye
"""

# Standard library imports
import os 
os.chdir('/Users/tnye/PROJECTS/Duration/code')

import glob

# Third party imports
import numpy as np
import scipy.constants as sp
import matplotlib.pyplot as plt
from amptools.io.dmg.core import read_dmg

# Local imports
import rot_components
import pga


filepath = '/Users/tnye/PROJECTS/Duration/data/events/chi_chi'

# Select all .V2 files for event
os.chdir(filepath)
files_grabbed = []
for file in glob.glob('*.V2'):
    files_grabbed.append(file)

files_grabbed.remove('CHY067.V2')    # read_dmg won't read file
    
# Read stations files
stations = []
for file in files_grabbed:
    print(file)
    file = '/Users/tnye/PROJECTS/Duration/data/events/chi_chi/' + file
    read_file = read_dmg(file)
    stations.append(read_file)

Ia_arith = []
PGA = []
for sta in stations:

    # Calc arithmetic mean for Arias intensity
    comp = rot_components.get_RotComp_Arias(sta, sta[0].stats.delta, 0)
    Ia_arith.append(comp[2])

    # Calc greater of two horizontals for PGA
    pga_arith, pga_max = pga.get_horizontal_pga(sta[1].data, sta[2].data)
    PGA.append(pga_max)

# Convert to m/s/s
PGA = np.multiply(PGA, 0.01)

# Cobvert to g
PGA = np.divide(PGA, sp.g)

# Obtain log of PGA 
logPGA = np.log10(PGA)

# Obtain log of Arias intensity 
logArias = np.log10(Ia_arith)

# Plot Figure
fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111)
plt.plot(logPGA, logArias, 'r.', label='calculated Arias')
plt.xlim(-2.5, 0)
plt.ylim(-3.5, 1.5)
plt.ylabel('log(Ia) m/s')
plt.xlabel('log(PGA) g')
plt.legend()
plt.title('1999 Chi Chi')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/chi_chi.png')