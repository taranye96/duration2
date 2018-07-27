#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:22:22 2018

@author: tnye
"""

# Main imports for calculation
import numpy as np
from openquake.hazardlib.gsim.travasarou_2003 import BooreEtAl2014
from openquake.hazardlib.imt import IA
from openquake.hazardlib.gsim.base import SitesContext
from openquake.hazardlib.gsim.base import DistancesContext
from openquake.hazardlib.gsim.base import RuptureContext
from openquake.hazardlib import const
from openquake.hazardlib.gsim.base import GMPE, CoeffsTable

# Stuff for plotting
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("ticks")

# Create an instance of the gmpe and input contexts
trav2003 = TravasarouEtAl2003()
sx = SitesContext()
rx = RuptureContext()
dx = DistancesContext()

# Define what IMTs and standard deviations you want
imt = IA()
sd_types = [const.StdDev.INTER_EVENT, const.StdDev.INTRA_EVENT]

# Fill in values in the contexts:
dx.rrup = np.logspace(-1, 2, 500)          #Why is this not just the rjb val
sx.vs30 = np.full_like(dx.rjb, 180)     #what is this
rx.mag = 6.7
rx.rake = -173

# Evaluate the GMPE
Ia_mean, sd = trav2003.get_mean_and_stddevs(sx, rx, dx, imt, sd_types)

plt.semilogx(dx.rjb, Ia_mean)