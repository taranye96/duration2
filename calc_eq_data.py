#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 11:52:15 2018

@author: tnye
"""

# Third party imports
from libcomcat.search import get_event_by_id
from obspy.geodetics import gps2dist_azimuth, kilometers2degrees
from obspy.taup import TauPyModel
from obspy import Stream, UTCDateTime
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
# from matplotlib.pyplot import close


def get_earthquake_data(event_id, stations):
    """
    Obtains magnitude, latitude, longitude, and depth for an earthquake based
    off its event id.

    Args:
        event_id (str): USGS event id for a specific earthquake.
        stations (array): Combined streams of acceleration data for
            each station.

    Returns:
        event_id (str): USGS event id for a specific earthquake.
        date (time?): UTC date.time origin for source
        mag (float): Magnitude of earthquake.
        source_lat (float): Source latitude.
        source_lon (float): Source longitude.
        depth (float): Depth of earthquake origin in km.
    """

    detail = get_event_by_id(event_id)
    date = UTCDateTime(detail.time)
    mag = detail.magnitude
    source_lat = detail.latitude
    source_lon = detail.longitude
    depth = detail.depth

    # Add event stats to each trace in each station
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[i]
            eventID = event_id
            magnitude = mag
            source_depth = depth
            event_lat = source_lat
            event_lon = source_lon
            if detail.hasProduct('moment-tensor'):
                tensor = detail.getProducts('moment-tensor')[0]
                if tensor.hasProperty('nodal-plane-1-rake'):
                    rake = float(tensor['nodal-plane-1-rake'])
                    if rake > 180 and rake < 360:
                        rake = rake - 360
                elif tensor.hasProperty('nodal-plane-1-slip'):
                    rake = float(tensor['nodal-plane-1-slip'])
                    if rake > 180 and rake < 360:
                        rake = rake - 360
                else:
                    rake = 'Nan'
            else:
                rake = 'Nan'

            trace.stats.eventID = eventID
            trace.stats.mag = magnitude
            trace.stats.source_depth = source_depth
            trace.stats.source_lat = event_lat
            trace.stats.source_lon = event_lon
            trace.stats.rake = rake

    return (event_id, date, mag, source_lat, source_lon, depth, rake)


def get_dist_and_parrivals(stations, station_stats, depth):
    """
    Calculate distance between the source and each station for an event and
    the theoretical p-wave arrival times and appends them to the station stats.

    Args:
        stations (array): Combined streams of acceleration data for
            each station.
        station_stats (list): List of lat and lon coordinates for event.
        depth (float): Depth of earthquake origin in km.

    Returns:
    """

    model = TauPyModel(model="iasp91")
    for sta in stations:
        for i in range(len(sta)):
            trace = sta[i]

            # Compute distance.
            dist_az_baz = gps2dist_azimuth(
                    trace.stats['knet']['stla'],
                    trace.stats['knet']['stlo'],
                    trace.stats['knet']['evla'],
                    trace.stats['knet']['evlo'])
            distance_meters = dist_az_baz[0]
            distance_km = distance_meters/1000.0
            dd = kilometers2degrees(distance_km)
            trace.stats.distance = distance_meters
            trace.stats.distkm = distance_km

            # Estimate travel time for p wave.
            p = model.get_travel_times(depth, dd, phase_list=['p', 'P'])
            trace.stats.P_arriv = p[0].time

    return ()


def plot_z_arrivals_by_dist(stations, date):
    """
    Plot vertical component p-wave arrivals on waveforms that are sorted by
    distance from source.

    Args:
        stations (array): Combined streams of acceleration data for
            each station.
        date (time?): UTC date.time origin for source.
    Returns:
    """

    stz = Stream()
    for sta in stations:
        newtrace = sta.select(channel='UD')
        stz += newtrace

    sorted_stz = stz.sort(keys=['rdist'])

    new_sorted = sorted_stz[90:100]

    fig = plt.figure()
    new_sorted.plot(fig=fig, show=False)
    for i in range(len(new_sorted)):
        p_onset = date + new_sorted[i].stats['P_arriv']

        ax = fig.axes[i]
        ax.axvline(date2num(p_onset.datetime), lw=2)
        plt.show
