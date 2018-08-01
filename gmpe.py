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
        PGA (array): Array of peak ground accelerations (g). 
        mag (float): Array of moment magnitudes.
        Vs30 (float): Array of average Vs30 values (m/s). 

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
        PGA (float): Peak ground acceleration (g). 
        mag (float): Moment magnitude.
        Vs30 (float): Average Vs30 (m/s). 

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


def get_FoulserPiggott(mag, Vs30, rake, rrup, heteroskedastic=True):
    """
    Calculates Arias intensity for horizontal components using the
    Foulser-Piggott GMPE.

    Args:
        mag (array): Array of moment magnitudes.  
        Vs30 (array): Array of Vs30 values (m/s). 
        rake (array): Array of rake angles. 
        rrup (array): Array of rupture distances (km). 
        heteroskedastic (bool): Use heteroskedastic coefficients?
         
    Returns:
        

    """

    # GMPE coefficients
    if heteroskedastic:
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
    else:
        c1 = 5.1961
        c2 = -0.2371
        c3 = -3.6561
        c4 = 0.2309
        c5 = 5.4651
        c6 = 0.3186
        v1 = -1.1335
        v2 = -0.6519
        v3 = -0.0022
        v4 = 0.1327
    
        # Sigma constants
        d1 = np.nan
        d2 = np.nan
        d3 = np.nan
        sigE = 0.6812
        sigA = 0.8975
    
        # Constants??
        Vref = 1100
        V1 = 280

    # Calculate Ia mean
    FP_Ia_mean = []
    refIa = []
    for i in range(len(rake)):
        if rake[i] >= 45 and rake[i] <= 135:
            FRV = 1
        else:
            FRV = 0

        lnIa_ref = \
            c1 + \
            (c2 * (8.5 - mag[i])**2) + \
            ((c3 + (c4 * mag[i])) *
                np.log(np.sqrt(rrup[i]**2 + c5**2))) + \
            (c6 * FRV)
        
        Ia_ref = np.exp(lnIa_ref)
        refIa.append(Ia_ref)

        f_site = ((v1 * np.log(Vs30[i]/Vref)) + 
                  (v2 * (np.exp(v3 * (min(Vs30[i], 1100) - v1)) - 
                         np.exp(v3 * (Vref - V1))) * 
                   np.log((Ia_ref + v4) / v4)))

        Ia = np.exp(lnIa_ref + f_site)
        FP_Ia_mean.append(Ia)

    return(FP_Ia_mean, refIa)


def get_FoulserPiggott_single(mag, Vs30, rake, rrup):
    """
    Calculates Arias intensity for horizontal components using the
    Foulser-Piggott GMPE.

    Args:
        mag (float): Moment magnitude 
        Vs30 (float): Vs30 value (m/s). 
        rake (float): Rake angle.
        Rrup (float): Rupture distance (km). 
         
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

    # Constants??
    Vref = 1100
    V1 = 280

    # Calculate Ia mean
    FP_Ia_mean = []
    refIa = []

    if rake >= 45 and rake <= 135:
        FRV = 1
    else:
        FRV = 0

    lnIa_ref = c1 + (c2 * (8.5 - mag)**2) + ((c3 + (c4 * mag)) *
                 math.log(math.sqrt(rrup**2 + c5**2))) + (c6 * FRV)
    
    Ia_ref = math.exp(lnIa_ref)
    refIa.append(Ia_ref)

    f_site = ((v1 * math.log(Vs30/Vref)) + (v2 * (math.exp(v3 * (min(Vs30, 1100) - v1)) - math.exp(v3 * (Vref - V1))) * math.log((Ia_ref + v4) / v4)))

    Ia = math.exp(lnIa_ref + f_site)
    FP_Ia_mean.append(Ia)

    return(FP_Ia_mean, refIa)


def get_Travasarou_array(mag, Vs30, rake, rrup):
    """
    Calculates Arias intensity for horizontal components using the
    Travasarou GMPE.

    Args:
        mag (array): Array of moment magnitudes.  
        Vs30 (array): Array of Vs30 values (m/s). 
        rake (array): Array of rake angles. 
        Rrup (array): Array of rupture distances (km). 
         
    Returns:
        

    """

    # GMPE regression coefficients. 
    c1 = 2.800
    c2 = -1.981
    c3 = 20.72
    c4 = -1.703
    h = 8.78
    s11 = 0.454
    s12 = 0.101
    s21 = 0.479
    s22 = 0.334
    f1 = -0.166
    f2 = 0.512

    Trav_Ia_mean = []
    for i in range(len(mag)):

        if Vs30[i] > 760.0:
            SC = 0
            SD = 0
        elif Vs30[i] >= 360.0 and Vs30[i] <= 760.0:
            SC = 1
            SD = 0
        else:
            SC = 0
            SD = 1

        if rake[i] >= - 112.5 and rake[i] <= -67.5:
            FN = 1
            FR = 0
        elif rake[i] >=22.5 and rake[i] <= 157.5:
            FN = 0
            FR = 1
        else:
            FN = 0
            FR = 0

        Ia = math.exp(c1 + (c2 * (mag[i] - 6)) + (c3 * math.log(mag[i] / 6)) +
                      (c4 * math.log(math.sqrt(rrup[i]**2 + h**2))) + ((s11 +
                      (s12 * (mag[i] - 6))) * SC) + ((s21 + (s22 * (mag[i] - 6))) * SD)
                      + (f1 * FN) + (f2 * FR))
        Trav_Ia_mean.append(Ia)

    return(Trav_Ia_mean)


def get_Travasarou_single(mag, Vs30, rake, rrup):
    """
    Calculates Arias intensity for horizontal components using the
    Travasarou GMPE.

    Args:
        mag (float): Moment magnitude.  
        Vs30 (float): Vs30 value (m/s). 
        rake (float): Rake angle. 
        Rrup (float: Rupture distance (km). 
         
    Returns:
        

    """

    # GMPE regression coefficients. 
    c1 = 2.800
    c2 = -1.981
    c3 = 20.72
    c4 = -1.703
    h = 8.78
    s11 = 0.454
    s12 = 0.101
    s21 = 0.479
    s22 = 0.334
    f1 = -0.166
    f2 = 0.512

    Trav_Ia_mean = []
    
    if Vs30 > 760.0:
        SC = 0
        SD = 0
    elif Vs30 >= 360.0 and Vs30 <= 760.0:
        SC = 1
        SD = 0
    else:
        SC = 0
        SD = 1

    if rake >= - 112.5 and rake <= -67.5:
        FN = 1
        FR = 0
    elif rake >=22.5 and rake <= 157.5:
        FN = 0
        FR = 1
    else:
        FN = 0
        FR = 0

    Ia = math.exp(c1 + (c2 * (mag - 6)) + (c3 * math.log(mag / 6)) +
                  (c4 * math.log(math.sqrt(rrup**2 + h**2))) + ((s11 +
                  (s12 * (mag - 6))) * SC) + ((s21 + (s22 * (mag - 6))) * SD)
                  + (f1 * FN) + (f2 * FR))
    Trav_Ia_mean.append(Ia)

    return(Trav_Ia_mean)
    






