#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 14:05:13 2018

@author: tnye
"""

# Standard library imports
import math

# Third party imports
import numpy as np
import pandas as pd

# Local imports
import read_seismic
import calc_eq_data
import arias_intensity
import CAV


filepath = '/Users/tnye/PROJECTS/Duration/data/usp000a1b0/ground_motion/knt'
filt_stns = '/Users/tnye/PROJECTS/Duration/data/usp000a1b0/ground_motion/knt/knt2000.csv'


# Read knet data.
stations, station_stats = read_seismic.get_knet_data(filepath, filt_stns)

# Get source data.
event_id, date, mag, source_lat, source_lon, depth = calc_eq_data.get_earthquake_data(
        'usp000a1b0', stations)

# Add distance and P_wave arrival times to stats
calc_eq_data.get_dist_and_parrivals(stations, station_stats, source_lat,
                                    source_lon, depth)

# Get avg Arias intensity for horizontal components.
for sta in stations:
    for i in range(len(sta)):
        trace = sta[i]
        acc = np.multiply(0.01, trace.data)
        Ia, NIa, = arias_intensity.get_arias_intensity(acc,
                                                       trace.stats['delta'])
        trace.stats.Ia = np.amax(Ia)


# Get avg CAV for horizontal components.
for sta in stations:
    for i in range(len(sta)):
        trace = sta[i]
        cav, cav5, cavstd = CAV.get_CAV(trace.data, trace.stats['delta'])
        trace.stats.CAV = cav
        trace.stats.CAV5 = cav5
        trace.stats.CAVstd = cavstd


# Add data to csv
event_ids = []
mags = []
depths = []
source_lats = []
source_lons = []
station_names = []
elevations = []
station_lats = []
station_lons = []
distances = []
Ias = []
CAVs = []
CAV5s = []
CAVstds = []

for i in range(len(stations)):
        event_id = stations[i][0].stats['eventID']
        mag = stations[i][0].stats['mag']
        depth = stations[i][0].stats['source_depth']
        source_lat = stations[i][0].stats['source_lat']
        source_lon = stations[i][0].stats['source_lon']
        station_name = stations[i][0].stats['station']
        elevation = stations[i][0].stats['knet']['stel']
        station_lat = stations[i][0].stats['knet']['stla']
        station_lon = stations[i][0].stats['knet']['stlo']
        distance = stations[i][0].stats['distkm']
#        Ia = (math.sqrt(stations[i][0].stats['Ia'] *
#                        stations[i][0].stats['Ia']))
#        CAV = (math.sqrt(stations[i][0].stats['CAV'] *
#                         stations[i][0].stats['CAV']))
#        CAV5 = (math.sqrt(stations[i][0].stats['CAV5'] *
#                          stations[i][0].stats['CAV5']))
#        CAVstd = (math.sqrt(stations[i][0].stats['CAVstd'] *
#                            stations[i][0].stats['CAVstd']))
        Ia = ((stations[i][0].stats['Ia'] +
               stations[i][0].stats['Ia']) / 2)
        CAV = ((stations[i][0].stats['CAV'] +
                stations[i][0].stats['CAV']) / 2)
        CAV5 = ((stations[i][0].stats['CAV5'] +
                 stations[i][0].stats['CAV5']) / 2)
        CAVstd = ((stations[i][0].stats['CAVstd'] +
                   stations[i][0].stats['CAVstd']) / 2)

        event_ids.append(event_id)
        mags.append(mag)
        depths.append(depth)
        source_lats.append(source_lat)
        source_lons.append(source_lon)
        station_names.append(station_name)
        elevations.append(elevation)
        station_lats.append(station_lat)
        station_lons.append(station_lon)
        distances.append(distance)
        Ias.append(Ia)
        CAVs.append(CAV)
        CAV5s.append(CAV5)
        CAVstds.append(CAVstd)

data = {'USGS_eventID': event_ids, 'magnitude': mags, 'depth(km)': depths,
        'source_lat': source_lats, 'source_lon': source_lons,
        'station_name': station_names, 'elev': elevations,
        'station_lat': station_lats, 'station_lon': station_lons,
        'rdist(km)': distances, 'Ia': Ias, 'CAV': CAVs,
        'CAV5': CAV5s, 'CAVstd': CAVstds}

filename = '/Users/tnye/PROJECTS/Duration/code/temp.csv'
df = pd.read_csv(filename)

dfnew = pd.DataFrame(data)
dfconcat = pd.concat([df, dfnew], sort=True)

columns = ['USGS_eventID', 'magnitude', 'depth(km)',
           'source_lat', 'source_lon',
           'station_name', 'elev(m)', 'station_lat',
           'station_lon', 'rdist(km)', 'rake_angle',
           'fault_type', 'Ia', 'CAV', 'CAV5',
           'CAVstd', ' Vs30', 'PGA', 'PGV']

dfconcat.to_csv(filename, index=False, columns=columns)
