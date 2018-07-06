#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 11:03:22 2018

@author: tnye
"""

# Standard library imports
import math
import os 

# Third party imports
import numpy as np
import pandas as pd
from obspy.core.stream import Stream
import matplotlib.pyplot as plt

os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Local imports
import read_seismic
import calc_eq_data
import arias_intensity
import CAV

filepath = '/Users/tnye/PROJECTS/Duration/data/usp000g9h6/ground_motion/knt'
filt_stns = '/Users/tnye/PROJECTS/Duration/data/usp000g9h6/ground_motion/knt/knt2008.csv'


# Read knet data.
stations, station_stats = read_seismic.get_knet_data(filepath, filt_stns)

# Get source data.
event_id, date, mag, source_lat, source_lon, depth = calc_eq_data.get_earthquake_data(
        'usp000g9h6', stations)

# Add distance and P_wave arrival times to stats
calc_eq_data.get_dist_and_parrivals(stations, station_stats, source_lat,
                                    source_lon, depth)


# Calc Arias intensity and add to stats
dt = 0.01
for sta in stations:
    for i in range(len(sta)):
        trace = sta[i]
        starttime = trace.stats.P_arriv
        acc = np.multiply(0.01, trace.data)
        Ia, NIa, = arias_intensity.get_arias_intensity(acc, 0.01, 0)
        newIa, newNIa = arias_intensity.get_arias_intensity(acc, 0.01, starttime)
        
        trace.stats.Ia = Ia
        trace.stats.NIa = NIa
        trace.stats.maxIa = np.amax(Ia)
        trace.stats.PIa = newIa
        trace.stats.PNIa = newNIa
        trace.stats.maxPIa = np.amax(newIa)
        
        time1 = arias_intensity.get_time_from_percent(NIa, 0.05, dt)
        time2 = arias_intensity.get_time_from_percent(NIa, 0.95, dt)
        trace.stats.arias5 = time1
        trace.stats.arias95 = time2    

# Gather all NS components into one stream and sort by dsit
hcomp = Stream()
for sta in stations:
    newtrace = sta.select(channel='NS')
    hcomp += newtrace

sorted_hcomp = hcomp.sort(keys=['distkm'])

# Plot ratio of arias with starttime to full arias
dist_source = []
maxIa = []
maxPIa = []
duration = []
ratio = []
for trace in sorted_hcomp:
    dist = trace.stats.distkm
    arias = trace.stats.maxIa
    Parias = trace.stats.maxPIa
    dur = (trace.stats.arias95 - trace.stats.arias5)
    Aratio = (Parias / arias)
    dist_source.append(dist)
    maxIa.append(arias)
    maxPIa.append(Parias)
    duration.append(dur)
    ratio.append(Aratio)

dist = np.array(dist_source)
arias = np.array(maxIa)
Parias = np.array(maxPIa)
durations = np.array(duration)
ratios = np.array(ratio)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
plt.scatter(dist, ratios, s=20, c='k')
plt.yscale('log')
plt.xscale('log')
plt.ylabel('Arias w P-arriv : Arias')
plt.xlabel('Dist km')
plt.title('usp000g9h6')
plt.show()
plt.savefig('/Users/tnye/PROJECTS/Duration/data/usp000g9h6/figures/Arias_ratio.png', dpi=300)