#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 11:53:30 2018

@author: tnye
"""

# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import pandas as pd
import numpy as np
import scipy.constants as sp

# Local imports
import gmpe

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

# Add column for Liu predictions to data frame
df['Liu_Ia'] = Liu_Ia
df.to_csv('/Users/tnye/PROJECTS/Duration/data/add_Liu.csv')