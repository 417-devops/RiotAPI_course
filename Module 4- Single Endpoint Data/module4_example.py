# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 16:49:53 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 4 example (Request challenger ladder, look at entries)
"""

#%% ##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher #'pip install riotwatcher' in Anaconda prompt
from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
import os
import pandas as pd

def total_games(player_info):
    total_games= (player_info['wins']+ player_info['losses'])
    return total_games

def setup_env():
    load_dotenv('../../config.env')
    api_key = os.environ['DEV_KEY'] 

    lol_watcher = LolWatcher(api_key) #Tell Riot Watcher to use LoL functions with the API key
    del(api_key)
    return lol_watcher


#%% MAIN CODE

##--------- LOAD CONFIG DATA ---------##
lol_watcher= setup_env()


##--------- GET THE RAW DATA ---------##
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
queue_type= 'RANKED_SOLO_5x5' #RANKED_SOLO_5x5, RANKED_FLEX_SR, 
challenger_ladder= lol_watcher.league.challenger_by_queue(region= player_region, 
                                                          queue=queue_type)

raw_data= pd.DataFrame.from_dict(challenger_ladder) #convert the challenger info to dataframe
print(raw_data.head())
print('Fields= ', list(raw_data))


##--------- EXTRACT RELEVANT DATA ---------##
print('\nENTRIES= \n', challenger_ladder['entries'][0:3])
challenger_players= pd.DataFrame.from_dict(challenger_ladder['entries']) #we only really care about the entried
print(challenger_players.head())
print('Fields= ', list(challenger_players))


##--------- CLEAN UP DATA ---------##
print('\n', challenger_players[['summonerName','leaguePoints']].head()) #run this a couple times, note un-ordered

challenger_players= challenger_players.sort_values(by = 'leaguePoints', ascending = False) #organize into leaderboard
challenger_players.reset_index(drop=True, inplace=True) #reset index to match order
print('\n', challenger_players[['summonerName','leaguePoints']].head())


##--------- LOOKING AT A SPECIFIC PLAYER ---------##
# Instead of adding columns, we only want to work with a single element -> convert to dict
num1_player= challenger_players.loc[challenger_players['summonerName'] == 'Kral Closer'].to_dict('records')[0]
n_player_name= challenger_players.iloc[50]['summonerName']
n_player= challenger_players.loc[challenger_players['summonerName'] == n_player_name].to_dict('records')[0]

#create function to analyze player (total games)
games_num1= total_games(num1_player)
games_numN= total_games(n_player)
print('\n#1 player: ', num1_player['summonerName'], 'has played', games_num1, 'games')
print('#50 player: ', n_player['summonerName'], 'has played', games_numN, 'games')