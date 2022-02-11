# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:15:55 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 4 example (getting match history)
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


##--------- GET MATCH HISTORY ---------##
# Here's where Riot uses the Puuid!
# Same as going to /lol/match/v5/matches/by-puuid/{puuid}/ids
puuid= 'b-zNFgYAT2sxjwn6483-dpbjI_hIcwKmEiTnZPv4UMaOlg-EzeCuXUJLC-AFXSfExhq_mx-dVqHnWg'
player_routing= 'americas'
num_matches_data= 20
match_history= lol_watcher.match.matchlist_by_puuid(region= player_routing, puuid= puuid,
                                                    queue= 420, 
                                                    start=0, count= num_matches_data)
print('\nMatch history IDs= \n',match_history)
