#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 13:15:08 2018

@author: tnye
"""

##### DO NOT USE THIS ONE. USE TRAVOQ CODE. #####


# Standard library imports.
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports.
import pandas as pd

# Local imports.
import gmpe

# Import data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Liu.csv')

# Obtain input values from data frame.
mag = df['magnitude']
Vs30 = df['Vs30(m/s)']
rake = df['rake_angle']
Rrup = df['rrup']

# Predict Ia using Travasarou. GMPE
Trav_Ia = gmpe.get_Travasarou(mag, Vs30, rake, Rrup)

