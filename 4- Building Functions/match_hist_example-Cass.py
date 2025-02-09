"""
LAST MODIFIED: 2025-02-09

@author: 417-DevOps
Desc: Pull recent match data using Cass
"""

#%%--------- LOAD LIBRARIES ---------##
import cassiopeia as cass
from dotenv import dotenv_values

#%%--------- LOAD CONFIG DATA ---------##
cass.set_riot_api_key(dotenv_values("../config.env")['DEV_KEY'])  #may need to modify where this file is located, so check the file path
region= 'americas'

#%%--------- CREATE PLAYER OBJECT ---------##
player_accoutInfo = cass.Account(name="RebirthNA", tagline="NA1", region="NA").load() #general Riot account, see https://cassiopeia.readthedocs.io/en/latest/cassiopeia/account.html
summoner= cass.Summoner(puuid=player_accoutInfo.puuid, region="NA").load() #LoL specific account, see https://cassiopeia.readthedocs.io/en/latest/cassiopeia/summoner.html
print('\nPlayer info= ',summoner)

#%%--------- Get a list of past matches ---------##
match_history = summoner.match_history #see https://cassiopeia.readthedocs.io/en/latest/cassiopeia/match.html#cassiopeia.cassiopeia.Summoner.match_history
print('\nLast matchIDs= ', match_history[0]) #match_history[0] is the last match played