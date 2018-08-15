#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 15:09:12 2018

@author: tnye
"""

import numpy as np

def get_Baker_eq6(T):
    """
    Calculates correlation coefficient between spectral acceleration and Arias
    intensity given a specified period between 0.05 and 5 seconds.

    Args:
        T (float): Spectral period in seconds. 
    Returns:
        p (float): Correlation between spectral acceleration and period.

    """

    if T >= 0.05 and T < 0.11:
        p = 0.344 - (0.152 * np.log(T))
    elif T >= 0.11 and T < 0.4:
        p = 0.971 + (0.131 * np.log(T))
    else:
        p = 0.697 - (0.166 * np.log(T))

    return(p)