#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 14:26:52 2018

@author: tnye
"""

# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import pandas as pd

# Local imports 
from pgm.station_summary import StationSummary 
import read_seismic


events = ['usp000a1b0', 'usp000d6vk', 'usp000fg9t', 'usp000g9h6', 'us2000gge9',
          'us1000etmq', 'us2000dwh6','nc30228270', 'nc72282711', 'ci14383980',
          'ci14607652', 'usp0009eq0']
types = ['knt', 'kik', 'smc', 'v2']

imts = ['PGA', 'sa(0.1)', 'sa(0.2)', 'sa(0.3)', 'sa(0.5)', 'sa(1)', 
        'sa(2)', 'sa(3)', 'sa(5)']
imcs = ['rotd50']

pga = []
sa0_1 = []
sa0_2 = []
sa0_3 = []
sa0_5 = []
sa1 = []
sa2 = []
sa3 = []
sa5 = []

for event in events:
    for data_type in types:

        # Determine if the data type exists for the event. 
        filepath = os.path.join('/Users/tnye/PROJECTS/Duration/data/events',
                                event, 'ground_motion', data_type)
        
        if os.path.exists(filepath)==True:
            filt_stns = os.path.join('/Users/tnye/PROJECTS/Duration/data/events',
                                     event, 'select_stations', data_type + '.csv')
        
            # Read data.
            stations, station_stats = read_seismic.get_station_data(event, data_type)

            # Calculate imts. 
            for station in stations:
                data = StationSummary.from_stream(station, imcs, imts).pgms
                pga.append(data['PGA']['ROTD50.0'])
                sa0_1.append(data['SA(0.1)']['ROTD50.0'])
                sa0_2.append(data['SA(0.2)']['ROTD50.0'])
                sa0_3.append(data['SA(0.3)']['ROTD50.0'])
                sa0_5.append(data['SA(0.5)']['ROTD50.0'])
                sa1.append(data['SA(1)']['ROTD50.0'])
                sa2.append(data['SA(2)']['ROTD50.0'])
                sa3.append(data['SA(3)']['ROTD50.0'])
                sa5.append(data['SA(5)']['ROTD50.0'])

# Create a dictionary of the imts. 
data_dic = {'SA(0.1)_rotd50': sa0_1, 'SA(0.2)_rotd50': sa0_2, 'SA(0.3)_rotd50': sa0_3, 
            'SA(0.5)_rotd50': sa0_5, 'SA(1)_rotd50': sa1, 'SA(2)_rotd50': sa2,
            'SA(3)_rotd50': sa3, 'SA(5)_rotd50': sa5}

# Turn dictionary into a data frame. 
df_spec = pd.DataFrame(data_dic, columns = ['SA(0.1)_rotd50', 'SA(0.2)_rotd50',
                                            'SA(0.3)_rotd50', 'SA(0.5)_rotd50',
                                            'SA(1)_rotd50', 'SA(2)_rotd50',
                                            'SA(3)_rotd50', 'SA(5)_rotd50'])

df_spec.to_csv('/Users/tnye/PROJECTS/Duration/data/rotd50.csv', index=False)
