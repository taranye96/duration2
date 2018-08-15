#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 15:59:36 2018

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
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_multiGMPE.csv')

# Get predicted PGA from dataframe.
pga = np.array(df['multiPGAgal'])
pga = pga * 0.01 # convert to m/s/s
pga = pga / sp.g # convert to g

# Get other imputs form data frame.
mag = np.array(df['magnitude'])
vs30 = np.array(df['Vs30(m/s)'])

# Calculate Arias intensity from Liu.
Ia, sc = gmpe.get_Liu(pga, mag, vs30)

# Calculate residuals.
Liu_Ia_obs = np.log(np.array(df['Liu_Ia']))
Liu_Ia_pred = np.log(Ia)
residuals = Liu_Ia_obs - Liu_Ia_pred

# Add predicted Arias to data frame.
df['Liu_Ia_pred'] = Ia
df['Liu_pred_res'] = residuals

df.to_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Liu_pred.csv', index=False)
