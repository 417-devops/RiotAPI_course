# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 19:12:12 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 5-2 example (functions)
"""

#%% ##--------- LOAD LIBRARIES ---------##
from module5_example2_setup import setup_env
from module5_example2_matchHistory import get_match_list
from module5_example2_gameDuration import get_game_duration

#%% MAIN CODE
##--------- LOAD ENV SETTINGS ---------##
env_file= '../../config.env'    
lol_watcher= setup_env(env_file)


##--------- SET PLAYER PARAMETERS ---------##
player_name= 'RebirthNA'
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'americas'


##--------- LOAD THE PLAYER DATA AS CLASS ---------##
#Relevant libraries are already loaded! 
summoner= lol_watcher.summoner.by_name(player_region, player_name)
print(summoner)


##--------- GET MATCH HISTORY ---------##
num_matches= 2
match_history= get_match_list(summoner, num_matches, player_routing, lol_watcher)


##--------- GET GAME DURATIONS ---------##
for matchID in match_history:
    game_time= get_game_duration(matchID, player_routing, lol_watcher)
    print('Match', matchID, 'lasted',game_time, 'seconds')