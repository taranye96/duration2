#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 13:44:32 2018

@author: tnye
"""

# Third party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import data frame
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/select_data.csv')
mags = np.array(df['magnitude'])
rrup = np.array(df['rrup'])
vs30 = np.array(df['Vs30(m/s)'])

#####Plot summaries#####
# Mag vs Vs30
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_yscale('log')
plt.plot(mags, vs30, 'ko')
plt.ylabel('Vs30 m/s')
plt.xlabel('Magnitude')
plt.title('Data Summary')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/datasum_mag_vs30.png', dpi=300)

# Mag vs Rrup
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_yscale('log')
plt.plot(mags, rrup, 'ko')
plt.ylabel('Rrup km')
plt.xlabel('Magnitude')
plt.title('Data Summary')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/datasum_mag_rrup.png', dpi=300)

# Rrup vs Vs30
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_yscale('log')
plt.plot(rrup, vs30, 'ko')
plt.ylabel('Vs30 m/s')
plt.xlabel('Rrup km')
plt.title('Data Summary')
plt.savefig('/Users/tnye/PROJECTS/Duration/figures/datasum_rrup_vs30.png', dpi=300)