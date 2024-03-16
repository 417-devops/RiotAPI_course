import requests
from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
import os

# Define player info
game_name = 'RebirthNA'
tagline = 'NA1'
load_dotenv('../../../config.env') #keeps API outside of repo
api_key = os.environ['DEV_KEY'] 
region= 'americas'

# Construct the API URL for puuid via endpoint= /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}
url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}?api_key={api_key}"
# Send the request and retrieve puuid
response = requests.get(url)
player_puuid = response.json()['puuid']

print(player_puuid)

# Construct the API URL for champion mastery data via endpoint= /lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}
url = f"https://{tagline}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{player_puuid}?api_key={api_key}"
# Send the request and return the data
response = requests.get(url)
champ_mastery_data = response.json()[0]

print(champ_mastery_data)