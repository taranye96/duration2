#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 16:36:52 2018

@author: tnye
"""

import numpy as np
import arias_intensity
import CAV
from amptools.io.dmg.core import read_dmg

stream1 = read_dmg('/Users/tnye/PROJECTS/Duration/data/loma_prieta/GILROY1.V2')
stream2 = read_dmg('/Users/tnye/PROJECTS/Duration/data/loma_prieta/GILROY2.V2')

#print("Arias Gilroy 1")
#for trace in stream1:
#    acc = np.multiply(0.01, trace.data)
#    channel = trace.stats.channel
#    Ia, NIa = arias_intensity.get_arias_intensity(acc, trace.stats['delta'])
#    print(channel, np.amax(Ia))
#
#print("Arias Gilroy 2")
#for trace in stream2: 
#    acc = np.multiply(0.01, trace.data)
#    channel = trace.stats.channel
#    Ia, NIa = arias_intensity.get_arias_intensity(acc, trace.stats['delta'])
#    print(channel, np.amax(Ia))

print("CAV Gilroy 1")
for trace in stream1:
    channel = trace.stats.channel
    cav, cav5, cavstd = CAV.get_CAV(trace.data, trace.stats['delta'])
    print(channel, cav)
