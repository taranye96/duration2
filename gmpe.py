#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:16:24 2018

@author: tnye
"""

# Third party imports 
import numpy as np


def get_Liu_array(PGA, mag, Vs30):
    """
    Calculates Arias intensity for horizontal components using the Liu GMPE.

    Args:
        PGA (array): Array of peak ground accelerations. 
        mag (float): Array of moment magnitudes.
        Vs30 (float): Array of average Vs30 values. 

    Returns:
        Ia (Array): Array of predicted Arias intensities. 

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
#    Sig = np.full((1, len(PGA)), sig)
#    Tau = np.full((1, len(PGA)), tau)
#    Sig_t = np.full((1, len(PGA)), sig_t)

    Liu_Ia = []
    for i in range(len(PGA)):
        Ia = 10**(a + (b * np.log10(PGA[i])) + (c * (mag[i] - 6)) +
                      (d * np.log10(Vs30[i] / 500)))
        Liu_Ia.append(Ia)
    
#    Liu_Ia = 10**(a + (b * np.log10(PGA)) + (c * (mag - 6)) + (d * np.log10(Vs30 / 500)))

    return(Liu_Ia)    


def get_Liu_single(PGA, mag, Vs30):
    """
    Calculates Arias intensity for horizontal components using the Liu GMPE.

    Args:
        PGA (float): Peak ground acceleration. 
        mag (float): Moment magnitude.
        Vs30 (float): Average Vs30. 

    Returns:
        Ia (float): Predicted Arias intensity. 

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

    
    Liu_Ia = 10**(a + (b * np.log10(PGA)) + (c * (mag - 6)) + (d * np.log10(Vs30 / 500)))

    return(Liu_Ia)