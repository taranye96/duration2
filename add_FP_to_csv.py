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
import pandas as pd

# Local imports
import gmpe

# Import data frame
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/add_Liu.csv')

# Obtain input values from data frame
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']
rake = df['rake_angle']
Rrup = df['rrup']

# Predict Ia using Foulser-Piggott GMPE
FP_Ia_mean = gmpe.get_FoulserPiggot(mag, Vs30, rake, Rrup)

# Add column for Liu predictions to data frame
df['FP_Ia'] = FP_Ia_mean
df.to_csv('/Users/tnye/PROJECTS/Duration/data/add_FP.csv')