#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 16:35:57 2018

@author: tnye
"""

# Third party imports
import numpy as np
import pandas as pd

# Path to list of dip angles for each event. 
dip_path = '/Users/tnye/PROJECTS/Duration/data/dips.csv'

# Read in dip angles.
dipvals = []
with open(dip_path) as f:
    lines = f.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].split(',')
    dipvals.append((lines[i][0], float(lines[i][1])))

# Read in data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_spec.csv')

# Import event IDs.
evids = np.array(df['USGS_eventID'])

# Search for mathcning event names from the dip angles and the data frame.
dip = []

for i in range(len(evids)):
    for event in dipvals:
        if event[0] == evids[i]:
            dip.append(event[1])


# Add dip angles to data frame.
df['dip'] = dip
df.to_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_dip.csv', index=False)
