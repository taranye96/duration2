#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 16:09:09 2018

@author: tnye
"""

# Third party imports 
import numpy as np
import scipy.stats


def conf_int(data, confidence=0.95):
    """ 
    Computes mean confidence interval for a set of data and specified confidence
    interval. 

    Args:
        data (array): Array of data. 
        confidence (float): Confidence interval. 

    Returns:
        h
    """

    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)

    return(h)