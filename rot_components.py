#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 16:49:13 2018

@author: tnye
"""

import math 
import numpy as np
# Local imports
import arias_intensity
import CAV


def get_RotComp_Arias(station, dt, starttime):
    """
    Calculates the rotational independent components of Ia and CAV: geometric
    mean, arithmetic mean, and max of two horizontal components.

    Args:
        station
        dt

    Returns:
        Ia_geom
        Ia_arith
        Ia_max
    """

    # Calculate Arias intensity
    for i in range(len(station)):
        trace = station[i]
        Ia, NIa = arias_intensity.get_arias_intensity(np.multiply(trace.data, 0.01),
                                                      trace.stats.delta,
                                                      starttime)
        trace.stats.Ia = np.amax(Ia)

    # Calculate geometric mean
    Ia_geom = (math.sqrt(station[0].stats['Ia'] *
                         station[2].stats['Ia']))

    # Calculate arithmetic mean
    Ia_arith = ((station[0].stats['Ia'] +
                 station[2].stats['Ia']) / 2)

    # Calculate max horizontal component 
    for i in range(len(station)):
        if station[0].stats.Ia > station[2].stats.Ia:
            Ia_max = station[0].stats.Ia
        else:
            Ia_max = station[2].stats.Ia

    return(Ia_geom, Ia_arith, Ia_max)


def get_RotComp_CAV(station, dt, starttime):
    """
    Calculates the rotational independent components of CAV: geometric
    mean, arithmetic mean, and max of two horizontal components.

    Args:
        station
        dt

    Returns:
        CAV_geom
        CAV5_geom
        CAVstd_geom
        CAV_arith
        CAV5_arith
        CAVstd_arith
        CAV_max
        CAV5_max
        CAVstd_max
    """

    # Calculate CAV
    for i in range(len(station)):
        trace = station[i]
        cav, cav5, cavstd = CAV.get_CAV(trace.data, trace.stats.delta,
                                        starttime)
        trace.stats.CAV = np.amax(cav)
        trace.stats.CAV5 = np.amax(cav5)
        trace.stats.CAVstd = np.amax(cavstd)
    
    # Calculate geometric mean
    CAV_geom = (math.sqrt(station[0].stats['CAV'] *
                          station[2].stats['CAV']))
    CAV5_geom = (math.sqrt(station[0].stats['CAV5'] *
                           station[2].stats['CAV5']))
    CAVstd_geom = (math.sqrt(station[0].stats['CAVstd'] *
                             station[2].stats['CAVstd']))

    # Calculate arithmetic mean
    CAV_arith = ((station[0].stats['CAV'] +
                  station[2].stats['CAV']) / 2)
    CAV5_arith = ((station[0].stats['CAV5'] +
                   station[2].stats['CAV5']) / 2)
    CAVstd_arith = ((station[0].stats['CAVstd'] +
                     station[2].stats['CAVstd']) / 2)

    # Calculate max horizontal component 
    for i in range(len(station)):
        if station[0].stats.CAV > station[2].stats.CAV:
            CAV_max = station[0].stats.CAV
        else:
            CAV_max = station[2].stats.CAV

        if station[0].stats.CAV5 > station[2].stats.CAV5:
            CAV5_max = station[0].stats.CAV5
        else:
           CAV5_max = station[2].stats.CAV5

        if station[0].stats.CAVstd > station[2].stats.CAVstd:
            CAVstd_max = station[0].stats.CAVstd
        else:
            CAVstd_max = station[2].stats.CAVstd
            
    return(CAV_geom, CAV5_geom, CAVstd_geom, CAV_arith, CAV5_arith,
           CAVstd_arith, CAV_max, CAV5_max, CAVstd_max)

    
    
    