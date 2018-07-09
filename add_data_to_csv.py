#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 14:05:13 2018

@author: tnye
"""

# Standard library imports
import math
import os

# Third party imports
import numpy as np
import pandas as pd

os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Local imports
import read_seismic
import calc_eq_data
import arias_intensity
import CAV


filepath = '/Users/tnye/PROJECTS/Duration/data/usp000g9h6/ground_motion/knt'
filt_stns = '/Users/tnye/PROJECTS/Duration/data/usp000g9h6/select_stations/knt.csv'


# Read knet data.
stations, station_stats = read_seismic.get_knet_data(filepath, filt_stns)

# Get source data.
event_id, date, mag, source_lat, source_lon, depth = calc_eq_data.get_earthquake_data(
        'usp000g9h6', stations)

# Add distance and P_wave arrival times to stats
calc_eq_data.get_dist_and_parrivals(stations, station_stats, source_lat,
                                    source_lon, depth)

# Get avg Arias intensity for horizontal components.
for sta in stations:
    for i in range(len(sta)):
        trace = sta[i]
        acc = np.multiply(0.01, trace.data)
        Ia, NIa, = arias_intensity.get_arias_intensity(acc,
                                                       trace.stats['delta'],
                                                       trace.stats.P_arriv)
        trace.stats.Ia = np.amax(Ia)


# Get avg CAV for horizontal components.
for sta in stations:
    for i in range(len(sta)):
        trace = sta[i]
        cav, cav5, cavstd = CAV.get_CAV(trace.data, trace.stats['delta'],
                                        trace.stats.P_arriv)
        trace.stats.CAV = np.amax(cav)
        trace.stats.CAV5 = np.amax(cav5)
        trace.stats.CAVstd = np.amax(cavstd)


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
Ia_geom = []
Ia_arith = []
CAV_geom = []
CAV_arith = []
CAV5_geom = []
CAV5_arith = []
CAVstd_geom = []
CAVstd_arith = []

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

        # Geometric mean
        ia_geom = (math.sqrt(stations[i][0].stats['Ia'] *
                             stations[i][2].stats['Ia']))
        cav_geom = (math.sqrt(stations[i][0].stats['CAV'] *
                              stations[i][2].stats['CAV']))
        cav5_geom = (math.sqrt(stations[i][0].stats['CAV5'] *
                               stations[i][2].stats['CAV5']))
        cavstd_geom = (math.sqrt(stations[i][0].stats['CAVstd'] *
                                 stations[i][2].stats['CAVstd']))
        
        # Arithmetic mean
        ia_arith = ((stations[i][0].stats['Ia'] +
                     stations[i][2].stats['Ia']) / 2)
        cav_arith = ((stations[i][0].stats['CAV'] +
                      stations[i][2].stats['CAV']) / 2)
        cav5_arith = ((stations[i][0].stats['CAV5'] +
                       stations[i][2].stats['CAV5']) / 2)
        cavstd_arith = ((stations[i][0].stats['CAVstd'] +
                         stations[i][2].stats['CAVstd']) / 2)

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
        Ia_geom.append(ia_geom)
        Ia_arith.append(ia_arith)
        CAV_geom.append(cav_geom)
        CAV_arith.append(cav_arith)
        CAV5_geom.append(cav5_geom)
        CAV5_arith.append(cav5_arith)
        CAVstd_geom.append(cavstd_geom)
        CAVstd_arith.append(cavstd_arith)

# Max horizontal component 
Ia_max = []
CAV_max = []
CAV5_max = []
CAVstd_max = []
for sta in stations:
    if sta[0].stats.Ia > sta[2].stats.Ia:
        Ia_max.append(sta[0].stats.Ia)
    else:
        Ia_max.append(sta[2].stats.Ia)

    if sta[0].stats.CAV > sta[2].stats.CAV:
        CAV_max.append(sta[0].stats.CAV)
    else:
        CAV_max.append(sta[2].stats.CAV)

    if sta[0].stats.CAV5 > sta[2].stats.CAV5:
        CAV5_max.append(sta[0].stats.CAV5)
    else:
        CAV5_max.append(sta[2].stats.CAV5)

    if sta[0].stats.CAVstd > sta[2].stats.CAVstd:
        CAVstd_max.append(sta[0].stats.CAVstd)
    else:
        CAVstd_max.append(sta[2].stats.CAVstd)

data = {'USGS_eventID': event_ids, 'magnitude': mags, 'depth(km)': depths,
        'source_lat': source_lats, 'source_lon': source_lons,
        'station_name': station_names, 'elev': elevations,
        'station_lat': station_lats, 'station_lon': station_lons,
        'rdist(km)': distances, 'Ia_geom': Ia_geom, 'Ia_arith': Ia_arith, 
        'Ia_max': Ia_max, 'CAV_geom': CAV_geom, 'CAV_arith': CAV_arith,
        'CAV_max': CAV_max, 'CAV5_geom': CAV5_geom, 'CAV5_arith': CAV5_arith,
        'CAV5_max': CAV5_max, 'CAVstd_geom': CAVstd_geom,
        'CAVstd_arith': CAVstd_arith, 'CAVstd_max': CAVstd_max}

filename = '/Users/tnye/PROJECTS/Duration/code/duration_data.csv'
df = pd.read_csv(filename)

dfnew = pd.DataFrame(data)
dfconcat = pd.concat([df, dfnew], sort=True)

columns = ['USGS_eventID', 'magnitude', 'depth(km)',
           'source_lat', 'source_lon',
           'station_name', 'elev(m)', 'station_lat',
           'station_lon', 'rdist(km)', 'rake_angle',
           'fault_type', 'Ia_geom', 'Ia_arith', 'Ia_max', 'CAV_geom',
           'CAV_arith', 'CAV_max', 'CAV5_geom', 'CAV5_arith', 'CAV5_max',
           'CAVstd_geom', 'CAVstd_arith', 'CAVstd_max', ' Vs30', 'PGA', 'PGV']

dfconcat.to_csv(filename, index=False, columns=columns)
