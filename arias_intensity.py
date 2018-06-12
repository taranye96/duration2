#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:15:25 2018

@author: tnye
"""
# third party
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt


def get_arias_intensity(acc, dt):
    """
    Determines Arias Intensity and plots it and its normalized values
    on graphs.

    Args:
        acc (array): array of acceleration values.
        dt (array): time between each sample (s).

    Returns:
        tuple: arrays of time, Arias Intensity, and normalized Arias
        intensity.
    """

    # Arias Intensity
    g = 980
    Int = integrate.cumtrapz(acc*acc, dx=dt)
    Ia = Int * np.pi/(2*g)

    # Normalized Arias Intensity
    # dividing arias intensity by max value
    NIa = Ia/np.amax(Ia)
    return(Ia, NIa)


def get_time_from_percent(NIa, p, dt):
    """
    Get time associated with percent of Arias Intensity.

    Args:
        p (float): Percent (0 to 1) of Arias Intensity.

    Returns:
        time(float): Time at which p occurs.
    """

    npts = len(NIa)
    t = np.linspace(0, npts*dt, num=npts)

    time = t[np.argmin(np.abs(p-NIa))]
    return(time)


def get_time_for_duration_parameters(NIa, dt, p1, p2):
    """
    Find cloest values to the desired %Arias intensity range and calc total
    time for the range.

    Args:
        p1
        p2

    Returns:
        dur_time(float): Time duration for paramteters.
    """
    t1 = get_time_from_percent(NIa, p1, dt)
    t2 = get_time_from_percent(NIa, p2, dt)

    dur_time = t2 - t1
    return(dur_time)


def plot_arias_intensity(Ia, NIa, dt):
    """
    Plots Arias intensity and normalized arias intensity

    Args:
        Ia (array): cumulative integral for Arias intensity
        NIa (array):cumulative integral for normalized Arias intensity
        dt (float):
    Returns:
        Nothing....?
    """

    npts = len(NIa)
    t = np.linspace(0, npts*dt, num=npts)

    # Plot Arias Intensity
    plt.plot(t, Ia, 'k-')
    plt.xlim(0, 30)
    plt.xlabel('Time (s)')
    plt.ylabel('Arias Intensity (m/s)')
    plt.savefig('Arias_Intensity.png')

    # Plot Normalized Arias Intensity
    plt.figure(figsize=(6.5, 2.5))
    plt.plot(t, NIa, 'b-')
    plt.xlim(0, 30)
    plt.ylim(0, 1)
    plt.xlabel('Time (s)')
    plt.ylabel('Norm Arias Intensity (m/s)')
    plt.show()
    plt.savefig('Norm_Arias_Intensity.png')
    return()


def plot_durations_on_NIa(NIa, dt, durations, ax, xlab=True):
    """
    Plots duration on normalized Arias intensity graph

    Args:
    Returns:
    """

    npts = len(NIa)
    t = np.linspace(0, npts*dt, num=npts)
    xmax = max(t)
    ax.plot(t, NIa, 'k-')
    if xlab:
        ax.set_xlabel('Time (s)')
    ax.set_ylabel('Norm Arias Intensity (m/s)')

    for i in range(len(durations)):
        p1 = durations[i][0]
        p2 = durations[i][1]
        t1 = get_time_from_percent(NIa, p1, dt)
        t2 = get_time_from_percent(NIa, p2, dt)
        height = (1/4 * i) + 1/4
        ax.plot(t1, p1, 'ok')
        ax.plot(t2, p2, 'ok')
        ax.annotate('', xy=(t2, height), xytext=(t1, height),
                    arrowprops=dict(arrowstyle='<->'))
        # plt.text(xmax-10, height, '$D_{5-75}=7.1s$', style='italic')
        # plt.text(xmax-10, height, '$D_{5-95}=18.4s$', style='italic')
        # plt.text(xmax-10, height, durations[i], style='italic')
        label = '$D_{%i{-}%i}$' % (100 * durations[i][0],
                                   100 * durations[i][1])
        ax.text(t2, height, label, style='italic',
                horizontalalignment='left',
                verticalalignment='center')