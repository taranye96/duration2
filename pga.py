#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:32:31 2018

@author: tnye
"""

# Third party imports
import numpy as np


def get_pga(acc):
    """ 
    Obtains PGA from a list of accelereation data.

    Args:
        acc (array): Array of acceleration values. 

    Returns:
        pga (float): Peak ground acceleration.  

    """

    # Turn acceleration into a numpy array.  
    acc = np.array(acc)

    # Obtain max value from accerlerations.  
    pga = np.amax(abs(acc))

    return(pga)


def get_horizontal_pga(acc1, acc2):
    """
    Calculates arithmetic mean of PGA for 2 horizontal components and max
    horizontal PGA. 

    Args:
        acc1 (array): Array of acceleration values for one horizontal
            component. 
        acc2 (array): Array of acceleration values for the other horizontal
            component. 

    Returns:
        pga_arith (float): Arithmetic mean of the two pga values. 
        pga_max (float): Max PGA for two PGA values.  

    """

    # Get PGA from accelerations. 
    pga1 = get_pga(acc1)
    pga2 = get_pga(acc2)

    # Turn pga values into a list. 
    pga_list = [pga1, pga2]

    # Calculate arithmetic mean for PGA. 
    pga_arith = (pga1 + pga2)/2

    # Choose max PGA value. 
    pga_max = max(pga_list)

    return(pga_arith, pga_max)






