#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 09:53:39 2018

@author: tnye
"""

# Third party imports
from shakelib.rupture.factory import get_rupture
from shakelib.rupture.origin import Origin
from shakelib.distance import get_distance


def get_fault_dist(rupture_file, stn_lats, stn_lons, depths):
    """
    Computes rrup, rjb, rx, and ry given a station and event.  

    Args:
        
    Returns:
        
    """
        
    # need a dummy origin
    origin = Origin({
        'id':'', 
        'netid':'', 
        'network':'', 
        'lat':0, 
        'lon':0, 
        'depth':0,
        'locstring':'', 
        'mag':0, 
        'time':''
    })

    # Calculate rupture 
    rupt = get_rupture(origin, rupture_file, new_format=False)
    
    methods = ['rrup', 'rjb', 'rx', 'ry']
    distances = get_distance(
        methods, 
        lat=stn_lats, 
        lon=stn_lons, 
        dep=depths,
        rupture=rupt
    )
            
    # Fill in the distances for this event
    rrup = distances['rrup']
    rjb = distances['rjb']
    rx = distances['rx']
    ry = distances['ry']

    return(rrup, rjb, rx, ry)
