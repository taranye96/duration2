#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 13:13:56 2018

@author: tnye
"""
import os
from obspy.core.stream import Stream

import processing
import CAV


def main():

    # Read acceleration data. If you want velocity units='vel',
    # Cdisplacement units='disp'
    data_dir = '/Users/tnye/PROJECTS/Duration/data'
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
        cav, cav5, cavstd  = CAV.get_CAV(trace.data, dt)

        # print("CAV (%s): %f" % (channel, np.amax(CAV)))

        # calc_CAV.plot_CAV(type_CAV, dt)

    # plt.savefig('CAV_tnye.png', dpi=300)


if __name__ == "__main__":
    main()
