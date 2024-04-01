# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 20:33:34 2024

@author: 417-DevOps
1) get challenger player list
2) basic data manipulation of challenger list data
3) get account info of a challenger player
4) get match history of that player
5) find out how much gold they earned in their last game
"""

#%% ##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher 
from dotenv import load_dotenv 
import os
import pandas as pd

def setup_env():
    load_dotenv('../../config.env') #may need to modify where this file is
    API_KEY = os.environ['DEV_KEY'] 

    lol_watcher = LolWatcher(API_KEY) #Tell Riot Watcher to use LoL functions with the API key
    del(API_KEY) #remove the API_KEY from env variables
    return lol_watcher

def total_games(player_info):
    total_games= (player_info['wins']+ player_info['losses'])
    return total_games

def get_player_match_data(matchID, player):
    match_data= lol_watcher.match.by_id(region= 'na1', match_id= matchID)['info']['participants']
    # now get the data of that player
    for participant in match_data:
        if participant['summonerName'] == player['name']:
            return participant['goldEarned']
        else:
            pass

#%%--------- LOAD CONFIG DATA ---------##
lol_watcher= setup_env()


#%%--------- GET THE RAW DATA ---------##
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
queue_type= 'RANKED_SOLO_5x5' #RANKED_SOLO_5x5, RANKED_FLEX_SR, 

challenger_ladder= lol_watcher.league.challenger_by_queue(region= player_region, 
                                                          queue=queue_type)
raw_data= pd.DataFrame.from_dict(challenger_ladder) #convert the challenger info to dataframe
# print(raw_data.head())
# print('Fields= ', list(raw_data))

#%%--------- EXTRACT RELEVANT DATA ---------##
challenger_players= pd.DataFrame.from_dict(challenger_ladder['entries']) #we only really care about the entries
# print(challenger_players.head())
# print('Fields= ', list(challenger_players))

challenger_players= challenger_players.sort_values(by = 'leaguePoints', ascending = False) #organize into leaderboard
challenger_players.reset_index(drop=True, inplace=True) #reset index to match order
print('\n', challenger_players[['summonerName','leaguePoints']].head())

#%%--------- Comparing the top and bottom challengers ---------##
num1_player= challenger_players.iloc[0]
bottom_chall= challenger_players.iloc[-1]

#create function to analyze player (total games)
games_num1= total_games(num1_player)
games_numN= total_games(bottom_chall)
print('\n#1 player: ', num1_player['summonerName'], 'has played', games_num1, 'games')
print('Bottom player: ', bottom_chall['summonerName'], 'has played', games_numN, 'games')


#%%--------- Check their recent game stats ---------##
player= lol_watcher.summoner.by_name(region= player_region, summoner_name= num1_player['summonerName'])
last_match_id= lol_watcher.match.matchlist_by_puuid(region= player_region, puuid= player['puuid'], count= 1)[0]

gold_earned= get_player_match_data(last_match_id, player)
print(f"{player['name']} earned {gold_earned} gold in their last game.")