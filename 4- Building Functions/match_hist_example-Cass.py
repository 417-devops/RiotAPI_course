# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 

@author: 417-DevOps
Desc: Pull recent match data using Cass
"""

#%%--------- LOAD LIBRARIES ---------##
import cassiopeia as cass
from dotenv import load_dotenv
import os

#%%--------- LOAD CONFIG DATA ---------##
load_dotenv('../../../config.env') #keeps API outside of repo
cass.set_riot_api_key(os.environ['DEV_KEY'])
# cass.set_riot_api_key('YOUR_API_KEY')

#%%--------- CREATE PLAYER OBJECT ---------##
summoner= cass.Summoner(name="RebirthNA", region="NA").load() #force loading due to cass's lazy loading behavior
print('Player info= \n',summoner)

#%%--------- Get a list of past matches ---------##
match_history = summoner.match_history
print('\nRecent matchID=\n', match_history[0])