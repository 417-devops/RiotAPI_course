# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:47:19 2024

@author: 417-DevOps
Desc: Get account info, then pull champ mastery data
Cass version (BROKEN)
"""

import cassiopeia as cass
from dotenv import load_dotenv
import os

load_dotenv('../../../config.env') #keeps API outside of repo
cass.set_riot_api_key(os.environ['DEV_KEY'])
# cass.set_riot_api_key('YOUR_API_KEY')  

summoner = cass.get_summoner(name="RebirthNA", region="NA").load()
print('Player info= \n',summoner)
print("\n{name} is a level {level} summoner on the {region} server.".format(name=summoner.name,
                                                                          level=summoner.level,
                                                                          region=summoner.region))
# from the docs
kalturi = cass.Summoner(name="Kalturi", region= 'NA')
good_with = kalturi.champion_masteries.filter(lambda cm: cm.level >= 6)
print([cm.champion.name for cm in good_with])

#champion masteries are broken
print(summoner.champion_masteries())
print(cass.get_champion_masteries(summoner=summoner,region='NA'))