#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:51:00 2018

@author: tnye
"""
import knet_new


stations, station_stats = knet_new.get_knet_data(
        '/Users/tnye/PROJECTS/Duration/data/usp000a1b0/ground_motion/knt')

date, mag, source_lat, source_lon, depth = knet_new.get_earthquake_data(
        'usp000a1b0')

station_dist, p_arrivals = knet_new.append_station_stats(stations,
                                                         station_stats,
                                                         source_lat,
                                                         source_lon, depth)

knet_new.plot_z_arrivals_by_dist(stations, date)
