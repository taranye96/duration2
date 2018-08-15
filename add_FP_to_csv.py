#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 16:08:38 2018

@author: tnye
"""

# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import numpy as np
import pandas as pd

# Local imports
import gmpe


# Import data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Trav.csv')

# Obtain input values from data frame.
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']
rake = df['rake_angle']
Rrup = df['rrup']

# Predict Ia using Foulser-Piggott GMPE.
FP_Ia, refIa, sc = gmpe.get_FoulserPiggott(mag, Vs30, rake, Rrup)

# Calculate residuals.
Ia_obs = np.array(df['Ia_arith(m/s)'])
logIa_obs = np.log(Ia_obs)
logIa_pred = np.log(FP_Ia)
residuals = logIa_obs - logIa_pred

# Add column for Liu predictions to data frame.
df['FP_Ia'] = FP_Ia
df['FP_d1'] = sc[0]
df['FP_d2'] = sc[1]
df['FP_d3'] = sc[2]
df['FP_SigE'] = sc[3]
df['FP_SigA'] = sc[4]
df['FP_res'] = residuals

df.to_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_FP.csv')
