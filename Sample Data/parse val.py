# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 10:37:54 2024

@author: 417-DevOps
"""
import pandas as pd
import json

#parse very large valorant info from https://stelar7.no/valorant/eu/1641207119.json
with open('VALORANT_match.json', encoding='utf8') as json_data:
    data= json.load(json_data)
    val_match_data = pd.DataFrame(data['matches'])
    del data


print(list(val_match_data)) #match info

val_match_data= val_match_data.head(1)
val_match_data.to_json('val-match-v1 match data example.json')

