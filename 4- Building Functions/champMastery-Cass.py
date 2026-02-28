"""
@author: 417-DevOps
Desc: Get account info, then pull champ mastery data
Riot Watcher version of champ_mastery.py
"""

import cassiopeia as cass # see https://github.com/meraki-analytics/cassiopeia
#from dotenv import load_dotenv
#import os
from dotenv import dotenv_values


#%% Load the API key from the .env file
#load_dotenv('../../../config.env') #keeps API outside of repo
#cass.set_riot_api_key(os.environ['DEV_KEY'])
dev_api_key= dotenv_values("../../config.env")['DEV_KEY'] #may need to modify where this file is located, so check the file path
cass.set_riot_api_key(dev_api_key)  
region= 'americas'

#%% Get the puuid to make any calls referencing the player
##summoner = cass.get_summoner(name="RebirthNA", region="NA").load() #changed when Riot switched API calles to taglines 
player_account = cass.get_account(name="RebirthNA", tagline="NA1", region="NA") #this is the more general account info, which is used for all Riot games, vs. the summoner endpoint which is just for LoL

#now lets get the LoL specific account info, which is used for all LoL specific calls, like match history, champion mastery, etc.
# https://cassiopeia.readthedocs.io/en/latest/cassiopeia/account.html#cassiopeia.Account.summoner
'''====================  IMPORTANT ==================== 
It looks like as of Sept 2025, Cassiopeia is broken. There is no fix because no one has updated the library (see https://github.com/meraki-analytics/cassiopeia/issues/468)
I have left the code as is, but it will not work until the library is updated. Notably the Feb 2026 commit did not fix the issue (see https://github.com/meraki-analytics/cassiopeia/commit/b01c3da4d4bd4f4ce777072af7c7ad1124c14446)

I strongly recommend using Riot Watcher for now as it is actively maintained and has a much larger user base, which means issues are more likely to be fixed in a timely manner.
'''


player_lol_acount= cass.get_summoner(name="RebirthNA", tagline="NA1", region="NA") #LoL specific account
print('\n', player_lol_acount)

#Now we want to know the details of the player
# typically you would do this, but the prior account info is more broad as it is used for all Riot games, vs. the summoner endpoint which is just for LoL
#print('\n', a_summoner.puuid)
# a_summoner is already loaded with all summoner details including puuid
#print('\n', a_summoner)


#Now we can load things like the match history
# see https://cassiopeia.readthedocs.io/en/latest/cassiopeia/summoner.html
print('\n', a_summoner.match_history[0])

# or other data, like the name + level + region
print("\n{name} is a level {level} summoner on the {region} server.".format(name=a_summoner.account.name,
                                                                          level=a_summoner.level,
                                                                          region=a_summoner.region))

#The a_summoner is an instance of the cassiopeia.Summoner class which has many attributes
# The example from the docs walks through this, though I have added explanations
kalturi = cass.Account(name="Kalturi", tagline="NA1", region="NA").summoner #this creates the summoner object
print('\n',kalturi) #view the summoner object, you'd have to call .load() to get all the attributes

# now lets use one "ChampionMasteries" which of the methods associated with the summoner object 
#.champion_materies calls get_champion_masteries, but because you are calling it on kalturi (summoner), it simply returns a class cass.ChampionMasteries
# .filter is a method of cass.ChampionMasteries, which is a list of cass.ChampionMastery objects
good_with = kalturi.champion_masteries.filter(lambda cm: cm.level >= 6) #returns a list of champions greater than mastery level 6
print([cm.champion.name for cm in good_with]) #iterate over the list of items from above and print the name 
