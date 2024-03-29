#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:51:54 2018

@author: tnye
"""

# Standard library imports
import os

# Third party imports
import numpy as np
from obspy.core.stream import Stream
import matplotlib.pyplot as plt

# Local imports
import processing
import arias_intensity


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

    durations = [(0.05, 0.75),
                 (0.2, 0.8),
                 (0.05, .95)]

    # Plots each boundary on the Norm Arias Intensity graph
    f, axes = plt.subplots(len(durations), 1, sharex=True,
                           figsize=(6.5, 7.5))

    for i, trace in enumerate(stream):

        # Convert acceleration to m/s/s
        acc = np.multiply(0.01, trace.data)

        channel = trace.stats['channel']
        dt = trace.stats.delta

        Ia, NIa = arias_intensity.get_arias_intensity(acc, dt, 0)
        print("Arias Intensity (%s): %f" % (channel, np.amax(Ia)))

        if i == 2:
            xlab = True
        else:
            xlab = False

        arias_intensity.plot_durations(NIa, dt, durations, axes[i], xlab)
        axes[i].set_title(channel)

    plt.savefig('/Users/tnye/PROJECTS/Duration/figures/Afshari_Fig_1_tnye.png',
                dpi=300)


if __name__ == "__main__":
    main()
