# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:12:37 2022

@author: compute

Desc: Riot API Bootcamp Module 1 example
"""

import pandas as pd
import matplotlib.pyplot as plt

air_quality= pd.read_csv('air_quality_no2.csv', index_col=0, parse_dates=True)
print(air_quality.head())


air_quality.plot()