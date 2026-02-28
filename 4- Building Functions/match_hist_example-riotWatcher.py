"""
LAST MODIFIED: 2025-02-09

@author: 417-DevOps
Desc: Pull recent match data using Riot Watcher
"""

#%%--------- LOAD LIBRARIES ---------##
from riotwatcher import RiotWatcher, LolWatcher 
from dotenv import dotenv_values


#%%--------- LOAD CONFIG DATA ---------##
api_key = dotenv_values("../../config.env")['DEV_KEY']
#api_key = 'RGAPI-x-x-x-x-x' #alternatively, test with your key here

#apply API key to various methods
lol_watcher = LolWatcher(api_key) #for league of legends specific calls
riot_watcher = RiotWatcher(api_key) #for all Riot games


#--------- SET PLAYER PARAMETERS ---------##
player_name= 'RebirthNA'.lower()
player_tagline= 'na1'
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'americas'


#%%--------- CREATE PLAYER OBJECT ---------##
# This is equivalent to going to /riot/account/v1/accounts/by-riot-id/
player_account = riot_watcher.account.by_riot_id(player_routing, player_name, player_tagline) #https://riot-watcher.readthedocs.io/en/latest/riotwatcher/Riot/AccountApi.html?highlight=account#riotwatcher._apis.riot.AccountApi.by_riot_id

#And this is equivalent to going to https://developer.riotgames.com/apis#summoner-v4
lol_account = lol_watcher.summoner.by_puuid(player_region, player_account['puuid'])


#%%--------- Get a list of past matches ---------##
matchlist= lol_watcher.match.matchlist_by_puuid(region= player_region, puuid= lol_account['puuid'])
print('Last 3 matchIDs matchIDs= ', matchlist[0:3]) #latest match is matchlist[0]

# %%
