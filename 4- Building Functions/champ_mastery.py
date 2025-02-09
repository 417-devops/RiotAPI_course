"""
LAST MODIFIED: 2025-02-09

@author: 417-DevOps
Desc: Get account info, then pull champ mastery data
Base version by making a web request
"""

import requests
#from dotenv import load_dotenv
#import os
from dotenv import dotenv_values  #'pip install python-dotenv' in Anaconda prompt


## Define player info
game_name = 'RebirthNA'
tagline = 'NA1'

## Load the API key from the .env file
# load_dotenv('../../../config.env') #keeps API outside of repo, you may need to modify the filepath
# api_key = os.environ['DEV_KEY'] 
api_key = dotenv_values("../config.env")['DEV_KEY']  #may need to modify where this file is located, so check the file path
region= 'americas'

## Construct the API URL for puuid via endpoint= /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}
url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}?api_key={api_key}"

## Send the request and retrieve puuid
response = requests.get(url)
player_puuid = response.json()['puuid']
print('Player puuid=', player_puuid)

## Construct the API URL for champion mastery data via endpoint= /lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}
url = f"https://{tagline}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{player_puuid}?api_key={api_key}"
# Send the request and return the data
response = requests.get(url)
champ_mastery_data = response.json()[0]

print('Player champion mastery data=', champ_mastery_data)
print() #for spacing after output to improve readability