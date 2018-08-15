#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 09:07:34 2018

@author: tnye
"""

# Third party imports
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt


# Import data frame.
df = pd.read_csv('/Users/tnye/PROJECTS/Duration/data/dataframes/add_Liu_pred.csv')

# Obtain residuals from data frame. 
res_types = ['Trav_res', 'FP_res', 'Liu_res', 'Liu_pred_res']

# Specifiy models. 
models = ['Travasarou', 'Foulser-Piggott', 'Liu', 'Liu_&_GMPE']

Avg_Bias = []
Tau = []
Phi = []

for res_type in res_types:

    # Select event IDs. 
    df2 = df[['USGS_eventID', res_type]]

    mod = smf.mixedlm(" ".join([res_type, '~', '1']), df2, groups=df["USGS_eventID"])
    mod_fit = mod.fit()
    
    # Summary
    summary = mod_fit.summary
    
    # Random effects
    rdm_effects = mod_fit.random_effects
    
    # Fixed effects
    fxd_effects = mod_fit.fe_params.Intercept
    Avg_Bias.append(fxd_effects)
    
    # Random effect standard deviation (tau)
    tau = np.array(np.sqrt(mod_fit.cov_re))
    tau = tau[0][0]
    Tau.append(tau)

    # Within-group standard deviation (phi)
    phi = np.sqrt(mod_fit.scale)
    Phi.append(phi)

#Turn data regression results into a dictionary. 
data = {'Model': models, 'Avg_Bias': Avg_Bias, 'Phi': Phi, 'Tau': Tau}

# Turn dictionary into a data frame. 
df_res = pd.DataFrame(data, columns = ['Model', 'Avg_Bias', 'Phi', 'Tau'])
df_res.to_csv('/Users/tnye/PROJECTS/Duration/data/std_dev.csv', index=False)


#####Plot Results#####
# Liu
liu = np.array(df['Liu_res'])
binwidth = 0.055828
plt.hist(liu, bins=np.arange(min(liu), max(liu) + binwidth, binwidth), edgecolor='black')
plt.title('Liu Residual Distribution')
plt.xlabel('')
plt.ylabel('Frequency')
plt.axvline(-0.102552, color='k', linestyle='dashed', linewidth=1)

# Trav
trav = np.array(df['Trav_res'])
binwidth = 0.235532
plt.hist(trav, bins=np.arange(min(trav), max(trav) + binwidth, binwidth), edgecolor='black')
plt.title('Trav Residual Distribution')
plt.xlabel('')
plt.ylabel('Frequency')
plt.axvline(-0.435106, color='k', linestyle='dashed', linewidth=1)

# FP
fp = np.array(df['FP_res'])
binwidth = 0.284588
plt.hist(fp, bins=np.arange(min(fp), max(fp) + binwidth, binwidth), edgecolor='black')
plt.title('FP Residual Distribution')
plt.xlabel('')
plt.ylabel('Frequency')
plt.axvline(-0.101483 , color='k', linestyle='dashed', linewidth=1)

