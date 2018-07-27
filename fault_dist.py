#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 09:53:39 2018

@author: tnye
"""

# Standard library imports
import os
from glob import glob

# Third party imports
import pandas as pd
import numpy as np
from shakelib.rupture.factory import get_rupture
from shakelib.rupture.origin import Origin
from shakelib.distance import get_distance

data_dir = '/Users/tnye/PROJECTS/Duration/data/'

# Read in data frame with all events
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/duration_data.csv')
evids = np.array(df['USGS_eventID'])
sta_lons = np.array(df['station_lon'])
sta_lats = np.array(df['station_lat'])

# Get list of event ids
event_ids = np.unique(df['USGS_eventID'])

# drop event that does not yet have fault text file
#event_ids = [e for e in event_ids if 'usp000g9h6' not in e]

# Temp numpy arrays for distances:
rrup_tmp = np.zeros_like(evids)
rjb_tmp = np.zeros_like(evids)
rx_tmp = np.zeros_like(evids)
ry_tmp = np.zeros_like(evids)

# Select an event
for i in range(len(event_ids)):
    event_id = event_ids[i]
    event_dir = os.path.join(data_dir, 'events', event_id)
    
    # Find the fault file
    rupt_dir = os.path.join(event_dir, 'rupture_info')
    rupt_file = glob(os.path.join(rupt_dir, '*_fault.txt'))[0]
    # need a dummy origin
    origin = Origin({
        'id':'', 
        'netid':'', 
        'network':'', 
        'lat':0, 
        'lon':0, 
        'depth':0,
        'locstring':'', 
        'mag':0, 
        'time':''
    })
    rupt = get_rupture(origin, rupt_file, new_format=False)
    
    # Get the stations for this event:
    idx = np.where(evids == event_id)[0]
    st_lons_i = sta_lons[idx]
    st_lats_i = sta_lats[idx]
    
    methods = ['rrup', 'rjb', 'rx', 'ry']
    distances = get_distance(
        methods, 
        lat=st_lats_i, 
        lon=st_lons_i, 
        dep = np.zeros_like(st_lats_i),
        rupture=rupt
    )
    
    # Fill in the distances for this event
    rrup_tmp[idx] = distances['rrup']
    rjb_tmp[idx] = distances['rjb']
    rx_tmp[idx] = distances['rx']
    ry_tmp[idx] = distances['ry']
    
# Append values to data frame
df['rrup'] = rrup_tmp
df['rjb'] = rjb_tmp
df['rx'] = rx_tmp
df['ry'] = ry_tmp
df.to_csv(os.path.join(data_dir, 'df_fault_dist.csv'))
