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
        threshold (float): Threshold value for acceleration.

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
            threshold of 25 cm/s/s for discrete 1-second time intervals.
    """

    # Create an array of acceleration times. 
    npts = len(acc)
    t = np.linspace(0, (npts-1)*dt, npts)
    t_max = np.max(t)

    # Create a separate acceleration array so that the original acceleration
    # array does not get zeroed out during CAV5 and CAVstd calculations. 
    acctemp = np.array(acc)

    # Choose acceleration values starting at the specificed starttime.
    acc2 = acctemp[t >= starttime]

    # Multiply by heaviside funciton to filter out lower CAV.
    heavy = Heaviside(acc2, 5.0)
    
    # Calculate CAV.
    CAV = np.amax(integrate.cumtrapz(np.abs(acc2), dx=dt))

    # Calculate CAV5.
    filt_acc = np.multiply(acc2, heavy)
    CAV5 = np.amax(integrate.cumtrapz(np.abs(filt_acc), dx=dt))

    # Calculate CAVstd.
    window_size = 1.0
    window_start = np.arange(0, t_max, window_size)
    window_end = window_start + window_size
    n_window = len(window_start)
    for i in range(n_window):
        w_ind = np.where((t >= window_start[i]) & (t <= window_end[i]))[0]
        pga_i = np.max(np.abs(acc2[w_ind]))
        if pga_i < 25:
            acc2[w_ind] = 0.0

    CAVstd = integrate.trapz(abs(acc2), dx=dt)

    return(CAV, CAV5, CAVstd)
