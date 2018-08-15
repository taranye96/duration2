#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 11:23:50 2018

@author: tnye
"""

# Standard library imports. 
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import numpy as np
from shakelib.utils.containers import ShakeMapOutputContainer
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
import cartopy.feature as cfeat

# Local imports
import gmpe


# Define projection.
data_crs = ccrs.PlateCarree()

# Path to ShakeMap 4 file
file = '/Users/tnye/PROJECTS/Duration/data/events/usp000a1b0/shakemap/shake_result.hdf'

# Obtain output container for file.
oc = ShakeMapOutputContainer.load(file)

# Obtain magnitude from output container.
mag = oc.getRuptureObject().getOrigin().mag

# Create a dictionary of pga data. 
pga_dict = oc.getIMTGrids('PGA', 'GREATER_OF_TWO_HORIZONTAL')
pga_mean_grid2d = pga_dict['mean']
pga_stddev_grid2d = pga_dict['std']
pga_mean = pga_mean_grid2d.getData()
pga_stddev = pga_stddev_grid2d.getData()

min_lon = pga_dict['mean'].getGeoDict().xmin
max_lon = pga_dict['mean'].getGeoDict().xmax
min_lat = pga_dict['mean'].getGeoDict().ymin
max_lat  = pga_dict['mean'].getGeoDict().ymax
num_pts_x = pga_dict['mean'].getGeoDict().nx
num_pts_y = pga_dict['mean'].getGeoDict().ny

# Get vs30 and rrup data. 
vs30_2d, vs30_metadata = oc.getGrid('vs30')
vs30_data = vs30_2d.getData()
rrup_2d, rrup_metadata = oc.getGrid('distance_rrup')
rrup_data = rrup_2d.getData()

# Define magnitude and rake.
mag = np.full_like(pga_mean, mag)
rake = np.full_like(pga_mean, -173)

oc.close()

# Get pga in format for figure. 
pga = np.exp(pga_mean)
pga = np.flipud(pga)

# Calculate Arias intentisy using FP GMPE. 
(Ia, refIa, sc) = gmpe.get_FoulserPiggott(mag, vs30_data, rake, rrup_data, heteroskedastic=True)
Ia = np.flipud(Ia)


##### ShakeMaps #####
# Mean
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(1, 1, 1, projection=data_crs)
ax.set_extent((min_lon, max_lon, min_lat, max_lat))
lons = np.linspace(min_lon, max_lon, num_pts_x)
lats = np.linspace(min_lat, max_lat, num_pts_y)
ax.coastlines(resolution='50m')
ax.add_feature(cfeat.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='face', facecolor='azure'))
cb = ax.contour(lons, lats, Ia, cmap=cm.OrRd, transform=data_crs)
plt.colorbar(cb, orientation='vertical', ticklocation='auto')
ax.set_title('Foulser-Piggott Arias Intensity')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/fp_shake.png', dpi=300)

# Standard Deviation



