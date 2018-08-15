#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 10:43:29 2018

@author: tnye
"""

# Third party imports 
import pandas as pd

# Import data frame
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_dist.csv')

# Select stations with Vs30 greater than 0
df2 = df[df['Vs30(m/s)'] > 0]

# Select stations with rrup less than or equal to 200 km
df3 = df2[df2['rrup'] <= 200]

# Create new csv with selected rows
df2.to_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/select_data.csv', index=False)
