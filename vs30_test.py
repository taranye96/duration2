#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 11:51:06 2018

@author: tnye
"""

import fiona

japan_shp = '/Users/tnye/PROJECTS/Duration/data/Vs30/japan_map/Z-V2-JAPAN-AMP-VS400_M250-SHAPE.shp'
minlon = 123
maxlon = 146
minlat = 26
maxlat = 46

# Register format drivers with a context manager
with fiona.drivers():

    # Open a file for reading
    with fiona.open(japan_shp) as source:
        meta = source.meta
        meta['schema']['geometry'] = 'Point'

        
        with fiona.open('test_write.shp', 'w', **meta) as sink:

            for f in source.filter(bbox=(minlon, minlat, maxlon, maxlat)):
                f['geometry'] = {
                    'type': 'Point',
                    'coordinates': f['geometry']['coordinates'][0][0]}

                sink.write(f)

with fiona.collection(japan_shp, 'r') as layer:
    for element in layer:
        if element['geometry'] == (135, 35):
            print(element['properties'])
     
        