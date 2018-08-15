#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 15:59:16 2018

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
          'us1000etmq', 'us2000dwh6', 'nc30228270', 'nc72282711', 'ci14383980',
          'ci14607652', 'usp0009eq0']
types = ['knt', 'kik', 'smc', 'v2']

imts = ['PGA', 'sa(0.1)', 'sa(0.2)', 'sa(0.3)', 'sa(0.5)', 'sa(1)', 
        'sa(2)', 'sa(3)', 'sa(5)']
imcs = ['channels']

sa0_1_hn1 = []
sa0_1_hn2 = []
sa0_2_hn1 = []
sa0_2_hn2 = []
sa0_3_hn1 = []
sa0_3_hn2 = []
sa0_5_hn1 = []
sa0_5_hn2 = []
sa1_hn1 = []
sa1_hn2 = []
sa2_hn1 = []
sa2_hn2 = []
sa3_hn1 = []
sa3_hn2 = []
sa5_hn1 = []
sa5_hn2 = []

for event in events:
    for data_type in types:

        # Determine if data type exists for event. 
        filepath = os.path.join('/Users/tnye/PROJECTS/Duration/data/events',
                                event, 'ground_motion', data_type)
        
        if os.path.exists(filepath)==True:
            filt_stns = os.path.join('/Users/tnye/PROJECTS/Duration/data/events',
                                     event, 'select_stations', data_type + '.csv')
        
            # Read data.
            stations, station_stats = read_seismic.get_station_data(event, data_type)
        
            for station in stations:
                
                # Calculate imts. 
                data = StationSummary.from_stream(station, imcs, imts).pgms
                if 'HN1' in data['PGA']:
                    h1 = 'HN1'
                    h2 = 'HN2'
                elif 'BN1' in data['PGA']:
                    h1 = 'BN1'
                    h2 = 'BN2'

                sa0_1_hn1.append(data['SA(0.1)'][h1])
                sa0_2_hn1.append(data['SA(0.2)'][h1])
                sa0_3_hn1.append(data['SA(0.3)'][h1])
                sa0_5_hn1.append(data['SA(0.5)'][h1])
                sa1_hn1.append(data['SA(1)'][h1])
                sa2_hn1.append(data['SA(2)'][h1])
                sa3_hn1.append(data['SA(3)'][h1])
                sa5_hn1.append(data['SA(5)'][h1])
                sa0_1_hn2.append(data['SA(0.1)'][h2])
                sa0_2_hn2.append(data['SA(0.2)'][h2])
                sa0_3_hn2.append(data['SA(0.3)'][h2])
                sa0_5_hn2.append(data['SA(0.5)'][h2])
                sa1_hn2.append(data['SA(1)'][h2])
                sa2_hn2.append(data['SA(2)'][h2])
                sa3_hn2.append(data['SA(3)'][h2])
                sa5_hn2.append(data['SA(5)'][h2])

# Read in data frame. 
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/partial_spec.csv')

# Create a dictionary of the imts. 
data_dic = {'SA(0.1)_HN1': sa0_1_hn1, 'SA(0.1)_HN2': sa0_1_hn2, 'SA(0.2)_HN1': sa0_2_hn1,
            'SA(0.2)_HN2': sa0_2_hn2, 'SA(0.3)_HN1': sa0_3_hn1, 'SA(0.3)_HN2': sa0_3_hn2,
            'SA(0.5)_HN1': sa0_5_hn1, 'SA(0.5)_HN2': sa0_5_hn2, 'SA(1)_HN1': sa1_hn1,
            'SA(1)_HN2': sa1_hn2, 'SA(2)_HN1': sa2_hn1, 'SA(2)_HN2': sa2_hn2,
            'SA(3)_HN1': sa3_hn1, 'SA(3)_HN2': sa3_hn2, 'SA(5)_HN1': sa5_hn1,
            'SA(5)_HN2': sa5_hn2}

# Turn dictionary into a data frame. 
df_spec = pd.DataFrame(data_dic, columns = ['SA(0.1)_HN1', 'SA(0.1)_HN2', 'SA(0.2)_HN1',
                                        'SA(0.2)_HN2', 'SA(0.3)_HN1', 'SA(0.3)_HN2',
                                        'SA(0.5)_HN1', 'SA(0.5)_HN2', 'SA(1)_HN1',
                                        'SA(1)_HN2', 'SA(2)_HN1', 'SA(2)_HN2',
                                        'SA(3)_HN1', 'SA(3)_HN2', 'SA(5)_HN1',
                                        'SA(5)_HN2'])

df_spec.to_csv('/Users/tnye/PROJECTS/Duration/data/specs.csv', index=False)
