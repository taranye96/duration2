#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 09:12:48 2018

@author: tnye
"""

#%%
# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from obspy.core.stream import Stream
from scipy.stats import gaussian_kde

# Local imports
import read_seismic
import calc_eq_data
import arias_intensity
import CAV
import rot_components

#%%
# Event 1
filepath1 = '/Users/tnye/PROJECTS/Duration/data/usp000a1b0/ground_motion/knt'
filt_stns1 = '/Users/tnye/PROJECTS/Duration/data/usp000a1b0/select_stations/knt.csv'

# Get event data.
stations1, station_stats1 = read_seismic.get_knt_data(filepath1, filt_stns1)
event_id1, date1, mag1, source_lat1, source_lon1, depth1 = calc_eq_data.get_earthquake_data(
        'usp000a1b0', stations1)
calc_eq_data.get_dist_and_parrivals(stations1, station_stats1, depth1)

#%%
# Event 2
filepath2 = '/Users/tnye/PROJECTS/Duration/data/usp000d6vk/ground_motion/knt'
filt_stns2 = '/Users/tnye/PROJECTS/Duration/data/usp000d6vk/select_stations/knt.csv'

# Get event data.
stations2, station_stats2 = read_seismic.get_knt_data(filepath2, filt_stns2)
event_id2, date2, mag2, source_lat2, source_lon2, depth2 = calc_eq_data.get_earthquake_data(
        'usp000d6vk', stations2)
calc_eq_data.get_dist_and_parrivals(stations2, station_stats2, depth2)

#%%
# Event 3
filepath3 = '/Users/tnye/PROJECTS/Duration/data/usp000fg9t/ground_motion/knt'
filt_stns3 = '/Users/tnye/PROJECTS/Duration/data/usp000fg9t/select_stations/knt.csv'

# Get event data.
stations3, station_stats3 = read_seismic.get_knt_data(filepath3, filt_stns3)
event_id3, date3, mag3, source_lat3, source_lon3, depth3 = calc_eq_data.get_earthquake_data(
        'usp000fg9t', stations3)
calc_eq_data.get_dist_and_parrivals(stations3, station_stats3, depth3)

#%%
# Event 4
filepath4 = '/Users/tnye/PROJECTS/Duration/data/usp000g9h6/ground_motion/knt'
filt_stns4 = '/Users/tnye/PROJECTS/Duration/data/usp000g9h6/select_stations/knt.csv'

# Get event data.
stations4, station_stats4 = read_seismic.get_knt_data(filepath4, filt_stns4)
event_id4, date4, mag4, source_lat4, source_lon4, depth4 = calc_eq_data.get_earthquake_data(
        'usp000g9h6', stations4)
calc_eq_data.get_dist_and_parrivals(stations4, station_stats4, depth4)

#%%
# Other Event
filepath = '/Users/tnye/PROJECTS/Duration/data/small_quake/knt'
filt_stns = '/Users/tnye/PROJECTS/Duration/data/small_quake/knt.csv'

# Get event data. 
stations, station_stats = read_seismic.get_knt_data(filepath, filt_stns)
calc_eq_data.get_dist_and_parrivals(stations, station_stats, 33)

#%%
# Arias with pick times
filepath = '/Users/tnye/PROJECTS/Duration/data/usp000a1b0/ground_motion/knt'
filt_stns = '/Users/tnye/PROJECTS/Duration/data/usp000a1b0/select_stations/pick_arrivals.csv'
stations, station_stats = read_seismic.get_knet_data(filepath, filt_stns)
event_id, date, mag, source_lat, source_lon, depth = calc_eq_data.get_earthquake_data(
        'usp000a1b0', stations)
calc_eq_data.get_dist_and_parrivals(stations, station_stats, depth)

time = pd.read_csv(filt_stns, usecols=(['Y']), sep=",")
timevals = time.values
timelist = timevals.reshape(1, -1)
times = []
for x in timelist:
    for y in x:
        times.append(y)
hcomp = Stream()
for sta in stations:
    newtrace = sta.select(channel='NS')
    hcomp += newtrace
ratios = []
dist = []
for i in range(len(hcomp)):
    trace = hcomp[i]
    dt = trace.stats.delta
    acc = np.multiply(0.01, trace.data)
    Ia, NIa, = arias_intensity.get_arias_intensity(acc, dt, 0)
    newIa, newNIa = arias_intensity.get_arias_intensity(acc, dt, times[i])
    trace.stats.Ia = np.amax(Ia)
    trace.stats.pIa = np.amax(newIa)
    ratio = (trace.stats.pIa / trace.stats.Ia)
    trace.stats.ratio = ratio
    ratios.append(ratio)
    dist.append(trace.stats.distkm)
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
plt.ylim(0, 1.02)
plt.scatter(dist, ratios, s=20, c='k')
plt.ylabel('Arias w P-arriv : Arias')
plt.xlabel('Dist km')
plt.title('usp000a1b0')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/small_quake_arias.png', dpi=300)

#%%
# CAV with pick times
filepath = '/Users/tnye/PROJECTS/Duration/data/usp000a1b0/ground_motion/knt'
filt_stns = '/Users/tnye/PROJECTS/Duration/data/usp000a1b0/select_stations/pick_arrivals.csv'
stations, station_stats = read_seismic.get_knet_data(filepath, filt_stns)
event_id, date, mag, source_lat, source_lon, depth = calc_eq_data.get_earthquake_data(
        'usp000a1b0', stations)
calc_eq_data.get_dist_and_parrivals(stations, station_stats, depth)

time = pd.read_csv(filt_stns, usecols=(['Y']), sep=",")
timevals = time.values
timelist = timevals.reshape((1, -1))
times = []
for x in timelist:
    for y in x:
        times.append(y)
hcomp = Stream()
for sta in stations:
    newtrace = sta.select(channel='NS')
    hcomp += newtrace
ratiosCAV = []
ratiosCAV5 = []
ratiosCAVstd = []
dist = []
for i in range(len(hcomp)):
    trace = hcomp[i]
    dt = trace.stats.delta
    cav, cav5, cavstd = CAV.get_CAV(trace.data, dt, 0)
    newCAV, newCAV5, newCAVstd = CAV.get_CAV(trace.data, dt, times[i])
    trace.stats.CAV = np.amax(cav)
    trace.stats.pCAV = np.amax(newCAV)
    ratioCAV = (trace.stats.pCAV / trace.stats.CAV)
    trace.stats.ratioCAV = ratioCAV
    ratiosCAV.append(ratioCAV)
    dist.append(trace.stats.distkm)
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
plt.ylim(0.98, 1)
plt.scatter(dist, ratiosCAV, s=20, c='k')
plt.ylabel('CAV w P-arriv : CAV')
plt.xlabel('Dist km')
plt.title('usp000a1b0')
plt.savefig('/Users/tnye/PROJECTS/Duration/data/usp000a1b0/figures/pick_CAV_ratio.png', dpi=300)

#%%
# Rotationa-independent components
Ia_geom = []
Ia_arith = []
Ia_max = []
CAV_geom = []
CAV_arith = []
CAV_max = []
CAV5_geom = []
CAV5_arith = []
CAV5_max = []
CAVstd_geom = []
CAVstd_arith = []
CAVstd_max = []
dist = []

stations = stations1 + stations2 + stations3 + stations4 

for i in range(len(stations)):
    station = stations[i]
    dt = station[0].stats.delta
    ia_geom, ia_arith, ia_max = rot_components.get_RotComp_Arias(station, dt, 0)
    (cav_geom, cav5_geom, cavstd_geom,
     cav_arith, cav5_arith, cavstd_arith,
     cav_max, cav5_max,
     cavstd_max) = rot_components.get_RotComp_CAV(station, dt, 0)
    Ia_geom.append(ia_geom)
    Ia_arith.append(ia_arith)
    Ia_max.append(ia_max)
    CAV_geom.append(cav_geom)
    CAV_arith.append(cav_arith)
    CAV_max.append(cav_max)
    CAV5_geom.append(cav5_geom)
    CAV5_arith.append(cav5_arith)
    CAV5_max.append(cav5_max)
    CAVstd_geom.append(cavstd_geom)
    CAVstd_arith.append(cavstd_arith)
    CAVstd_max.append(cavstd_max)
    dist.append(station[0].stats.distkm)
Ia_Ratio_GeoArith = np.divide(Ia_geom, Ia_arith)
Ia_Ratio_GeoMax = np.divide(Ia_geom, Ia_max)
Ia_Ratio_ArithMax = np.divide(Ia_arith, Ia_max)
CAV_Ratio_GeoArith = np.divide(CAV_geom, CAV_arith)
CAV_Ratio_GeoMax = np.divide(CAV_geom, CAV_max)
CAV_Ratio_ArithMax = np.divide(CAV_arith, CAV_max)
CAV5_Ratio_GeoArith = np.divide(CAV5_geom, CAV5_arith)
CAV5_Ratio_GeoMax = np.divide(CAV5_geom, CAV5_max)
CAV5_Ratio_ArithMax = np.divide(CAV5_arith, CAV5_max)
CAVstd_Ratio_GeoArith = np.divide(CAVstd_geom, CAVstd_arith)
CAVstd_Ratio_GeoMax = np.divide(CAVstd_geom, CAVstd_max)
CAVstd_Ratio_ArithMax = np.divide(CAVstd_arith, CAVstd_max)

#%%
# Ia ratios
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
xy = np.vstack([dist, Ia_Ratio_GeoArith])
z = gaussian_kde(xy)(xy)
plt.scatter(dist, Ia_Ratio_GeoArith, s=20, c=z, edgecolor='')
plt.ylim(0, 1.02)
plt.ylabel('IaGeo : IaArith')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Ia_Ratio_GeoArith_density.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
xy = np.vstack([dist, Ia_Ratio_GeoMax])
z = gaussian_kde(xy)(xy)
plt.scatter(dist, Ia_Ratio_GeoMax, s=20, c=z, edgecolor='')
plt.ylim(0, 1.02)
plt.ylabel('IaGeo : IaMax')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Ia_Ratio_GeoMax_density.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
xy = np.vstack([dist, Ia_Ratio_ArithMax])
z = gaussian_kde(xy)(xy)
plt.scatter(dist, Ia_Ratio_ArithMax, s=20, c=z, edgecolor='')
plt.ylim(0, 1.02)
plt.ylabel('IaArith : IaMax')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Ia_Ratio_ArithMax_density.png', dpi=300)

#%%
# CAV ratios
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
xy = np.vstack([dist, CAV_Ratio_GeoArith])
z = gaussian_kde(xy)(xy)
plt.scatter(dist, CAV_Ratio_GeoArith, s=20, c=z, edgecolor='')
plt.ylim(0, 1.02)
plt.ylabel('CAVGeo : CAVArith')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/CAV_Ratio_GeoArith_density.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
xy = np.vstack([dist, CAV_Ratio_GeoMax])
z = gaussian_kde(xy)(xy)
plt.scatter(dist, CAV_Ratio_GeoMax, s=20, c=z, edgecolor='')
plt.ylim(0, 1.02)
plt.ylabel('CAVGeo : CAVMax')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/CAV_Ratio_GeoMax_density.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
xy = np.vstack([dist, CAV_Ratio_ArithMax])
z = gaussian_kde(xy)(xy)
plt.scatter(dist, CAV_Ratio_ArithMax, s=20, c=z, edgecolor='')
plt.ylim(0, 1.02)
plt.ylabel('CAVArith : CAVMax')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/CAV_Ratio_ArithMax_density.png', dpi=300)

#%%
# CAV5 ratios
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
plt.scatter(dist, CAV5_Ratio_GeoArith, s=20, c='k')
plt.ylim(0, 1.02)
plt.ylabel('CAV5Geo : CAV5Arith')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/CAV5_Ratio_GeoArith.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
plt.scatter(dist, CAV5_Ratio_GeoMax, s=20, c='k')
plt.ylim(0, 1.02)
plt.ylabel('CAV5Geo : CAV5Max')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/CAV5_Ratio_GeoMax.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
plt.ylim(0, 1.02)
plt.scatter(dist, CAV_Ratio_ArithMax, s=20, c='k')
plt.ylabel('CAV5Arith : CAV5Max')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/CAV5_Ratio_ArithMax.png', dpi=300)

#%%
# CAVstd ratios
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
plt.scatter(dist, CAV5_Ratio_GeoArith, s=20, c='k')
plt.ylim(0, 1.02)
plt.ylabel('CAVstdGeo : CAVstdArith')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/CAVstd_Ratio_GeoArith.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
plt.scatter(dist, CAV5_Ratio_GeoMax, s=20, c='k')
plt.ylim(0, 1.02)
plt.ylabel('CAVstdGeo : CAVstdMax')
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/CAVstd_Ratio_GeoMax.png', dpi=300)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
plt.scatter(dist, CAV_Ratio_ArithMax, s=20, c='k')
plt.ylabel('CAVstdArith : CAVstdMax')
plt.ylim(0, 1.02)
plt.xlabel('Dist km')
plt.title('4_Japanese_Events')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/CAVstd_Ratio_ArithMax.png', dpi=300)








