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


# Import data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_FP.csv')

# Obtain PGA arithmetic mean values.
pga_arith = df['PGA_arith(cm/s/s)'] # units: cm/s/s
pga_arith = np.multiply(pga_arith, 0.01) # convert to m/s/s
pga_arith = pga_arith / sp.g # convert to g

# Obtain PGA greater of two horizontals.
pga_max = df['PGA_max(cm/s/s)'] # units: cm/s/s    
pga_max = pga_max * 0.01 # convert to m/s/s
pga_max = pga_max / sp.g # convert to g

# Obtain magnitudes and Vs30 values.
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']

# Predict Ia using Liu GMPE.
Liu_Ia, sc = gmpe.get_Liu(pga_max, mag, Vs30)

# Flatten lists of sigma constants.
flatSig = [item for sublist in sc[0] for item in sublist]
flatTau = [item for sublist in sc[1] for item in sublist]
flatSig_t = [item for sublist in sc[2] for item in sublist]

# Calculate residuals.
Ia_obs = np.array(df['Ia_arith(m/s)'])
logIa_obs = np.log(Ia_obs)
logIa_pred = np.log(Liu_Ia)
residuals = logIa_obs - logIa_pred

# Add column for Liu predictions and residuals to data frame.
df['Liu_Ia'] = Liu_Ia
df['Liu_Sig'] = flatSig
df['Liu_Tau'] = flatTau
df['Liu_Sig_t'] = flatSig_t
df['Liu_res'] = residuals

df.to_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Liu.csv')