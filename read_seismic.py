#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 11:24:53 2018

@author: tnye
"""

from obspy import read
import processing
from amptools.stream import group_channels
# from matplotlib.pyplot import close
import pandas as pd
import glob
import os


def get_knet_data(filepath, filtered_stations):
    """
    Reads a knet file for an earthquake with horizontal and vertical components
    of acceleration, gathers it into 1 stream per station, and give station
    stats.

    Args:
        filepath (str): Absolute filepath to the earthquake data.
        filtered_stations (csv): Csv of names of usable stations for the event.

    Returns:
        stations (array): Combined streams of acceleration data for
            each station.
        station_stats (list): Name, lat, and lon coordinates for each station.
    """

    # Obtain only the acceleration files.
    # .EW and .NS are horizontal components and .UD is the vertical component.
    os.chdir(filepath)
    types = ('*.EW', '*.NS', '*.UD')
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))

    # Read files using Obspy
    data = []
    for i in range(len(files_grabbed)):
        data.append(read(files_grabbed[i]))

    # Filter out stations with poor records using a dataframe of pre-selected
    # station names
    names = pd.read_csv(filtered_stations)
    names_list = names.to_string(index=False)
    filtered_files = []
    for st in data:
        for i in range(len(st)):
            trace = st[i]
            if trace.stats.station in names_list:
                filtered_files.append([trace])

    # Group all acceleration files by station.
    stations = group_channels(filtered_files)

    # Obtain stats for each station using the stats from the first trace
    station_stats = []
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[0]
            name = trace.stats['station']
            station_lat = trace.stats['knet']['stla']
            station_lon = trace.stats['knet']['stlo']
            elev = trace.stats['knet']['stel']
            station_stats.append([name, station_lat, station_lon, elev])

    # Demean data
    for sta in stations:
        sta.detrend('demean')

    # Add calibration to get data into gals (sm/s^2)
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[i]
            trace.data = trace.data * trace.stats.calib * 100

    # Set calibration to 1 to avoid double calibration when plotting.
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[i]
            trace.stats.calib = 1

    return (stations, station_stats)


def get_kik_data(filepath):
    """
    Reads a kik file for an earthquake with above surface horizontal and
    vertical components of acceleration, gathers it into 1 stream per station,
    and give station stats.

    Args:
        filepath (str): Absolute filepath to the earthquake data

    Returns:
        stations (array): Combined streams of acceleration data for
            each station.
        station_stats (list): Name, lat, and lon coordinates for each station.
    """

    # Obtain only the acceleration files.
    # .EW and .NS are horizontal components and .UD is the vertical component.
    os.chdir(filepath)
    types = ('*.EW2', '*.NS2', '*.UD2')
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))

    data = []
    for i in range(len(files_grabbed)):
        data.append(read(files_grabbed[i]))

    # Group all acceleration files by station.
    stations = group_channels(data)

    # Obtain stats for each station using the stats from the first trace
    station_stats = []
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[0]
            name = trace.stats['station']
            station_lat = trace.stats['knet']['stla']
            station_lon = trace.stats['knet']['stlo']
            elev = trace.stats['knet']['evlo']
            station_stats.append([name, station_lat, station_lon, elev])

    # Demean data
    for sta in stations:
        sta.detrend('demean')

    # Add calibration to get data into gals (sm/s^2)
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[i]
            trace.data = trace.data * trace.stats.calib * 100

    # Set calibration to 1 to avoid double calibration when plotting.
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[i]
            trace.stats.calib = 1

    return (stations, station_stats)


def get_USC_data(filepath):
    """
    Reads a USC file for an earthquake with horizontal and vertical components
    of acceleration, gathers it into 1 stream per station, and give station
    stats.

    Args:
        filepath (str): Absolute filepath to the earthquake data

    Returns:
        stations (array): Combined streams of acceleration data for
            each station.
        station_stats (list): Name, lat, and lon coordinates for each station.
    """

    # Obtain only the acceleration files.
    # .n0a and .n0c are horizontal and .n0b is vertical.
    os.chdir(filepath)
    types = ('*.n0a', '*.n0b', '*.n0c')
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))

    # Read in data
    data = []
    for i in range(len(files_grabbed)):
        data.append(processing.read_data(files_grabbed[i], units='acc'))
    
    # Group data by station
    stations = group_channels(data)
    
    # Obtain stats for each station using the stats from the first trace
    station_stats = []
    
    
    
    
    
    
    
    