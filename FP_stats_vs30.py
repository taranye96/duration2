#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 17:21:29 2018

@author: tnye
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 17:15:21 2018

@author: tnye
"""

# Standard library imports
import os
os.chdir('/Users/tnye/PROJECTS/Duration/code')

# Third party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Local imports
from conf_interval import conf_int


# Read in dataframe.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_FP.csv')
vs30 = df['Vs30(m/s)']
residuals = df['FP_res']

# Bin residuals by vs30.
bins = np.logspace(2, 3.2, 8)

bin1 = []
bin2 = []
bin3 = []
bin4 = []
bin5 = []
bin6 = []
bin7 = []
bin8 = []
for i in range(len(vs30)):
    if vs30[i] >= bins[0] and vs30[i] < bins[1]:
        bin1.append(residuals[i])
    elif vs30[i] >=bins[1] and vs30[i] < bins[2]:
        bin2.append(residuals[i])
    elif vs30[i] >=bins[2] and vs30[i] < bins[3]:
        bin3.append(residuals[i])
    elif vs30[i] >=bins[3] and vs30[i] < bins[4]:
        bin4.append(residuals[i])
    elif vs30[i] >= bins[4] and vs30[i] < bins[5]:
        bin5.append(residuals[i])
    elif vs30[i] >= bins[5] and vs30[i] < bins[6]:
        bin6.append(residuals[i])
    elif vs30[i] >=bins[6] and vs30[i] < bins[7]:
        bin7.append(residuals[i])
    else: 
        bin8.append(residuals[i])

# Calculate mean and standard deviation for each bin.
bin1_mean = np.mean(bin1)
bin2_mean = np.mean(bin2)
bin3_mean = np.mean(bin3)
bin4_mean = np.mean(bin4)
bin5_mean = np.mean(bin5)
bin6_mean = np.mean(bin6)
bin7_mean = np.mean(bin7)
bin8_mean = np.mean(bin8)

bin1_conf = conf_int(bin1)
bin2_conf = conf_int(bin2)
bin3_conf = conf_int(bin3)
bin4_conf = conf_int(bin4)
bin5_conf = conf_int(bin5)
bin6_conf = conf_int(bin6)
bin7_conf = conf_int(bin7)
bin8_conf = conf_int(bin8)

# Bin midpoints.
mid1 = (bins[1]+bins[0])/2
mid2 = (bins[2]+bins[1])/2
mid3 = (bins[3]+bins[2])/2
mid4 = (bins[4]+bins[3])/2
mid5 = (bins[5]+bins[4])/2
mid6 = (bins[6]+bins[5])/2
mid7 = (bins[7]+bins[6])/2

##### Plot statistics and rsiduals #####
fig = plt.figure(figsize=(5,4))
plt.axvline(bins[1], color='b', linestyle='dashed', linewidth=1)
plt.axvline(bins[2], color='b', linestyle='dashed', linewidth=1)
plt.axvline(bins[3], color='b', linestyle='dashed', linewidth=1)
plt.axvline(bins[4], color='b', linestyle='dashed', linewidth=1)
plt.axvline(bins[5], color='b', linestyle='dashed', linewidth=1)
plt.axvline(bins[6], color='b', linestyle='dashed', linewidth=1)
plt.axvline(bins[7], color='b', linestyle='dashed', linewidth=1)
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.plot(vs30, residuals, 'o', color='#c0c0c0', markersize=2)
plt.errorbar(mid1, bin1_mean, yerr=bin1_conf, color='black', fmt='o',
             ecolor='k', elinewidth=3, markersize=5, zorder=100)
plt.errorbar(mid2, bin2_mean, yerr=bin2_conf, color='black', fmt='o',
             ecolor='k', elinewidth=3, markersize=5, zorder=100)
plt.errorbar(mid3, bin3_mean, yerr=bin3_conf, color='black', fmt='o',
             ecolor='k', elinewidth=3, markersize=5, zorder=100)
plt.errorbar(mid4, bin4_mean, yerr=bin4_conf, color='black', fmt='o',
             ecolor='k', elinewidth=3, markersize=5, zorder=100)
plt.errorbar(mid5, bin5_mean, yerr=bin5_conf, color='black', fmt='o',
             ecolor='k', elinewidth=3, markersize=5, zorder=100)
plt.errorbar(mid6, bin6_mean, yerr=bin6_conf, color='black', fmt='o',
             ecolor='k', elinewidth=3, markersize=5, zorder=100)
plt.errorbar(mid7, bin7_mean, yerr=bin7_conf, color='black', fmt='o',
             ecolor='k', elinewidth=3, markersize=5, zorder=100)
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.get_yaxis().get_major_formatter().labelOnlyBase = False
ax.set_xlim(100, 1500)
ax.set_ylim(-7.5, 7.5)
ax.set_ylabel('Residuals')
ax.set_xlabel('vs30')
ax.set_title('95% Confidence Level of Foulser-Piggott Residuals')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/FP_residuals_vs30_bins.png')