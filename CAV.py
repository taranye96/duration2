#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 12:34:17 2018

@author: tnye
"""
# Third party imports
import numpy as np
from scipy import integrate


def Heaviside(acc, threshold):
    """Heaviside step function to filter out lower CAV values.

    Args:
        acc (array): Array of acceleration values in cm/s/s.
        threshold (float): Threshold value for acceleration values.

    Returns:
        H_array (array): array of factors to multiply CAV array by.
                    Values are:
                    -1 if CAV is greater than threshold.
                    -0 if CAV is not greater threshold.
    """
    H_array = np.zeros(len(acc))
    H_array[acc > threshold] = 1
    return H_array


def get_CAV(acc, dt, starttime):
    """Calculates cumulative absolute velocity.

    Args:
        acc (array): Array of acceleration values in cm/s/s.
        dt (float): Time between each sample in s.
        starttime (float): Time in s, after record start, to start
            integrating. Usually P-wave arrival time.

    Returns:
        CAV (array): Array of cumulative absolute velocity values with respect
            to time.
        CAV5 (array): Array of cumulative absolute velocity values with a
            threshold of 5 cm/s/s.
        CAVstd (array): Standardized cumulative absolute velocity with a
            threshold of 25 cm/s/s for a 1 second time interval.
    """
    npts = len(acc)
    t = np.linspace(0, (npts-1)*dt, npts)
    t_max = np.max(t)
    heavy = Heaviside(acc, 5.0)

    # Calculate CAV.
    CAV = np.amax(integrate.cumtrapz(np.abs(acc), dx=dt, initial=starttime))

    # Calculate Cumulative Absolute Velocity for values above 5 cm/s/s.
    filt_acc = np.multiply(acc, heavy)
    CAV5 = np.amax(integrate.cumtrapz(np.abs(filt_acc), dx=dt,
                                      initial=starttime))

    # Calculate Standardized Cumualte Absolute Velocity.
    window_size = 1.0
    window_start = np.arange(starttime, t_max, window_size)
    window_end = window_start + window_size
    n_window = len(window_start)
    for i in range(n_window):
        w_ind = np.where((t >= window_start[i]) & (t <= window_end[i]))[0]
        pga_i = np.max(np.abs(acc[w_ind]))
        if pga_i < 25:
            acc[w_ind] = 0.0

    CAVstd = integrate.trapz(abs(acc), dx=dt)

    #print("CAV5:", CAV5)
    #print("CAVstd:", CAVstd)
    #print("CAV", CAV)

    return(CAV, CAV5, CAVstd)
