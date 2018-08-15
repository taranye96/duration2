#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 17:54:47 2018

@author: tnye
"""

# Third party imports
import numpy as np
import pandas as pd


# Path to Vs30 values from geology. 
geo_vs30_path = '/Users/tnye/PROJECTS/Duration/data/Vs30/station_vs30.csv'

# Obtain list of other vs30 values (Cali and rest of Japan) extrapolated from
# geology and convert to string.
geo_vs30 = []
with open(geo_vs30_path) as f:
    lines = f.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].split(',')
    geo_vs30.append((lines[i][0], float(lines[i][3])))
geo_names = []
for i in range(len(lines)):
    geo_names.append(lines[i][0])
geo_names_str = ','.join(geo_names)

# Read in data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/duration_data.csv')

# Import station names and Vs30 values.
stn_names = np.array(df['station_name'])
vs30 = np.array(df['Vs30(m/s)'])

# Search for matching station names from the geology Vs30 and the data frame.
for i in range(len(stn_names)):
    if stn_names[i] in geo_names_str:
        for data in geo_vs30:
            if data[0] == stn_names[i]:
                df.set_value(i, 'Vs30(m/s)', data[1])

# Add changes to data frame
df.to_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/duration_data.csv', index=False)
