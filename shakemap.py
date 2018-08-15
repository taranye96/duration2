#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 10:46:18 2018

@author: tnye
"""

# Third party imports
import matplotlib.pyplot as plt
import matplotlib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
import numpy.ma as ma
from scipy.io import loadmat
from mapio import shake


grid = shake.ShakeGrid.load('/Users/tnye/PROJECTS/Duration/data/events/usp000a1b0/shakemap/shakemap_grid.xml')
pga_layer = grid.getLayer('pga')
pga_data = pga_layer.getData 

projection = ccrs.PlateCarree
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw=dict(projection=projection))
ax.set_extent(bbox)
ax.coastlines(resolution='50m')
gl = ax.gridlines(draw_labels=True)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

cmap = plt.get_cmap('rainbow')
bbox = [lons.min(), lons.max(), lats.min(), lats.max()]
fig, ax = make_map(bbox=bbox)
cs = ax.pcolormesh(lons, lats, data, cmap=cmap)
cbar = fig.colorbar(cs, extend='both', shrink=0.5, orientation='horizontal')
cbar.set_label(str(grid.getLocationName()) +" " \
               + str(grid.getLevel()) + " " \
               + str(grid.getParameter()) \
               + " (" + str(grid.getUnit()) + ") " \
               + "valid " + str(grid.getDataTime().getRefTime()))