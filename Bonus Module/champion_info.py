# -*- coding: utf-8 -*-
"""
Created on Sun May  1 14:02:49 2022

Author: 417-DevOps
Desc: Extract champion data
"""
from riotwatcher import LolWatcher

from dotenv import load_dotenv
import os

#%% --------- LOAD CONFIG DATA ---------##
load_dotenv('../../../config.env')
api_key = os.environ['DEV_KEY']
lol_watcher = LolWatcher(api_key) #replace with API key
del api_key

#%% --------- Get the Champion information ---------##
region = 'na1' #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]
# note that for Ddragon, eun1->eune; oc1->oce

# First we get the latest version of the game from data dragon
versions = lol_watcher.data_dragon.versions_for_region(region)
# print(versions)
champions_version = versions['n']['champion'] #want the champion info

# Extract the specific info for champions
current_champ_list = lol_watcher.data_dragon.champions(champions_version)['data']
test_champ= current_champ_list['Aatrox']
# print(test_champ)

# Get all the tanks
tanks = [x for x in current_champ_list 
         if 'Tank' in current_champ_list[x]['tags']]
# print(tanks)

#%% --------- Pull out the key values ---------##
#usually we want the stats of the champion (movespeed, hp, etc)
champ_stats= test_champ['stats']
# print(test_champ['id'],'has', champ_stats['hp'], 'HP at level 1')


#%% --------- What about abilities and scaling? ---------##
# Riot API has some, but they're broken (see vars and aN/fN in documentation https://developer.riotgames.com/docs/lol)
full_champ_data= lol_watcher.data_dragon.champions(champions_version, full= True)['data']
test_champ= full_champ_data['Aatrox']
# print(test_champ)
print(test_champ['spells'][1]) #q/w/e/r

# note that actual damage values and scalings are not provided by the Riot api
# recommend the following sources:
# https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions/Annie.json
# https://www.communitydragon.org/