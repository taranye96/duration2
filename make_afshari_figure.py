#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:51:54 2018

@author: tnye
"""

import numpy as np
from obspy.core.stream import Stream

import processing
import arias_intensity
import matplotlib.pyplot as plt


def main():

    # Read acceleration data. If you want velocity units='vel',
    # Cdisplacement units='disp'
    files = ['1994.c.017m30su.n0a',
             '1994.c.017m30su.n0b',
             '1994.c.017m30su.n0c']

    stream = Stream()

    # Data for the trace we are working with
    # There are 3 traces (0, 1,  2), and i denotes trace we are working with
    for i in range(len(files)):
        cmp = processing.read_data(files[i], units='acc')[0]
        stream.append(cmp)

    durations = [(0.05, 0.75),
                 (0.2, 0.8),
                 (0.05, .95)]

    # Plots each boundary on the Norm Arias Intensity graph
    # plt.figure(figsize=(6.5, 2.5))
    f, axes = plt.subplots(len(durations), 1, sharex=True, 
                           figsize=(6.5, 7.5))

    for i, trace in enumerate(stream):
        trace_stats = trace.stats
        channel = trace.stats['channel']
        dt = trace_stats.delta
        Ia, NIa = arias_intensity.get_arias_intensity(trace.data, dt)
        print("Arias Intensity (%s): %f" % (channel, np.amax(Ia)))
        if i == 2:
            xlab = True
        else:
            xlab = False
        arias_intensity.plot_durations_on_NIa(NIa, dt, durations, 
                                              axes[i], xlab)
        axes[i].set_title(channel)

    plt.savefig('Ashfari_Fig_1_tnye.png', dpi=300)


if __name__ == "__main__":
    main()
