#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 15:09:28 2018

@author: tnye
"""

# Third party imports
import pandas as pd
from collections import OrderedDict

data = OrderedDict([('USGS_eventID', []), ('magnitude', []), ('depth(km)', []),
                    ('rake_angle', []), ('source_lat', []), ('source_lon', []),
                    ('station_name', []), ('station_type', []),
                    ('station_lat', []), ('station_lon', []),
                    ('ep_dist(km)', []), ('fault_dist(km)', []),
                    ('Vs30(m/s)', []), ('PGA_arith(cm/s/s)', []),
                    ('PGA_max(cm/s/s)', []), ('Ia_arith(m/s)', []),
                    ('Ia_geom(m/s)', []), ('Ia_max(m/s)', []),
                    ('CAV_arith(cm/s)', []), ('CAV_geom(cm/s)', []),
                    ('CAV_max(cm/s)', []), ('CAV5_arith(cm/s)', []),
                    ('CAV5_geom(cm/s)', []), ('CAV5_max(cm/s)', []),
                    ('CAVstd_arith(cm/s)', []), ('CAVstd_geom(cm/s)', []),
                    ('CAVstd_max(cm/s)', [])])

df = pd.DataFrame(data)

filepath = '/Users/tnye/PROJECTS/Duration/data/initial_df.csv'
df.to_csv(filepath, index=False)
