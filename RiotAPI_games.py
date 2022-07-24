# -*- coding: utf-8 -*-
"""
Author: 417-DevOps
Desc: compare LoL and TFT code for Riot API calls
"""

from riotwatcher import LolWatcher, TftWatcher

from dotenv import load_dotenv
import os

#%% --------- LOAD CONFIG DATA ---------##
load_dotenv('../../config.env')
api_key = os.environ['DEV_KEY']
lol_watcher = LolWatcher(api_key) #replace with API key
tft_watcher= TftWatcher(api_key)
del api_key

player_name= 'RebirthNA'
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'americas'

summoner_lol= lol_watcher.summoner.by_name(player_region, player_name)
print('LoL: \n', summoner_lol)
print()

summoner_tft= tft_watcher.summoner.by_name(player_region, player_name)
print('TFT: \n', summoner_tft)

print('\nSame info? ',summoner_lol==summoner_tft)