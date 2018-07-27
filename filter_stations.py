#!/usr/bin/env python3
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

evlat =  35.512
evlon = 140.408
dep = 33
event_time = UTCDateTime(2005, 7, 17, 10, 51, 0)

model = TauPyModel(model='iasp91')

st = read('/Users/tnye/PROJECTS/Duration/data/small_quake/knt/*.NS')

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

zp = reviewData.InteractivePlot(st, picktimes=None)

# fig = reviewData.recsec(st, picktimes=picktimes)


# usp000a1b0 usp000d6vk usp000fg9t usp000g9h6
