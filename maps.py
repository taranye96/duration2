#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 15:00:08 2018

@author: tnye
"""

import numpy as np
from shakelib.utils.containers import ShakeMapOutputContainer
from mapio.grid2d import Grid2D
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat


file = '/Users/tnye/PROJECTS/Duration/data/events/usp000a1b0/shakemap/shake_result.hdf'

oc = ShakeMapOutputContainer.load(file)

mag = oc.getRuptureObject().getOrigin().mag

pga_dict = oc.getIMTGrids('PGA', 'GREATER_OF_TWO_HORIZONTAL')
pga_mean_grid2d = pga_dict['mean']
pga_stddev_grid2d = pga_dict['std']
pga_mean = pga_mean_grid2d.getData()
pga_stddev = pga_stddev_grid2d.getData()

vs30_2d, vs30_metadata = oc.getGrid('vs30')
vs30_data = vs30_2d.getData()

rrup_2d, rrup_metadata = oc.getGrid('distance_rrup')
rrup_data = rrup_2d.getData()

oc.close()

log_Ia = 0.552 + 1.644 * pga_mean / np.log(10) + 0.297 * (mag - 6.0) + -0.454 * np.log10(vs30_data / 500)

# Basic fig
fig = plt.figure(figsize=(8, 6))
pos = plt.imshow(pga_mean / np.log(10))
plt.title("PGA")
fig.colorbar(pos)
fig = plt.figure(figsize=(8, 6))
pos = plt.imshow(log_Ia)
plt.title("Arias Intensity")
fig.colorbar(pos)

# plt.countourf test
data_crs = ccrs.PlateCarree()
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(1, 1, 1, projection=data_crs)

#ax.add_feature(cfeat.LAND)
#ax.add_feature(cfeat.OCEAN)
#ax.add_feature(cfeat.COASTLINE)

#ax.set_extent((131.9333, 134.8500, 34.0167, 36.5000))
ax.set_extent((125, 140, 30, 40))
ax.set_title('Liu Arias Intensity')

lons = np.linspace(131.9333, 134.8500, 351)
lats = np.linspace(34.0167, 36.5000, 299)


ax.coastlines(resolution='50m')
cb = ax.contourf(lons, lats, pga_mean/np.log(10), transform=data_crs)
plt.colorbar(cb, cmap='flag', orientation='vertical', ticklocation='auto')
plt.show()




