# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:38:28 2022

@author: compute
"""

import pandas as pd
import matplotlib.pyplot as plt


## ---------- TASK 1-2: Load and Parse the data ----------
# First load the data & convert to a dataframe
raw_data= pd.read_json('raw_data.json')
print(raw_data.head())

# What data do we have?
print(list(raw_data))
parsed_data= raw_data

## ---------- TASK 3: Add a column ----------
# Add a "Score" column of (KDA + damage)/gold_earned
parsed_data['Score']= (parsed_data['KDA'] +parsed_data['total_damage']) /parsed_data['gold_earned']
print(parsed_data.head())

## ---------- TASK 4: Make a graph ----------
# See if trend between gold earned and total damage
plt.scatter(parsed_data['gold_earned'],parsed_data['total_damage'] )
plt.xlabel('gold_earned')
plt.ylabel('total_damage')
