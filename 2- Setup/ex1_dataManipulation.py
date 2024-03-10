# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 17:25:10 2024

@author: 417-devops
"""

import pandas as pd

# read in the data
air_quality= pd.read_csv('air_quality_no2.csv', index_col=0, parse_dates=True)
print(air_quality.head())

# make a plot
air_quality.plot()

# delete the column of Antwerp data
reduced_data= air_quality.drop(['station_antwerp'], axis=1)
print(reduced_data.head())