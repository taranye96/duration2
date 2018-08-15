#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 11:24:53 2018

@author: tnye
"""

# Standard library imports
import glob
import os

# Third party imports
from obspy import read
from amptools.stream import group_channels
import pandas as pd

# Local imports
#import processing
from amptools.io.read import read_data


def get_station_data(event, data_type):
    """
    Reads in seismic data, groups by station, and creates a list of station
    stats. 

    Args:
        event (str): USGS event ID. 
        data_type (str): Seismic data format.  
                         Options are: 
                            knt
                            kik
                            smc
                            V2_V3

    Returns:
        stations (array): Combined streams of acceleration data for each station.
        station_stats (list): Name, lat, lon, and elevation for each station.
        
    """

    # Define filepath and selected stations to use (if there are any).
    filepath = os.path.join('/Users/tnye/PROJECTS/Duration/data/events',
                            event, 'ground_motion', data_type)
    select_stns = os.path.join('/Users/tnye/PROJECTS/Duration/data/events',
                               event, 'select_stations', data_type + '.csv')

    os.chdir(filepath)

    # Select acceleration files and combine into a list.
    files_grabbed = []

    if data_type == 'knt':
        types = ('*.EW', '*.NS', '*.UD')
        for files in types:
            files_grabbed.extend(glob.glob(files))
    elif data_type == 'kik':
        types = ('*.EW2', '*.NS2', '*.UD2')
        for files in types:
            files_grabbed.extend(glob.glob(files))
    elif data_type == 'smc':
        types = ('*a.smc')
        for file in glob.glob(types):
            files_grabbed.append(file)
    elif data_type == 'v2':
        types = ('*.V2')
        for file in glob.glob(types):
            files_grabbed.append(file)

    # Read files using Amptools.
    data = []
    try:
        for i in range(len(files_grabbed)):
            data.append(read_data(files_grabbed[i]))
    except:
            print('Bad file', files_grabbed[i])
        

    # Filter out stations with poor records using a dataframe of pre-selected
    # station names for knet and kiknet events.
    names = pd.read_csv(select_stns, usecols=(['X']), sep=",")
    names_list = names.to_string(index=False)
    filtered_files = []
    for st in data:
        for i in range(len(st)):
            trace = st[i]
            if trace.stats.station in names_list:
                filtered_files.append([trace])
    data = filtered_files

    # Group all acceleration files by station if they are not already grouped.
    if len(data[0]) == 3:
        stations = data
    else:
        stations = group_channels(data)

    # Obtain stats for each station using the stats from the first trace
        # Also add station type to stats 
        # (read does not distinguish between knet and kik)
    station_stats = []
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[0]
            stn_type = trace.stats.standard['source_format']
            name = trace.stats['station']
            station_lat = trace.stats.coordinates['latitude']
            station_lon = trace.stats.coordinates['longitude']
            elev = trace.stats.coordinates['elevation']
            station_stats.append([stn_type, name, station_lat, station_lon, elev])

    return(stations, station_stats)


def get_knt_data(filepath, filtered_stations):
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
    names = pd.read_csv(filtered_stations, usecols=(['X']), sep=",")
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
        # Also add station type to stats 
        # (read does not distinguish between knet and kik)
    station_stats = []
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[0]
            trace.stats.type = 'Knet'
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


def get_kik_data(filepath, filtered_stations):
    """
    Reads a kik file for an earthquake with above surface horizontal and
    vertical components of acceleration, gathers it into 1 stream per station,
    and give station stats.

    Args:
        filepath (str): Absolute filepath to the earthquake data
        kik_profiles (str): Absolute filepath to kik-profiles.
        filtered_stations (csv): Csv of names of usable stations for the event.

    Returns:
        stations (array): Combined streams of acceleration data for
            each station.
        station_stats (list): Name, lat, and lon coordinates for each station.
    """

    # Create string of all the stations with usable data
    names = pd.read_csv(filtered_stations, usecols=(['X']), sep=",")
    names_list = names.to_string(index=False)
    
    # Obtain only the acceleration files from all of the event records.
    # .EW and .NS are horizontal components and .UD is the vertical component.
    os.chdir(filepath)
    types = ('*.EW2', '*.NS2', '*.UD2')
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))

    # Read files using Obspy
    data = []
    for i in range(len(files_grabbed)):
        data.append(read(files_grabbed[i]))

    # Select only stations that have usable data AND a kik-profile
    filtered_files = []
    for sta in data:
        for i in range(len(sta)):
            trace = sta[i]
            if trace.stats.station in names_list:
                filtered_files.append([trace])

    # Group all acceleration files by station.
    stations = group_channels(filtered_files)

    # Obtain stats for each station using the stats from the first trace
        # Also add station type to stats 
        # (read does not distinguish between knet and kik)
    station_stats = []
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[0]
            trace.stats.type = 'KIKnet'
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
    