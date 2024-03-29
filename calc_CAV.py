#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 13:13:56 2018

@author: tnye
"""
# Standard library imports
import os

# Third party imports
from obspy.core.stream import Stream

# Local imports
import processing
import CAV


def main():

    # Read acceleration data. If you want velocity units='vel',
    # Cdisplacement units='disp'
    data_dir = '/Users/tnye/PROJECTS/Duration/data/ci3144585/ground_motion'
    files = ['1994.c.017m30su.n0a',
             '1994.c.017m30su.n0b',
             '1994.c.017m30su.n0c']
    files = [os.path.join(data_dir, f) for f in files]

    stream = Stream()

    # Data for the trace we are working with
    # There are 3 traces (0, 1,  2), and i denotes trace we are working with
    for i in range(len(files)):
        cmp = processing.read_data(files[i], units='acc')[0]
        stream.append(cmp)

    for i, trace in enumerate(stream):
        trace_stats = trace.stats
        channel = trace.stats['channel']
        print(channel)
        dt = trace_stats.delta
        cav = CAV.get_CAV(trace.data, dt, 0)

if __name__ == "__main__":
    main()
