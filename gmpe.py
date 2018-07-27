#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:16:24 2018

@author: tnye
"""

# Third party imports 
import numpy as np
import math


def get_Liu_array(PGA, mag, Vs30):
    """
    Calculates Arias intensity for horizontal components using the Liu GMPE.

    Args:
        PGA (array): Array of peak ground accelerations. 
        mag (float): Array of moment magnitudes.
        Vs30 (float): Array of average Vs30 values. 

    Returns:
        Liu_Ia_mean (Array): Array of predicted mean Arias intensities. 

    """

    # GMPE regression coefficients. 
    a = 0.552
    b = 1.644
    c = 0.297
    d = -0.454

    # Sigma constants
    sig = 0.164
    tau = 0.071
    sig_t = 0.178

    # Create arrays of the constants
    Sig = np.full((1, len(PGA)), sig)
    Tau = np.full((1, len(PGA)), tau)
    Sig_t = np.full((1, len(PGA)), sig_t)

    Liu_Ia_mean = []
    for i in range(len(PGA)):
        Ia = 10**(a + (b * np.log10(PGA[i])) + (c * (mag[i] - 6)) +
                      (d * np.log10(Vs30[i] / 500)))
        Liu_Ia_mean.append(Ia)

    return(Liu_Ia_mean, Sig, Tau, Sig_t)    


def get_Liu_single(PGA, mag, Vs30):
    """
    Calculates Arias intensity for horizontal components using the Liu GMPE.

    Args:
        PGA (float): Peak ground acceleration. 
        mag (float): Moment magnitude.
        Vs30 (float): Average Vs30. 

    Returns:
        Liu_Ia_mean (float): Predicted mean Arias intensity. 

    """

    # GMPE regression coefficients. 
    a = 0.552
    b = 1.644
    c = 0.297
    d = -0.454

    # Sigma constants
    sig = 0.164
    tau = 0.071
    sig_t = 0.178

    
    Liu_Ia_mean = 10**(a + (b * np.log10(PGA)) + (c * (mag - 6)) + (d * np.log10(Vs30 / 500)))

    return(Liu_Ia_mean)


def get_FoulserPiggot(mag, Vs30, rake, Rrup):
    """
    Calculates Arias intensity for horizontal components using the
    Foulser-Piggott GMPE.

    Args:
        mag (array): Array of moment magnitudes.  
        Vs30 (array): Array of Vs30 values. 
        rake (arrau): Array of rake angles. 
        Rrup (array): Array of rupture distances. 
         
        

    Returns:
        

    """

    # GMPE coefficients
    c1 = 4.9862
    c2 = -0.1939
    c3 = -4.0332
    c4 = 0.2887
    c5 = 6.3049
    c6 = 0.3507
    v1 = -1.1576
    v2 = -0.4576
    v3 = -0.0029
    v4 = 0.0818

    # Sigma constants
    d1 = -0.5921
    d2 = 3.8311
    d3 = 4.0762
    sigE = 0.6556
    sigA = 0.5978

    # Constants??
    Vref = 1100
    V1 = 280

    # Calculate Ia mean
    FP_Ia_mean = []
    for i in range(len(rake)):
        if rake[i] >= 45 and rake[i] <= 135:
            FRV = 1
        else:
            FRV = 0

        lnIa_ref = c1 + (c2 * (8.5 - mag[i])**2) + ((c3 + (c4 * mag[i])) *
                     math.log(math.sqrt(Rrup[i]**2 + c5**2))) + (c6 * FRV)

        f_site = ((v1 * math.log(Vs30[i]/Vref)) + (v2 * (math.exp(v3 * (min(Vs30[i], 1100) - v1)) - math.exp(v3 * (Vref - V1))) * math.log((math.exp(lnIa_ref) + v4) / v4)))

        Ia = math.exp(lnIa_ref + f_site)
        FP_Ia_mean.append(Ia)

    return(FP_Ia_mean)
    






