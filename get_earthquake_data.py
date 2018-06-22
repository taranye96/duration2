#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 10:00:27 2018

@author: tnye
"""
import pandas as pd
import csv


####################### Attempt 1
df = pd.DataFrame(columns = ['USGS_eventID', 'station_name', 'station_coords',
                            'event_coords', 'magnitude', 'depth',
                            'd_from_fault', 'rake_angle', 'fault_type',
                            'Ia', 'CAV', 'CAV5', 'CAVstd', 'Vs30', 'PGA', 'PGV'
                            ]
                  )



###################### Attempt 2
dic = {}

download_dir = "earthquake_data.csv"

csv = open(dowload_dir, "w")

columnTitleRow = "station_name, station_coords, USGS_eventID, event coords,
                    rdist, magnitude, depth, rake_angle, fault_type, Ia, CAV,
                    CAV5, CAVstd, Vs30, PGA, PGV"
csv.write(columnTitleRow)

for key in dic.keys():
    station_name = key
    station_coords
    ........
    row = station_name + "," + ...........
    csv.write(row)




###################### Attempt 3
csvData = [['station_name,' 'station_coords', 'USGS_eventID', 'event coords',
            'rdist', 'magnitude', 'depth', 'rake_angle', 'fault_type',
            'Ia', 'CAV', 'CAV5', 'CAVstd', 'Vs30', 'PGA', 'PGV']]

with open('earthquake_data.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)

csvFile.close
