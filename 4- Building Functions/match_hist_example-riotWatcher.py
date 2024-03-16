# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 

@author: 417-DevOps
Desc: Pull recent match data using Riot Watcher
"""

#%%--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher #'pip install riotwatcher' in Anaconda prompt
from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
import os


#%%--------- LOAD CONFIG DATA ---------##
load_dotenv('../../../config.env') #keeps API outside of repo
api_key = os.environ['DEV_KEY'] 
# api_key = 'YOUR_API_KEY' #alternatively, test with your key here

lol_watcher = LolWatcher(api_key) #Tell Riot Watcher to use LoL functions with the API key


#%%--------- SET PLAYER PARAMETERS ---------##
player_name= 'RebirthNA'.lower()
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'americas'


#%%--------- CREATE PLAYER OBJECT ---------##
# This is equivalent to going to /riot/account/v1/accounts/by-riot-id/
summoner= lol_watcher.summoner.by_name(player_region, player_name)
#summoner= lol_watcher.summoner.by_name(region= 'NA1', summoner_name= 'RebirthNA')
print('Player info= \n',summoner)


#%%--------- Get a list of past matches ---------##
matchlist= lol_watcher.match.matchlist_by_puuid(region= player_region, puuid= summoner['puuid'])
print('Recent matchID=\n', matchlist)
