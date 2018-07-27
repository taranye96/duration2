#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 16:04:46 2018

@author: tnye
"""

import pandas as pd
from collections import OrderedDict

data = OrderedDict([('Station', []), ('Coordinates', [])])

df = pd.DataFrame(data)

df.to_csv('Vs30_geo.csv', index=False)