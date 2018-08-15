#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 18:37:57 2018

@author: tnye
"""

# Third party imports
import numpy as np
import pandas as pd


# Path to rake values that original data frame code could not grab. 
rake_path = '/Users/tnye/PROJECTS/Duration/data/missing_rake.csv'

# Import list of rake angles.
rake = []
with open(rake_path) as f:
    lines = f.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].split(',')
    rake.append((lines[i][0], float(lines[i][1])))
rake_names = []
for i in range(len(lines)):
    rake_names.append(lines[i][0])
rake_names_str = ','.join(rake_names)

# Read in data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/duration_data.csv')

# Import station names and rake angles. 
evids = np.array(df['USGS_eventID'])
dfrake = np.array(df['rake_angle'])

# Search for Vs30 values in textfile of missing Vs30 data.
for i in range(len(evids)):
    if evids[i] in rake_names_str:
        for data in rake:
            if data[0] == evids[i]:
                df.set_value(i, 'rake_angle', data[1])

# Add changes to data frame
df.to_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/duration_data.csv', index=False)
