"""
Desc: Pull recent match data using Cass

====================  IMPORTANT ==================== 
It looks like as of Sept 2025, Cassiopeia is broken. There is no fix because no one has updated the library (see https://github.com/meraki-analytics/cassiopeia/issues/468)
I have left the code as is, but it will not work until the library is updated. Notably the Feb 2026 commit did not fix the issue (see https://github.com/meraki-analytics/cassiopeia/commit/b01c3da4d4bd4f4ce777072af7c7ad1124c14446)

I strongly recommend using Riot Watcher for now as it is actively maintained and has a much larger user base, which means issues are more likely to be fixed in a timely manner.

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