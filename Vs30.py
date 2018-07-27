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


def knet_Vs30(stations, knet_Vs30, vs30_path):
    """
    Obtains Vs30 values from a spreadsheet for a list of knet stations.
    Stations not listed in the spreadsheet are put into a list. 

    Args:
        filepath (str): Absolute filepath to the earthquake data.
        knet_Vs30 (csv): Csv of Vs30 values (extrapolated from California) for
            a list of knet stations. 
        vs30_path (str): Absolute path to list of vs30 values from geology.
           
    Returns:
        Vs30 (array): Array of Vs30 values for the knet stations. 

    """

    # Read in spreadsheet with Vs30 values and convert station names to string.
    data = pd.read_csv(knet_Vs30, usecols=(['X', 'Y']), sep=",")
    datavals = data.values
    names = []
    for i in range(len(datavals)):
        names.append(datavals[i][0])
    names_str = ','.join(names)

    geo_vs30 = []
    with open(vs30_path) as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split('\t')
        geo_vs30.append((lines[i][2], float(lines[i][3])))
    
    Vs30 = []
    special_files = []
    for station in stations:   
        stn_name = station[0].stats.station
        lat = station[0].stats.knet.stla
        lon = station[0].stats.knet.stlo

        # Remove files that are not in spreadsheet.
        if stn_name in names_str:

            # Select Vs30 values from spreadsheet that match the station names.
            for i in range(len(datavals)):
                if datavals[i][0] == stn_name:
                    Vs30.append(datavals[i][1])
        else:
#            special_files.append((stn_name, lat, lon))
#            Vs30.append('Nan')
            for i in range(len(geo_vs30)):
                    if geo_vs30[i][0] == stn_name:
                        Vs30.append(geo_vs30[i][1])

    return(Vs30, special_files)


def kik_Vs30(stations, profile_path, vs30_path):
    """
    Calculates Vs30 values for a list Kik-net stations.  Stations without a
    profile or with unusable data are put into a list. 
    
    Args:
        station (stream): Stream of Kik-net stations.
        profile_path (str): Absolute path to Kik-net profiles.
        vs30_path (str): Absolute path to list of vs30 values from geology.
    Returns:
        Vs30 (float): Average velocity for the top 30 m. 
        special_files (stream): Stream of stations that do not have a kik
            profile or have unusable data.

    """
        
    geo_vs30 = []
    with open(vs30_path) as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split('\t')
        geo_vs30.append((lines[i][2], float(lines[i][3])))
         
    
    special_files = []
    Vs30 = []
    for station in stations:   
        stn_name = station[0].stats.station
        lat = station[0].stats.knet.stla
        lon = station[0].stats.knet.stlo
        type_file = '.dat'
        file = stn_name + type_file
        filepath = profile_path + file
    
        # Check to see kik-profile exists
        if os.path.exists(profile_path + file)==True:
    
            # Read kik profiles
            with open(filepath) as f:
                lines = f.readlines()
    
            # Create arrays of the thickness, depth, and velocity of each layer
            Depth = []
            Velocity = []
            Thickness = []
            x = len(lines)
    
            # Remove files that have missing or 0 velocity data
            if lines[2][30:].replace(' ', '') == '\n':
    #                special_files.append((stn_name, lat, lon))
    #                Vs30.append('Nan')
                for i in range(len(geo_vs30)):
                    if geo_vs30[i][0] == stn_name:
                        Vs30.append(geo_vs30[i][1])
            elif float(lines[2][30:].replace(' ', '')) == 0:
    #                special_files.append((stn_name, lat, lon))
    #                Vs30.append('Nan')
                for i in range(len(geo_vs30)):
                    if geo_vs30[i][0] == stn_name:
                        Vs30.append(geo_vs30[i][1])
            else:
                for i in range(len(lines)):
                    if i >= 2 and i != (x - 1):
                        thickness = float(lines[i][5:11].replace(' ', ''))
                        depth = float(lines[i][12:20].replace(' ', ''))
                        velocity = float(lines[i][30:].replace(' ', ''))
                        Thickness.append(thickness)
                        Depth.append(depth)
                        Velocity.append(velocity)
    
                # Calculate Vs30
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
    #            special_files.append((stn_name, lat, lon))
    #            Vs30.append('Nan')
            for i in range(len(geo_vs30)):
                    if geo_vs30[i][0] == stn_name:
                        Vs30.append(geo_vs30[i][1])

    return(Vs30, special_files)
