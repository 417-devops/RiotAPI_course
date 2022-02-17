# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 18:54:13 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 5-1 example (memory usage)
"""

#%% ##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher #'pip install riotwatcher' in Anaconda prompt
from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
import os

from sys import getsizeof

def setup_env():
    load_dotenv('../../config.env')
    api_key = os.environ['DEV_KEY'] 

    lol_watcher = LolWatcher(api_key) #Tell Riot Watcher to use LoL functions with the API key
    del(api_key)
    
    return lol_watcher


#%% MAIN CODE
lol_watcher= setup_env()

##--------- SET PLAYER PARAMETERS ---------##
player_name= 'RebirthNA'
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'americas'


##--------- LOAD THE PLAYER DATA AS CLASS ---------##
summoner= lol_watcher.summoner.by_name(player_region, player_name)
match_history= lol_watcher.match.matchlist_by_puuid(region= player_routing, puuid= summoner['puuid'],
                                                    queue= 420, 
                                                    start=0, count= 1)
matchID= match_history[0]


match_data_big= lol_watcher.match.by_id(region= player_routing, match_id= matchID)
game_time= match_data_big['info']['gameDuration']
print('Basic game duration size [bytes]= ', getsizeof(match_data_big)+getsizeof(game_time))


match_data_small= lol_watcher.match.by_id(region= player_routing, match_id= matchID)['info']['gameDuration']
print('More efficient method size [bytes]= ', getsizeof(match_data_small))


print('2nd method is', round(getsizeof(match_data_big)/getsizeof(match_data_small),2), 'times smaller')