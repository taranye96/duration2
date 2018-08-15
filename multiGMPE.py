#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 17:54:50 2018

@author: tnye
"""

# Standard library imports 
import os
import glob 

# Third party imports
import numpy as np
import pandas as pd
import scipy.constants as sp

# Local imports 
from openquake.hazardlib.gsim.boore_2014 import BooreEtAl2014
from openquake.hazardlib.gsim.campbell_bozorgnia_2014 import CampbellBozorgnia2014
from openquake.hazardlib.gsim.abrahamson_2014 import AbrahamsonEtAl2014
from openquake.hazardlib.gsim.chiou_youngs_2014 import ChiouYoungs2014
from openquake.hazardlib.imt import PGA, SA
from openquake.hazardlib.gsim.base import SitesContext
from openquake.hazardlib.gsim.base import DistancesContext
from openquake.hazardlib.gsim.base import RuptureContext
from openquake.hazardlib import const
from shakelib.multigmpe import MultiGMPE
from shakelib.rupture.factory import get_rupture
from shakelib.rupture.origin import Origin


# List of GMPEs to use.
gmpe_list = [
    BooreEtAl2014(),
    CampbellBozorgnia2014(), 
    AbrahamsonEtAl2014(), 
    ChiouYoungs2014()
]

# GMPE weights.
weight_list = [0.25] * 4

# Intensity measure component.
imc = const.IMC.RotD50

# Create multigmpe instance.
gmpe = MultiGMPE.from_list(gmpe_list, weight_list, imc)

# Define IMTs and standard deviations.
imts = [PGA(), SA(0.1), SA(0.2), SA(0.3), SA(0.5), SA(1), SA(2),
        SA(3), SA(5)]
sd_types = [const.StdDev.INTER_EVENT, const.StdDev.INTRA_EVENT]


# Import data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Liu.csv')

# Get list of event IDs.
eventids = ['usp000a1b0', 'usp000d6vk', 'usp000fg9t', 'usp000g9h6', 'us2000gge9',
            'us1000etmq', 'us2000dwh6', 'nc30228270', 'nc72282711', 'ci14383980',
            'ci14607652', 'usp0009eq0']

# Calculate spectrals for each event.
pga = []
sa0_1 = []
sa0_2 = []
sa0_3 = []
sa0_5 = []
sa1 = []
sa2 = []
sa3 = []
sa5 = []
spectrals = [pga, sa0_1, sa0_2, sa0_3, sa0_5, sa1, sa2, sa3, sa5]

pga_std = []
sa0_1_std = []
sa0_2_std = []
sa0_3_std = []
sa0_5_std = []
sa1_std = []
sa2_std = []
sa3_std = []
sa5_std = []
stds = [pga_std, sa0_1_std, sa0_2_std, sa0_3_std, sa0_5_std, sa1_std, sa2_std,
        sa3_std, sa5_std]

# Separate data by event.
for event in eventids:
    partial_df = df.loc[df['USGS_eventID'] == event]
    
    # Data directory.
    data_dir = '/Users/tnye/PROJECTS/Duration/data/'
    # Event directory. 
    event_dir = os.path.join(data_dir, 'events', event)

    # Distance context.
    dx = DistancesContext()
    dx.rjb = np.array(partial_df['rjb'])
    dx.rrup = np.array(partial_df['rrup'])
    dx.rx = np.array(partial_df['rx'])
    dx.ry0 = np.array(partial_df['ry'])

    # Sites context.
    sx = SitesContext()
    sx.vs30 = np.array(partial_df['Vs30(m/s)'])
    sx = MultiGMPE.set_sites_depth_parameters(sx, gmpe)
    sx.vs30measured = np.zeros_like(sx.vs30, dtype=bool)

    # Rupture context.
    rx = RuptureContext()
    rx.mag = np.array(partial_df['magnitude'])[0]
    rx.rake = np.array(partial_df['rake_angle'])[0]
    rx.dip = np.array(partial_df['dip'])[0]
    rx.hypo_depth = np.array(partial_df['depth(km)'])[0]

    # Determine if there is a fault file.
    rupt_dir = os.path.join(event_dir, 'rupture_info')
    os.chdir(rupt_dir)
    rupture_file = []
    types = ('*_fault.txt', '*json')

    for file in types:
        rupture_file.extend(glob.glob(file))

    if len(rupture_file) != 0:
        filepath = os.path.join(rupt_dir, rupture_file[0])
 
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

        rupt =  get_rupture(origin, filepath, new_format=False)

        rx.width = rupt.getWidth()
        rx.ztor = rupt.getDepthToTop()
        

    # If there is no fault file, use hypocentral dist for rrup.
    else:
        rx.width = 10**(-0.76 + 0.27*rx.mag)
        rx.ztor = rx.hypo_depth
        
    
    # Evaluate the GMPE.
    for i in range(len(imts)):
        gmpe_imt_mean, gmpe_imt_sd = gmpe.get_mean_and_stddevs(sx, rx, dx, imts[i], sd_types)
        spectrals[i].append(gmpe_imt_mean)
        stds[i].append(gmpe_imt_sd)

# Flatten lists  .     
for i in range(len(spectrals)):
    spectrals[i] = [item for sublist in spectrals[i] for item in sublist]
#    stds[i] = [item for sublist in stds[i] for item in sublist]

# Add to data frame
df['multiPGAgal'] = np.exp(np.array(spectrals[0]))*sp.g*100
df['multiSA(0.1)gal'] = np.exp(np.array(spectrals[1]))*100
df['multiSA(0.2)gal'] = np.exp(np.array(spectrals[2]))*100
df['multiSA(0.3)gal'] = np.exp(np.array(spectrals[3]))*100
df['multiSA(0.5)gal'] = np.exp(np.array(spectrals[4]))*100
df['multiSA(1)gal'] = np.exp(np.array(spectrals[5]))*100
df['multiSA(2)gal'] = np.exp(np.array(spectrals[6]))*100
df['multiSA(3)gal'] = np.exp(np.array(spectrals[7]))*100
df['multiSA(5)gal'] = np.exp(np.array(spectrals[8]))*100

#df['multiPGA_sd'] = np.exp(np.array(stds[0])/sp.g)
#df['multiSA(0.1)_sd'] = np.exp(np.array(stds[1])/sp.g)
#df['multiSA(0.2_sd)'] = np.exp(np.array(stds[2])/sp.g)
#df['multiSA(0.3)_sd'] = np.exp(np.array(stds[3])/sp.g)
#df['multiSA(0.5)_sd'] = np.exp(np.array(stds[4])/sp.g)
#df['multiSA(1)_sd'] = np.exp(np.array(stds[5])/sp.g)
#df['multiSA(2)_sd'] = np.exp(np.array(stds[6])/sp.g)
#df['multiSA(3)_sd'] = np.exp(np.array(stds[7])/sp.g)
#df['multiSA(5)_sd'] = np.exp(np.array(stds[8])/sp.g)

df.to_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_multiGMPE.csv', index=False)

# Note: units of both mean and sd are natural log of g in this case.
        