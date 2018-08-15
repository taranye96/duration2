#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 15:00:08 2018

@author: tnye
"""

# Third party imports
import numpy as np
from shakelib.utils.containers import ShakeMapOutputContainer
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
import cartopy.feature as cfeat


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

oc.close()

# Get pga in format for figure. 
pga = np.exp(pga_mean)
pga = np.flipud(pga)

# Calculate Arias intentisy using Liu model. 
log_Ia = 0.552 + 1.644 * pga_mean / np.log(10) + 0.297 * (mag - 6.0) + -0.454 * np.log10(vs30_data / 500)
Ia = 10**(log_Ia)
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
plt.plot([133.134], [35.456], marker='*', markersize=20, color='y')
ax.set_title('Liu Arias Intensity')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/liu_shake.png', dpi=300)




