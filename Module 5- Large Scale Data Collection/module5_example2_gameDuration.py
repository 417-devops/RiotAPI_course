# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 19:21:27 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 5-2 example (functions)
MATCH INFORMATION FILE (game duration)
"""

#%% ##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher

from module5_example2_setup import setup_env
from module5_example2_matchHistory import get_match_list

def get_game_duration(matchID, player_routing, lol_watcher):
    game_time= lol_watcher.match.by_id(region= player_routing, match_id= matchID)['info']['gameDuration']
    
    return game_time


#%% MAIN CODE
if __name__ == "__main__": #read more at https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    env_file= '../../config.env'    
    lol_watcher= setup_env(env_file)
    
    player_name= 'RebirthNA'
    player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
    player_routing= 'americas'
    
    summoner= lol_watcher.summoner.by_name(player_region, player_name)
    
    num_matches= 2
    match_history= get_match_list(summoner, num_matches, player_routing, lol_watcher)
    
    print('Game times= ')
    for matchID in match_history:
        game_time= get_game_duration(matchID, player_routing, lol_watcher)
        print(game_time)