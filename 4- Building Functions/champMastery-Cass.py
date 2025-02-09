"""
LAST MODIFIED: 2025-02-09

@author: 417-DevOps
Desc: Get account info, then pull champ mastery data
Riot Watcher version of champ_mastery.py
"""

import cassiopeia as cass
#from dotenv import load_dotenv
#import os
from dotenv import dotenv_values


#%% Load the API key from the .env file
#load_dotenv('../../../config.env') #keeps API outside of repo
#cass.set_riot_api_key(os.environ['DEV_KEY'])
cass.set_riot_api_key(dotenv_values("../config.env")['DEV_KEY'])  #may need to modify where this file is located, so check the file path
region= 'americas'

#%% Get the puuid to make any calls referencing the player
#summoner = cass.get_summoner(name="RebirthNA", region="NA").load() #changed when Riot switched API calles to taglines 
player_accoutInfo = cass.Account(name="RebirthNA", tagline="NA1", region="NA").load() #load forces all attributes to load vs. lazy loading (which only loads puuid)
print('\n', player_accoutInfo)

#%% Now we want to know the details of the player
# typically you would do this, but the prior account info is more broad as it is used for all Riot games, vs. the summoner endpoint which is just for LoL
a_summoner= cass.Summoner(puuid=player_accoutInfo.puuid, region="NA").load()
#a_summoner = cass.get_summoner(puuid=player_accoutInfo.puuid, region="NA").load() #alt. method of above
print('\n', a_summoner)


#%% Now we can load things like the match history
# see https://cassiopeia.readthedocs.io/en/latest/cassiopeia/summoner.html
print('\n', a_summoner.match_history[0])

# or other data, like the name + level + region
print("\n{name} is a level {level} summoner on the {region} server.".format(name=a_summoner.account.name,
                                                                          level=a_summoner.level,
                                                                          region=a_summoner.region))

#%% The a_summoner is an instance of the cassiopeia.Summoner class which has many attributes
# The example from the docs walks through this, though I have added explanations
kalturi = cass.Account(name="Kalturi", tagline="NA1", region="NA").summoner #this creates the summoner object
print('\n',kalturi) #view the summoner object, you'd have to call .load() to get all the attributes

# now lets use one "ChampionMasteries" which of the methods associated with the summoner object 
#.champion_materies calls get_champion_masteries, but because you are calling it on kalturi (summoner), it simply returns a class cass.ChampionMasteries
# .filter is a method of cass.ChampionMasteries, which is a list of cass.ChampionMastery objects
good_with = kalturi.champion_masteries.filter(lambda cm: cm.level >= 6) #returns a list of champions greater than mastery level 6
print([cm.champion.name for cm in good_with]) #iterate over the list of items from above and print the name 
