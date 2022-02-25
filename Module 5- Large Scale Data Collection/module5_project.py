# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 20:17:14 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 5 project (challenger ladder roles)
"""
#%% ##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher #'pip install riotwatcher' in Anaconda prompt
from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def setup_env():
    load_dotenv('../../../config.env')
    api_key = os.environ['DEV_KEY'] 

    lol_watcher = LolWatcher(api_key) #Tell Riot Watcher to use LoL functions with the API key
    del(api_key)
    
    return lol_watcher

def get_match_history(summonerName, player_region):
    match_history= lol_watcher.match.matchlist_by_puuid(region= player_routing, puuid= summoner['puuid'],
                                                    queue= 420, 
                                                    start=0, count= 2)
    return match_history
    
def get_time(matchID, player_routing):
    game_time= lol_watcher.match.by_id(region= player_routing, match_id= matchID)['info']['gameDuration']
    return game_time

#%% MAIN CODE
lol_watcher= setup_env()


# Get challenger players
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'americas'
queue_type= 'RANKED_SOLO_5x5' #RANKED_SOLO_5x5, RANKED_FLEX_SR, 

challenger_players= pd.DataFrame.from_dict(lol_watcher.league.challenger_by_queue(region= player_region, 
                                                          queue=queue_type)['entries']) 
challenger_players= challenger_players.sort_values(by = 'leaguePoints', ascending = False) #organize into leaderboard
challenger_players.reset_index(drop=True, inplace=True) #reset index to match order
summoner_names= challenger_players['summonerName'].tolist()

chall_game_times=[]
for i in range (0,50):
    summonerName= summoner_names[i]
    summoner= lol_watcher.summoner.by_name(player_region, summonerName)
    match_history= get_match_history(summonerName, player_region)
    
    game_time_list= []
    for matchID in match_history:
        try:
            game_time= get_time(matchID, player_routing)
            game_time_list.append(game_time)
        except:
            pass
    
    avg_game_time= np.mean(game_time_list)
    chall_game_times.append(avg_game_time)
    print(summonerName, 'has average game time of', avg_game_time)

plt.scatter(np.linspace(0,len(chall_game_times),len(chall_game_times)), chall_game_times )
plt.xlabel('Ranking')
plt.ylabel('Average game time')
