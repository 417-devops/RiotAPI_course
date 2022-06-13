# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 19:12:12 2022

Author: 417-DevOps
Desc: Riot API Bootcamp Module 5-2 example (functions)
SETUP FILE 
"""

#%% ##--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher #'pip install riotwatcher' in Anaconda prompt
from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
import os

def setup_env(env_file_location):
    load_dotenv(env_file_location)
    api_key = os.environ['DEV_KEY'] 

    lol_watcher = LolWatcher(api_key) #Tell Riot Watcher to use LoL functions with the API key
    del(api_key)
    
    return lol_watcher


#%% MAIN CODE
if __name__ == "__main__": #read more at https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    env_file= '../../config.env'    
    lol_watcher= setup_env(env_file)
    print('Loaded ', lol_watcher)