# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:20:39 2024

@author: 417-DevOps
Example of working with static data
1) Read through champion.json and extract the ADCs
2) Sort by attack range
"""

import pandas as pd


#%% read in the champion data json, retaining only the data field
champ_data= pd.json_normalize(pd.read_json('ddragon_full_champ_data-KEYS.json').data)


#%% retain only the fields we care about
champ_data= champ_data[['id','key','tags','stats.attackrange']]
# print(champ_data['tags'].head())

# we want to filter on the tags, so let's make them separate columns 
champ_data[['primary type', 'secondary type']] = champ_data['tags'].apply(lambda x: pd.Series(x) if isinstance(x, list) else pd.Series([x, None]))
# print(champ_data.head())


#%% now get the ADCs
adc_data = champ_data[champ_data['primary type'] == 'Marksman']

# order by decreasing attack range
adc_data= adc_data.sort_values(by = 'stats.attackrange', ascending = False) #organize into leaderboard
adc_data.reset_index(drop=True, inplace=True) #reset index to match order

print(adc_data[['id','stats.attackrange']].head(3))
print('\n', adc_data[['id','stats.attackrange']].tail(3))