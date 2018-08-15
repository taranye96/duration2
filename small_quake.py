#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 11:08:18 2018

@author: tnye
"""

# Standard libray imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports. 
import pandas as pd
import read_seismic

# Paths to the small earthquake data and to the list of filtered stations. 
filepath = ('/Users/tnye/PROJECTS/Duration/data/small_quake/knt')
filt_stns = ('/Users/tnye/PROJECTS/Duration/data/small_quake/knt.csv')

# Read data. 
stations, station_stats = read_seismic.get_knt_data(filepath, filt_stns)

# Read in hand-picked pick times for the event. 
picktimes = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/small_quake/picktimes.csv')
pickvals = picktimes.values
picklist = []
for x in pickvals:
    for y in x:
        picklist.append(y)

