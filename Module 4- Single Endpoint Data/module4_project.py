# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:15:55 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 4 project (account info + match history)
"""
##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher #'pip install riotwatcher' in Anaconda prompt
from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
import os


##--------- LOAD CONFIG DATA ---------##
# You can replace this with your API key, I just keep mine outside of repo directory
load_dotenv('../../config.env')
api_key = os.environ['DEV_KEY'] 

lol_watcher = LolWatcher(api_key) #Tell Riot Watcher to use LoL functions with the API key


##--------- SET PLAYER PARAMETERS ---------##
player_name= 'RebirthNA'
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'americas'


##--------- CREATE PLAYER OBJECT ---------##
# This is equivalent to going to /riot/account/v1/accounts/by-riot-id/
summoner= lol_watcher.summoner.by_name(player_region, player_name)
print('Player info= \n',summoner)


##--------- GET MATCH HISTORY ---------##
# Here's where Riot uses the Puuid!
# Same as going to /lol/match/v5/matches/by-puuid/{puuid}/ids
num_matches_data= 20
match_history= lol_watcher.match.matchlist_by_puuid(region= player_routing, puuid= summoner['puuid'],
                                                    queue= 420, 
                                                    start=0, count= num_matches_data)
print('\nMatch history IDs= \n',match_history)