# -*- coding: utf-8 -*-
"""
Created on Sun May  1 17:00:45 2022

Author: 417-DevOps
Desc: Extract item data
"""

from riotwatcher import LolWatcher

from dotenv import load_dotenv
import os

#%% --------- LOAD CONFIG DATA ---------##
load_dotenv('../../config.env')
api_key = os.environ['DEV_KEY']
lol_watcher = LolWatcher(api_key) #replace with API key
del api_key


#%% --------- Get the Item Data ---------##
region = 'na1' #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]
# note that for Ddragon, eun1->eune; oc1->oce

# First we get the latest version of the game from data dragon
versions = lol_watcher.data_dragon.versions_for_region(region)
item_ver = versions['n']['item'] #want the champion info

# Extract the item data
item_list = lol_watcher.data_dragon.items(item_ver)['data']


#%% --------- Looking at a specific item ---------##
item_list = lol_watcher.data_dragon.items(item_ver)['data']
# items are referred to by number, not name
boots= item_list['1001']
print(boots)

# what if we want to know the stats it modifies?
for stat_modified in boots['stats']:
    print(stat_modified)
