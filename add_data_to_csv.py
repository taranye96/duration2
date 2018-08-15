#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 14:05:13 2018

@author: tnye
"""

# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import pandas as pd

# Local imports
import read_seismic
import calc_eq_data
import pga
import rot_components
import Vs30


# List of events
events = ['usp000a1b0', 'usp000d6vk', 'usp000fg9t', 'usp000g9h6', 'us2000gge9',
          'us1000etmq', 'us2000dwh6','nc30228270', 'nc72282711', 'ci14383980',
          'ci14607652', 'usp0009eq0']
# List of types of files
data_types = ['knt', 'kik', 'smc', 'v2']


# Obtain values for data frame.
for event in events:
    for data_type in data_types:

        # Search to see if the data type exists.
        folderpath = os.path.join('/Users/tnye/PROJECTS/Duration/data/events',
                                  event, 'ground_motion', data_type)
        if os.path.exists(folderpath)==True:
        
            # Read seismic data.
            stations, station_stats = read_seismic.get_station_data(event,
                                                                    data_type)
    
            # Get event data.
            event_id, date, mag, source_lat, source_lon, depth, rake =\
                calc_eq_data.get_earthquake_data(event, stations)
    
            # Add distance and P_wave arrival times to stats
            calc_eq_data.get_dist_and_parrivals(stations, depth)
    
            # Get all other values. 
            event_ids = []
            mags = []
            depths = []
            rake_angles = []
            source_lats = []
            source_lons = []
    
            station_names = []
            station_types = []
            station_lats = []
            station_lons = []
            distances = []
            PGA_arith = []
            PGA_max = []
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
    
    
            for sta in stations:
                event_id = sta[0].stats['eventID']
                mag = sta[0].stats['mag']
                depth = sta[0].stats['source_depth']
                rake = sta[0].stats['rake']
                source_lat = sta[0].stats['source_lat']
                source_lon = sta[0].stats['source_lon']
                station_name = sta[0].stats['station']
                station_type = data_type
                station_lat = sta[0].stats.coordinates['latitude']
                station_lon = sta[0].stats.coordinates['longitude']
                distance = sta[0].stats['distkm']
                event_ids.append(event_id)
                mags.append(mag)
                depths.append(depth)
                rake_angles.append(rake)
                source_lats.append(source_lat)
                source_lons.append(source_lon)
                station_names.append(station_name)
                station_types.append(station_type)
                station_lats.append(station_lat)
                station_lons.append(station_lon)
                distances.append(distance)
        
                # PGA
                pga_arith, pga_max = pga.get_horizontal_pga(sta[0].data,
                                                            sta[2].data)
                PGA_arith.append(pga_arith)
                PGA_max.append(pga_max)
    
                # Rotation-independent components
                dt = sta[0].stats.delta
                ia_geom, ia_arith, ia_max = rot_components.get_RotComp_Arias(sta, dt, 0)
                Ia_geom.append(ia_geom)
                Ia_arith.append(ia_arith)
                Ia_max.append(ia_max)
    
                (cav_geom, cav5_geom, cavstd_geom,
                 cav_arith, cav5_arith, cavstd_arith,
                 cav_max, cav5_max,
                 cavstd_max) = rot_components.get_RotComp_CAV(sta, dt, 0)
                CAV_geom.append(cav_geom)
                CAV5_geom.append(cav5_geom)
                CAVstd_geom.append(cavstd_geom)
                CAV_arith.append(cav_arith)
                CAV5_arith.append(cav5_arith)
                CAVstd_arith.append(cavstd_arith)
                CAV_max.append(cav_max)
                CAV5_max.append(cav5_max)
                CAVstd_max.append(cavstd_max)
    
    
            # Vs30
            if data_type == 'knt':
                vs30 = Vs30.knet_Vs30(stations)
            elif data_type == 'kik':
                vs30 = Vs30.kik_Vs30(stations)
            else:
                vs30 = Vs30.misc(stations)
    
    
            # Add data to spreadsheet
            data = {'USGS_eventID': event_ids, 'magnitude': mags, 'depth(km)': depths,
                    'rake_angle': rake_angles, 'source_lat': source_lats,
                    'source_lon': source_lons, 'station_name': station_names,
                    'station_type': station_types, 'station_lat': station_lats,
                    'station_lon': station_lons, 'ep_dist(km)': distances,
                    'Vs30(m/s)': vs30, 'PGA_arith(cm/s/s)': PGA_arith,
                    'PGA_max(cm/s/s)': PGA_max, 'Ia_geom(m/s)': Ia_geom,
                    'Ia_arith(m/s)': Ia_arith, 'Ia_max(m/s)': Ia_max,
                    'CAV_geom(cm/s)': CAV_geom, 'CAV_arith(cm/s)': CAV_arith,
                    'CAV_max(cm/s)': CAV_max, 'CAV5_geom(cm/s)': CAV5_geom,
                    'CAV5_arith(cm/s)': CAV5_arith, 'CAV5_max(cm/s)': CAV5_max,
                    'CAVstd_geom(cm/s)': CAVstd_geom,
                    'CAVstd_arith(cm/s)': CAVstd_arith,
                    'CAVstd_max(cm/s)': CAVstd_max}
    
            filename1 = '/Users/tnye/PROJECTS/Duration/data/initial_df.csv'
            filename2 = '/Users/tnye/PROJECTS/Duration/data/duration_data.csv'
            df = pd.read_csv(filename1)
    
            dfnew = pd.DataFrame(data)
            dfconcat = pd.concat([df, dfnew], sort=True)
            
            columns = ['USGS_eventID', 'magnitude', 'depth(km)', 'rake_angle',
                       'source_lat', 'source_lon', 'station_name', 'station_type',
                       'station_lat', 'station_lon', 'ep_dist(km)', 'fault_dist(km)',
                       'Vs30(m/s)', 'PGA_arith(cm/s/s)', 'PGA_max(cm/s/s)',
                       'Ia_geom(m/s)', 'Ia_arith(m/s)', 'Ia_max(m/s)',
                       'CAV_geom(cm/s)', 'CAV_arith(cm/s)', 'CAV_max(cm/s)',
                       'CAV5_geom(cm/s)', 'CAV5_arith(cm/s)', 'CAV5_max(cm/s)',
                       'CAVstd_geom(cm/s)', 'CAVstd_arith(cm/s)',
                       'CAVstd_max(cm/s)']
            
            dfconcat.to_csv(filename2, index=False, columns=columns)
