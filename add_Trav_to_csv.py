#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 13:15:08 2018

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
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/add_FP.csv')

# Obtain input values from data frame
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']
rake = df['rake_angle']
Rrup = df['rrup']

# Predict Ia using Foulser-Piggott GMPE
Trav_Ia_mean = gmpe.get_Travasarou(mag, Vs30, rake, Rrup)

# Add column for Liu predictions to data frame
df['Trav_Ia'] = Trav_Ia_mean
df.to_csv('/Users/tnye/PROJECTS/Duration/data/add_Trav.csv')