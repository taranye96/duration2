#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 12:34:17 2018

@author: tnye
"""

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt


def Heaviside(acc, threshold=0.0):
    """Heaviside step function to filt out lower CAV.

    Args:
        acc (array): Array of acceleration values.
        threshold (float): Threshold value for acceleration values.

    Returns:
        H_array (array): array of factors to multiply CAV by
                    -1 if CAV is greater than 5 m/s
                    -0 if CAV is not greater than 5 m/s
    """
    H_array = np.zeros(len(acc))
    H_array[acc > threshold] = 1
    return H_array


def get_CAV(acc, dt):
    """Determines cumulative absolute velocity.

    Args:
        acc (array): Array of acceleration values.
        dt (float): time between each sample (s).

    Returns:
        CAV (array): Integral of abs value of acceleration with respect
            to time.
        CAV5 (array): CAV with a threshold of 5 cm/c^2.
        CAVstd (array): Standardized CAV with a threshold of 2.5 cm/s^2.
    """
    npts = len(acc)
    t = np.linspace(0, (npts-1)*dt, npts)
    t_max = np.max(t)
    heavy = Heaviside(acc, 5.0)

    # Calculate Cumulative Absolute Velocity
    CAV = integrate.trapz(np.abs(acc), dx=dt)

    # Calculate Cumulative Absolute Velocity for values above 5 cm/s^2
    filt_acc = np.multiply(acc, heavy)
    CAV5 = integrate.trapz(np.abs(filt_acc), dx=dt)

    # Calculate Standard Cumualte Absolute Velocity
    window_size = 1.0
    window_start = np.arange(0, t_max, window_size)
    window_end = window_start + window_size
    n_window = len(window_start)
    for i in range(n_window):
        w_ind = np.where((t >= window_start[i]) & (t <= window_end[i]))[0]
        pga_i = np.max(np.abs(acc[w_ind]))
        if pga_i < 2.5:
            print('window %i is zero-ed out' %i)
            acc[w_ind] = 0.0

    CAVstd = integrate.trapz(abs(acc), dx=dt)

    print("CAV5:", CAV5)
    print("CAVstd:", CAVstd)
    print("CAV", CAV)

    return(CAV, CAV5, CAVstd)


def plot_CAV(type_CAV, dt):
    """
    Plots cumulative absolute velocity with respect to time.

    Args:
        type_CAV (array): CAV based on specified threshold.  Options are:
            "CAV"
            "CAV5"
            "CAVstd"

    Returns:
        Just the plot
    """

    npts = len(CAV)
    t = np.linspace(0, (npts-1)*dt, num=npts)

    plt.plot(t, CAV, 'k-')
    plt.xlabel('Time (s)')
    plt.ylabel('CAV')
    plt.show()
    # plt.savefig('Arias_Intensity.png')
    return()
