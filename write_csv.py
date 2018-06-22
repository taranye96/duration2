#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 09:48:26 2018

@author: tnye
"""

import csv

csvData = [['USGS_eventID', 'magnitude', 'source_lat', 'source_lon',
            'depth(km)', 'station_name', 'station_lat', 'station_lon', 'elev',
            'rdist(km)', 'rake_angle', 'fault_type', 'Ia', 'CAV', 'CAV5',
            'CAVstd', 'Vs30', 'PGA', 'PGV']]

with open('earthquake_data.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)

csvFile.close
