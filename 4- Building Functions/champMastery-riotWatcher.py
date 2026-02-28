"""
LAST MODIFIED: 2025-02-09

@author: 417-DevOps
Desc: Get account info, then pull champ mastery data
Riot Watcher version of champ_mastery.py
"""

#%%--------- LOAD LIBRARIES ---------##
#import riotwatcher as rw    #'pip install riotwatcher' in Anaconda prompt
from riotwatcher import LolWatcher, RiotWatcher, ApiError #alt if you want to just use LolWatcher instead of rw.X
#from dotenv import load_dotenv
#import os
from dotenv import dotenv_values


#%%--------- LOAD CONFIG DATA ---------##
# load_dotenv('../../../../config.env') #keeps API outside of repo
# api_key = os.environ['DEV_KEY']
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
# /lol/summoner/v4/summoners/by-puuid/{encryptedPUUID} is the way to get a summoner by PUUID, remnant of Riot API starting from LoL as the only game
# /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine} OR /riot/account/v1/accounts/by-puuid/{puuid} is the preferred way under the new Riot API (for all games)
# Lets do this the proper way by making a call to the Riot API accounts endpoint
player_account = riot_watcher.account.by_riot_id(player_routing, player_name, player_tagline) #https://riot-watcher.readthedocs.io/en/latest/riotwatcher/Riot/AccountApi.html?highlight=account#riotwatcher._apis.riot.AccountApi.by_riot_id
print('Riot account info= ', player_account) #see how this has general account info?

me = lol_watcher.summoner.by_puuid(player_region, player_account['puuid'])
#playerName_RiotAPI= riot_watcher.account.by_puuid(player_routing, player_account['puuid']) #this is how to do puuid -> 'gameName' and 'tagLine' for the player
print('LoL account info= ', me) #see how this has more specific LoL info (e.g. profileIconID, summonerLevel, etc.)?
#also notice how unlike cass, this loads all the attributes


#%%--------- Now get champ mastery ---------##
#first get champion_mastery from lol_watcher, see https://riot-watcher.readthedocs.io/en/latest/riotwatcher/LeagueOfLegends/index.html
#then we want to apply that method to the player we are looking at, see https://riot-watcher.readthedocs.io/en/latest/riotwatcher/LeagueOfLegends/ChampionMasteryApiV4.html

champ_mastery = lol_watcher.champion_mastery.by_puuid(player_region, me['puuid'])
print('\nHighest mastery champion data= ', champ_mastery[0])
#the above used to be champion_mastery.by_summoner, but that was deprecated in favor of by_puuid
#the docs are not updated as seen here at the link on line 45
#if you ever need to ID what methods are available, use print(dir(lol_watcher.champion_mastery)) to see all the methods available and replace what is in dir(~) as needed

# for reference, the Github for Riot Watcher gives this example to pull player attributes 
my_ranked_stats = lol_watcher.league.by_puuid(player_region, me['puuid'])
print(my_ranked_stats)
