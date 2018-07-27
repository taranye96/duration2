#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 11:08:18 2018

@author: tnye
"""
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')
import pandas as pd
from dateutil import parser
import read_seismic

filepath = ('/Users/tnye/PROJECTS/Duration/data/small_quake/knt')
filt_stns = ('/Users/tnye/PROJECTS/Duration/data/small_quake/knt.csv')

stations, station_stats = read_seismic.get_knt_data(filepath, filt_stns)

picktimes = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/small_quake/picktimes.csv')
pickvals = picktimes.values
picklist = []
for x in pickvals:
    for y in x:
        picklist.append(y)

