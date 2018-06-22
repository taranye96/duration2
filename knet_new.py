#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 11:24:53 2018

@author: tnye
"""

from obspy import read
from amptools.stream import group_channels
from libcomcat.search import get_event_by_id
from obspy.geodetics import gps2dist_azimuth, kilometers2degrees
from obspy.taup import TauPyModel
from obspy import Stream, UTCDateTime
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
# from matplotlib.pyplot import close
import glob
import os


def get_knet_data(filepath):
    """
    Reads a knet file for an earthquake with horizontal and vertical components
    of acceleration, gathers it into 1 stream per station, and give station
    stats.

    Args:
        filepath (str): Absolute filepath to the earthquake data

    Returns:
        stations (array): Combined streams of acceleration data for
            each station.
        station_stats (list): Name, lat, and lon coordinates for each station.
    """

    os.chdir("/Users/tnye/PROJECTS/Duration/data/usp000a1b0/ground_motion/knt")
    types = ('*.EW', '*.NS', '*.UD')
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))

    data = []
    for i in range(len(files_grabbed)):
        data.append(read(files_grabbed[i]))

    stations = group_channels(data)

    station_stats = []
    for i in range(len(stations)):
        station = stations[i]
        trace = station[0]
        name = trace.stats['station']
        station_lat = trace.stats['knet']['stla']
        station_lon = trace.stats['knet']['stlo']
        elev = trace.stats['knet']['evlo']
        station_stats.append([name, station_lat, station_lon, elev])

    return (stations, station_stats)


def get_earthquake_data(event_id):
    """
    Obtains magnitude, latitude, longitude, and depth for an earthquake based
    off its event id.

    Args:
        event_id (str): USGS event id for a specific earthquake.

    Returns:
        date (time?): UTC date.time origin for source
        mag (float): Magnitude of earthquake.
        source_lat (float): Source latitude.
        source_lon (float): Source longitude.
        depth (float): Depth of earthquake origin in km.
    """

    detail = get_event_by_id(event_id)
    date = UTCDateTime(detail.time)
    mag = detail.magnitude
    source_lat = detail.latitude
    source_lon = detail.longitude
    depth = detail.depth

    return (date, mag, source_lat, source_lon, depth)


def append_station_stats(stations, station_stats, source_lat, source_lon,
                         depth):
    """
    Calculate distance between the source and each station for an event and
    the theoretical p-wave arrival times and appends them to the station stats.

    Args:
        stations (array): Combined streams of acceleration data for
            each station.
        station_stats (list): List of lat and lon coordinates for event.
        source_lat (float): Source latitude.
        source_lon (float): Source longitude.
        depth (float): Depth of earthquake origin in km.

    Returns:
        station_dist (array): Array of distances in km from each station to the
            source (not sorted by distance).
        p_arrivals (array): Array of p-wave arrival times to each station (not
                   sorted by distance).
    """

    model = TauPyModel(model="iasp91")
    station_dist = []           # unsorted
    p_arrivals = []             # unsorted
    for sta in stations:
        distances = []
        arrivals = []
        for i in range(len(sta)):
            trace = sta[i]
            dkm = gps2dist_azimuth(trace.stats['knet']['stla'],
                                   trace.stats['knet']['stlo'],
                                   source_lat, source_lon)
            dkm = dkm[0] / 1000.0
            dd = kilometers2degrees(dkm)
            p = model.get_travel_times(depth, dd, phase_list=['p', 'P'])

            trace.stats.rdist = dkm
            trace.stats.P_arriv = p[0].time
            distances.append(dkm)
            arrivals.append(p)
            station_dist.append(distances[0])
            p_arrivals.append(arrivals[0])

    return (station_dist, p_arrivals)


def plot_z_arrivals_by_dist(stations, date):
    """
    Plot vertical component p-wave arrivals on waveforms that are sorted by
    distance from source.

    Args:
    Returns:
    """

    stz = Stream()
    for sta in stations:
        newtrace = sta.select(channel='UD')
        stz += newtrace

    sorted_stz = stz.sort(keys=['rdist'])

    new_sorted = sorted_stz[0:9]

    fig = plt.figure()
    new_sorted.plot(fig=fig, show=False)
    for i in range(len(new_sorted)):
        p_onset = date + new_sorted[i].stats['P_arriv']

        ax = fig.axes[i]
        ax.axvline(date2num(p_onset.datetime), lw=2)
    plt.show
