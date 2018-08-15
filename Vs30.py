#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:10:20 2018

@author: tnye
"""

# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports 
import pandas as pd
import numpy as np


def knet_Vs30(stations):
    """
    Obtains Vs30 values from a knet spreadsheet or from a text file of Vs30
    values extrapolated from geology for a list of knet stations. Stations not
    listed in the either are added to a spreadsheet for missing Vs30 data. 

    Args:
        stations (array): Array of knet stations. 
           
    Returns:
        Vs30 (array): Array of Vs30 values for the knet stations.

    """

    # Knet spreadsheet
    knet_vs30 = '/Users/tnye/PROJECTS/Duration/data/Vs30/knet_xtrap.csv'
    # Vs30 from geology textfile
    geo_vs30_path = '/Users/tnye/PROJECTS/Duration/data/Vs30/japan_map/geo_vs30'
    # Spreadsheet with station names missing Vs30 data
    missing_vs30_path = '/Users/tnye/PROJECTS/Duration/data/Vs30/missing_vs30.csv'

    # Read in spreadsheet with knet Vs30 values and convert station names to string.
    data = pd.read_csv(knet_vs30, usecols=(['X', 'Y']), sep=",")
    datavals = data.values
    names = []
    for i in range(len(datavals)):
        names.append(datavals[i][0])
    names_str = ','.join(names)

    # Obtain list of vs30 values extrapolated from geology and convert to string.
    geo_vs30 = []
    with open(geo_vs30_path) as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split('\t')
        geo_vs30.append((lines[i][2], float(lines[i][3])))
    geo_names = []
    for i in range(len(lines)):
        geo_names.append(lines[i][2])
    geo_names_str = ','.join(geo_names)

    # Read in spreadsheet of missing Vs30 values and convert to string. 
    df = pd.read_csv(missing_vs30_path)
    missingvals = df.values
    missing_names = []
    for i in range(len(missingvals)):
        missing_names.append(missingvals[i][0])
    missing_names_str = ','.join(missing_names)
    
    # Obtain Vs30 values for stations.
    Vs30 = []
    stn_names = []
    stn_lats = []
    stn_lons = []

    for sta in stations:   
        stn_name = sta[0].stats.station
        lat = sta[0].stats.coordinates['latitude']
        lon = sta[0].stats.coordinates['longitude']

        # Search for station data in knet spreadsheet.
        if stn_name in names_str:

            # Select Vs30 values from spreadsheet that match the station names.
            for data in datavals:
                if data[0] == stn_name:
                    for i in range(len(sta)):
                        sta[i].stats.vs30 = data[1]
                    Vs30.append(data[1])

        # Search for station data in geoVs30 file. 
        elif stn_name in geo_names_str:

            # Select Vs30 values from geoVs30 data that match the station names.
            for data in geo_vs30:
                if data[0] == stn_name:
                    for i in range(len(sta)):
                        sta[i].stats.vs30 = data[1]
                    Vs30.append(data[1])

        # Add station information to spreadsheet for missing vs30 data.  
        else:
            Vs30.append(np.nan)
            if stn_name in missing_names_str:
                pass
            else:
                stn_names.append(stn_name)
                stn_lats.append(lat)
                stn_lons.append(lon)
                
    missing_data = {'Station': stn_names, 'Station_lat': stn_lats,
                                'Station_lon': stn_lons}
    dfnew = pd.DataFrame(missing_data)
    dfconcat = pd.concat([df, dfnew], sort=True)
    columns = ['Station', 'Station_lat', 'Station_lon']
    
    dfconcat.to_csv(missing_vs30_path, index=False, columns=columns)
                

    return(Vs30)


def kik_Vs30(stations):
    """
    Calculates Vs30 values for a list Kik-net stations using a KIKnet profile.
    Stations without a profile will search for Vs30 value from a list of Vs30
    values extrapolated from geology.  If station is not in this list, it is
    added to a spreadsheet for missing Vs30 data. 
    
    Args:
        stations (array): Array of Kik-net stations.

    Returns:
        Vs30 (array): Array of Vs30 values for the KIKnet stations. 

    """

    # KIKnet velocity profiles 
    profile_path = '/Users/tnye/PROJECTS/Duration/data/Vs30/kik_profiles/'
    # Vs30 from geology textfile
    geo_vs30_path = '/Users/tnye/PROJECTS/Duration/data/Vs30/japan_map/geo_vs30'
    # Spreadsheet with station names missing Vs30 data
    missing_vs30_path = '/Users/tnye/PROJECTS/Duration/data/Vs30/missing_vs30.csv'

    # Obtain list of vs30 values extrapolated from geology and convert to string.
    geo_vs30 = []
    with open(geo_vs30_path) as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split('\t')
        geo_vs30.append((lines[i][2], float(lines[i][3])))
    geo_names = []
    for i in range(len(lines)):
        geo_names.append(lines[i][2])
    geo_names_str = ','.join(geo_names)

    # Read in spreadsheet of missing Vs30 values and convert to string. 
    df = pd.read_csv(missing_vs30_path)
    missingvals = df.values
    missing_names = []
    for i in range(len(missingvals)):
        missing_names.append(missingvals[i][0])
    missing_names_str = ','.join(missing_names)

    # Obtain Vs30 values for stations.  
    Vs30 = []
    stn_names = []
    stn_lats = []
    stn_lons = []
    for sta in stations:   
        stn_name = sta[0].stats.station
        lat = sta[0].stats.coordinates['latitude']
        lon = sta[0].stats.coordinates['longitude']
        type_file = '.dat'
        file = stn_name + type_file
        filepath = profile_path + file
    
        # Check to see if kik-profile exists
        if os.path.exists(profile_path + file)==True:
    
            # Read kik profiles
            with open(filepath) as f:
                lines = f.readlines()
    
            # Create arrays of the thickness, depth, and velocity of each layer
            Depth = []
            Velocity = []
            Thickness = []
            x = len(lines)
    
            # Remove files that have missing velocity data.
            if lines[2][30:].replace(' ', '') == '\n':

                # Select Vs30 values from geoVs30 data that match the station names.
                if stn_name in geo_names_str:
                    for data in geo_vs30:
                        if data[0] == stn_name:
                            for i in range(len(sta)):
                                sta[i].stats.vs30 = data[1]
                            Vs30.append(data[1])

                # Add station information to spreadsheet for missing vs30 data.  
                else:
                    Vs30.append(np.nan)
                    if stn_name in missing_names_str:
                        pass
                    else:
                        stn_names.append(stn_name)
                        stn_lats.append(lat)
                        stn_lons.append(lon)

            # Remove files that have 0 velocity data. 
            elif float(lines[2][30:].replace(' ', '')) == 0:

                # Select Vs30 values from geoVs30 data that match the station names.
                if stn_name in geo_names_str:
                    for data in geo_vs30:
                        if data[0] == stn_name:
                            for i in range(len(sta)):
                                sta[i].stats.vs30 = data[1]
                            Vs30.append(data[1])

                # Add station information to spreadsheet for missing vs30 data.  
                else:
                    Vs30.append(np.nan)
                    if stn_name in missing_names_str:
                        pass
                    else:
                        stn_names.append(stn_name)
                        stn_lats.append(lat)
                        stn_lons.append(lon)

            # Calculate Vs30 values
            else:
                for i in range(len(lines)):
                    if i >= 2 and i != (x - 1):
                        thickness = float(lines[i][5:11].replace(' ', ''))
                        depth = float(lines[i][12:20].replace(' ', ''))
                        velocity = float(lines[i][30:].replace(' ', ''))
                        Thickness.append(thickness)
                        Depth.append(depth)
                        Velocity.append(velocity)
    
                if Depth[0] <= 30:
                    time=0
                    for i in range(len(Depth)):
                        if Depth[i] <= 30:
                            part_time = (Thickness[i]) / Velocity[i]
                        elif (Depth[i] > 30 and Depth[i-1] < 30):
                            part_time = (30 - Depth[i-1]) / Velocity[i]
                        else:
                            part_time = 0
                        time = time+part_time
                    vs30 = 30 / time
                    Vs30.append(vs30)
                else: 
                    vs30 = Velocity[0]
                    Vs30.append(vs30)
        else:
            
            # Select Vs30 values from geoVs30 data that match the station names.
            if stn_name in geo_names_str:
                for data in geo_vs30:
                    if data[0] == stn_name:
                        for i in range(len(sta)):
                            sta[i].stats.vs30 = data[1]
                        Vs30.append(data[1])

            # Add station information to spreadsheet for missing vs30 data.
            else:
                    Vs30.append(np.nan)
                    if stn_name in missing_names_str:
                        pass
                    else:
                        stn_names.append(stn_name)
                        stn_lats.append(lat)
                        stn_lons.append(lon)

    missing_data = {'Station': stn_names, 'Station_lat': stn_lats,
                                'Station_lon': stn_lons}
    dfnew = pd.DataFrame(missing_data)
    dfconcat = pd.concat([df, dfnew], sort=True)
    columns = ['Station', 'Station_lat', 'Station_lon']
    
    dfconcat.to_csv(missing_vs30_path, index=False, columns=columns)

    return(Vs30)


def misc(stations):
    """
    Adds station data to a spreadsheet for missing Vs30 data for non KIKnet or
    knet stations.

    Args:
        stations (array): Array of knet stations. 
           
    Returns:
        Vs30 (array): Array of NaN values the size of stations. 

    """

    # Spreadsheet with station names missing Vs30 data
    missing_vs30_path = '/Users/tnye/PROJECTS/Duration/data/Vs30/missing_vs30.csv'

    # Read in spreadsheet of missing Vs30 values and convert to string. 
    df = pd.read_csv(missing_vs30_path)
    missingvals = df.values
    missing_names = []
    for i in range(len(missingvals)):
        missing_names.append(missingvals[i][0])
    missing_names_str = ','.join(missing_names)
    
    # Obtain Vs30 values for stations.
    Vs30 = []
    stn_names = []
    stn_lats = []
    stn_lons = []

    for sta in stations:   
        stn_name = sta[0].stats.station
        lat = sta[0].stats.coordinates['latitude']
        lon = sta[0].stats.coordinates['longitude']

        Vs30.append(np.nan)
        if stn_name in missing_names_str:
            pass
        else:
            stn_names.append(stn_name)
            stn_lats.append(lat)
            stn_lons.append(lon)
                
    missing_data = {'Station': stn_names, 'Station_lat': stn_lats,
                                'Station_lon': stn_lons}
    dfnew = pd.DataFrame(missing_data)
    dfconcat = pd.concat([df, dfnew], sort=True)
    columns = ['Station', 'Station_lat', 'Station_lon']
    
    dfconcat.to_csv(missing_vs30_path, index=False, columns=columns)
                

    return(Vs30)