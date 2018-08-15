#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:22:22 2018

@author: tnye
"""

# Third party imports. 
import numpy as np
import pandas as pd

# Local imports. 
from openquake.hazardlib.gsim.travasarou_2003 import TravasarouEtAl2003
from openquake.hazardlib.imt import IA
from openquake.hazardlib.gsim.base import SitesContext
from openquake.hazardlib.gsim.base import DistancesContext
from openquake.hazardlib.gsim.base import RuptureContext
from openquake.hazardlib import const


# Create an instance of the gmpe and input contexts.
trav2003 = TravasarouEtAl2003()
sx = SitesContext()
rx = RuptureContext()
dx = DistancesContext()

# Import data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/select_data.csv')

# Define IMTs and standard deviations.
imt = IA()
sd_types = [const.StdDev.INTER_EVENT, const.StdDev.INTRA_EVENT]

# List of event IDs. 
eventids = ['usp000a1b0', 'usp000d6vk', 'usp000fg9t', 'usp000g9h6', 'us2000gge9',
            'us1000etmq', 'us2000dwh6', 'nc30228270', 'nc72282711', 'ci14383980',
            'ci14607652', 'usp0009eq0']

# Calculate mean Arias intensity and the standard deviations.
Trav_Ia_mean = []
interSD = []
intraSD = []

for event in eventids:
    partial_df = df.loc[df['USGS_eventID'] == event]

    sx.vs30 = np.array(partial_df['Vs30(m/s)'])
    dx.rrup = np.array(partial_df['rrup'])
    rx.mag = np.array(partial_df['magnitude'])[0]
    rx.rake = np.array(partial_df['rake_angle'])[0]
    Ia_mean, sd = trav2003.get_mean_and_stddevs(sx, rx, dx, imt, sd_types)

    Trav_Ia_mean.append(np.exp(Ia_mean))
    interSD.append(sd[0])
    intraSD.append(sd[1])

# Flatten lists.
flat_Ia = [val for sublist in Trav_Ia_mean for val in sublist]
flat_interSD = [val for sublist in interSD for val in sublist]
flat_intraSD = [val for sublist in intraSD for val in sublist]

# Calculate residuals.
Ia_obs = np.array(df['Ia_arith(m/s)'])
logIa_obs = np.log(Ia_obs)
logIa_pred = np.log(flat_Ia)
residuals = logIa_obs - logIa_pred

# Add data to data frame.
df['Trav_Ia'] = flat_Ia
df['Trav_Inter_SD'] = flat_interSD
df['Trav_Intra_SD'] = flat_intraSD
df['Trav_res'] = residuals
df.to_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Trav.csv')
