#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 15:09:28 2018

@author: tnye
"""

import pandas as pd
from collections import OrderedDict

data = OrderedDict([('USGS_eventID', []), ('magnitude', []), ('depth(km)', []),
                    ('source_lat', []), ('source_lon', []),
                    ('station_name', []), ('elev(m)', []), ('station_lat', []),
                    ('station_lon', []), ('rdist(km)', []), ('rake_angle', []),
                    ('fault_type', []), ('Ia', []), ('CAV', []), ('CAV5', []),
                    ('CAVstd', []), ('Vs30', []), ('PGA', []), ('PGV', [])])

df = pd.DataFrame(data)

df.to_csv('duration_data.csv', index=False)
