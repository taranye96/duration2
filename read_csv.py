#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 10:05:51 2018

@author: tnye
"""

import csv

with open('earthquake_data.csv') as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            print(row)