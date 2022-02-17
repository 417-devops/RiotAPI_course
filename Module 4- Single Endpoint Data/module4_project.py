# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 17:50:21 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 4 project (request past games, determine gametime)
"""

#%% ##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher #'pip install riotwatcher' in Anaconda prompt
from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
import os

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
num_matches_data= 10
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'americas'

##--------- LOAD THE PLAYER DATA AS CLASS ---------##
summoner= lol_watcher.summoner.by_name(player_region, player_name)
match_history= lol_watcher.match.matchlist_by_puuid(region= player_routing, puuid= summoner['puuid'],
                                                    queue= 420, 
                                                    start=0, count= num_matches_data)

# See example file in folder for match data, info at
# https://developer.riotgames.com/apis#match-v5/GET_getMatch 
print('Game times= ')
for matchID in match_history:
    # explanation way
    match_data= lol_watcher.match.by_id(region= player_routing, match_id= matchID)
    game_time= match_data['info']['gameDuration']
    
    # better way to save memory
    match_data= lol_watcher.match.by_id(region= player_routing, match_id= matchID)['info']['gameDuration']
    print(game_time)