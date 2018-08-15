#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 15:20:12 2018

@author: tnye
"""

# Standard library imports
import glob
import os 
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import numpy as np
import pandas as pd

# Local imports
import fault_dist


# Data directory.
data_dir = '/Users/tnye/PROJECTS/Duration/data/'

# Read in data frame with all events.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_dip.csv')
evids = np.array(df['USGS_eventID'])

# Get list of event ids.
ids = np.unique(evids, return_index=True)[1]
events = [evids[index] for index in sorted(ids)]

Rrup = []
Rjb = []
Rx = []
Ry = []

for event in events:

    # Determine event directory. 
    event_dir = os.path.join(data_dir, 'events', event)
    
    # Select one event. 
    event_data = df[df['USGS_eventID'] == event]

    # Obtain station information for the selected event. 
    stn_lats = np.array(event_data['station_lat'])
    stn_lons = np.array(event_data['station_lon'])
    depths = np.array(event_data['depth(km)'])
    epdist = np.array(event_data['ep_dist(km)'])
    
    # Determine if there is a fault file.
    rupt_dir = os.path.join(event_dir, 'rupture_info')
    os.chdir(rupt_dir)
    rupture_file = []
    types = ('*_fault.txt', '*json')
    for file in types:
        rupture_file.extend(glob.glob(file))

    if len(rupture_file) != 0:
        filepath = os.path.join(rupt_dir, rupture_file[0])
        rrup, rjb, rx, ry = fault_dist.get_fault_dist(filepath, stn_lats,
                                                      stn_lons, depths)

    # If there is no fault file, use hypocentral dist for rrup.
    else:
        hypdist = np.sqrt(depths**2 + epdist**2)
        rrup = hypdist
        rjb = np.full_like(rrup, 0)
        rx = np.full_like(rrup, 0)
        ry = np.full_like(rrup, 0)
            
    Rrup.append(rrup)
    Rjb.append(rjb)
    Rx.append(rx)
    Ry.append(ry)

# Flatten lists. 
rrup = [item for sublist in Rrup for item in sublist]
rjb = [item for sublist in Rjb for item in sublist]
rx = [item for sublist in Rx for item in sublist]
ry = [item for sublist in Ry for item in sublist]

# Append to distances to data frame. 
df['rrup'] = rrup
df['rjb'] = rjb
df['rx'] = rx
df['ry'] = ry

df.to_csv(os.path.join(data_dir, 'dataframes', 'add_dist.csv'))
