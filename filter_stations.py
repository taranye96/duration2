 a#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 14:11:52 2018

@author: tnye
"""

from obspy import UTCDateTime, read
from obspy.core import AttribDict
from reviewData import reviewData
from obspy.taup import TauPyModel
from obspy.geodetics import kilometer2degrees

evlat = 39.030
evlon = 140.881
dep = 7.8
event_time = UTCDateTime(2008, 6, 13, 23, 43, 45)

model = TauPyModel(model='iasp91')

st = read('/Users/tnye/PROJECTS/Duration/data/usp000g9h6/ground_motion/knt/*.NS')

# Turn station lats into attrib dict

for tr in st:
    tr.stats.coordinates = AttribDict({'latitude': tr.stats['knet']['stla'],
                                       'longitude': tr.stats['knet']['stlo'],
                                       'elevation': tr.stats['knet']['stel']})
    az12, az21, dist = reviewData.pyproj_distaz(evlat, evlon,
                                                tr.stats['knet']['stla'],
                                                tr.stats['knet']['stlo'])
    arr = model.get_travel_times(source_depth_in_km=dep,
                                 distance_in_degree=kilometer2degrees(dist),
                                 phase_list=['p', 'P'])

    tr.stats.rdist = dist
    tr.stats.ptime = arr[0].time

st.sort(['rdist'])
picktimes = [event_time + tr.stats.ptime for tr in st]

st.detrend('demean')
zp = reviewData.InteractivePlot(st, picktimes=picktimes)
# fig = reviewData.recsec(st, picktimes=picktimes)


# usp000a1b0 usp000d6vk usp000fg9t usp000g9h6
