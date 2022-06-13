# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 19:17:11 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 5-2 example (functions)
MATCH HISTORY FILE
"""

#%% ##--------- LOAD LIBRARIES ---------##
from module5_example2_setup import setup_env

def get_match_list(summoner, num_matches, player_routing, lol_watcher):
    match_history= lol_watcher.match.matchlist_by_puuid(region= player_routing, puuid= summoner['puuid'],
                                                        queue= 420, start=0, count= num_matches)
    
    return match_history


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
    print(match_history)