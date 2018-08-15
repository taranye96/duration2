#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 14:11:52 2018

@author: tnye
"""

import glob
import os
from obspy.core.stream import Stream
from amptools.io.read import read_data
from obspy import UTCDateTime, read
from obspy.core import AttribDict
from reviewData import reviewData
from obspy.taup import TauPyModel
from obspy.geodetics import kilometer2degrees

evlat =  37.036
evlon = -121.880
dep = 17.2
event_time = UTCDateTime(1989, 10, 18, 0, 4, 15)

model = TauPyModel(model='iasp91')

##### Set Data type #####
data_type = []

if data_type == 'knt' or data_type == 'kik':
    
    # Read in one component of acceleration.
    st = read('/Users/tnye/PROJECTS/Duration/data/events/us2000dwh6/ground_motion/kik/*.NS2')

elif data_type == 'smc':

    # Read in one component of acceleration. 
    os.chdir('/Users/tnye/PROJECTS/Duration/data/events/nc216859/ground_motion/smc')
    files_grabbed = []
    for file in glob.glob('*a.smc'):
        files_grabbed.append(file)
    
    st_list = []
    for file in files_grabbed:
        data = read_data(file)
        st_list.append(data)
    flat_list = [item for sublist in st_list for item in sublist]
    
    st = Stream([])
    for trace in flat_list:
        st.append(trace)

elif data_type == 'v2':

    # Read in one component of acceleration. 
    os.chdir('/Users/tnye/PROJECTS/Duration/data/events/nc72282711/ground_motion/v2')
    files_grabbed = []
    for file in glob.glob('*.V2'):
        files_grabbed.append(file)

    st_list = []
    for file in files_grabbed:
        data = read_data(file)
        st_list.append(data[0])
    
    st = Stream([])
    for trace in st_list:
        st.append(trace)

# Turn station lats into attrib dict.
for tr in st:
    tr.stats.coordinates = AttribDict({'latitude': tr.stats.coordinates['latitude'],
                                       'longitude': tr.stats.coordinates['longitude'],
                                       'elevation': tr.stats.coordinates['elevation']})
    az12, az21, dist = reviewData.pyproj_distaz(tr.stats.coordinates['latitude'],
                                                tr.stats.coordinates['longitude'],
                                                evlat, evlon,)
    arr = model.get_travel_times(source_depth_in_km=dep,
                                 distance_in_degree=kilometer2degrees(dist),
                                 phase_list=['p', 'P'])
    tr.stats.rdist = dist
    tr.stats.ptime = arr[0].time

# Sort by distance from fault. 
st.sort(['rdist'])

# Determine picktimes. 
picktimes = [event_time + tr.stats.ptime for tr in st]

# Demean data. 
st.detrend('demean')

# Open interactive data analysis. 
zp = reviewData.InteractivePlot(st, picktimes=picktimes)

