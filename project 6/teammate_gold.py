# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 11:55:45 2024

@author: 417-DevOps
PURPOSE: get teammates' current gold
"""
import requests
import json
import sys, warnings, time
import pandas as pd
import datetime

#%% FUNCTIONS
def kbhit(): #will use this to detect key press
    if sys.platform.startswith('win'):
        import msvcrt
        return msvcrt.kbhit()
    else:
        import select
        return select.select([sys.stdin], [], [], 0)[0]

def get_allgamedata(url):
    warnings.simplefilter("ignore")  # to suppress the warnings about insecure network request
    try:
        response = requests.get(url, verify=False)  # Ignore SSL certificate errors
        allgamedata = response.json()
        return allgamedata
    except requests.exceptions.RequestException as e:
        print("Error making request:", e)
    except KeyError:
        print("Unable to retrieve current gold value from the response.")

def parse_allgamedata(allgamedata):
    # You could also make calls by player to URLs, but I think parsing is probably faster
    # ex= ​https://127.0.0.1:2999/liveclientdata/playerscores?summonerName=
    
    activePlayer= allgamedata['activePlayer']
    allPlayers= allgamedata['allPlayers']
    events= allgamedata['events']
    gameData= allgamedata['gameData']
    
    return activePlayer, allPlayers, events, gameData

def calc_passiveGold(gameData):
    #current game time is in seconds
    # gold gen starts at 1:50, 20.4 per 10 -> 2.04 per sec
    passive_gold= (gameData['gameTime']-110)*2.04
    #need to account for starting gold
    passive_gold+=500
    return round(passive_gold,2)

def calc_minionValue(gameData):
    # 0-15min, avg is 19.8 per cs
    # 15-17:15, avg is 22.6
    # 17:15-25, avg is 23
    # 25+ min, avg is 27.6
    if gameData['gameTime'] < 15*60:
        minnion_value= 19.8
    elif gameData['gameTime'] >15*60 and gameData['gameTime'] < 17*60+15:
        minnion_value= 22.6
    elif gameData['gameTime'] > 17*60+15 and gameData['gameTime'] < 25*60:
        minnion_value= 23
    else:
        minnion_value= 27.6
    return minnion_value

def calc_supportPassiveGold(gameData):
    # world atlas is 3 per 10
    # all other is 5 per 10
    # we will keep it simple and assume 0.3 per sec
    support_gold= (gameData['gameTime']-110)*0.3
    return support_gold

def get_teammates(activePlayer,allPlayers):
    df= pd.DataFrame.from_dict(allPlayers, orient='columns')
    you_name= activePlayer['summonerName'].partition("#")[0] #activePlayer is name#tag but team is just name
    
    team_name= df[df['summonerName'] == you_name]['team'].iloc[0] #find what team you are on
    raw_team_data= df[df['team'] == team_name] #keep only team data
    
    raw_team_data= raw_team_data[['championName','items','position', 'scores', 'summonerName']] #retain relevant data
    return raw_team_data

def calc_teamGold(team_data, passive_gold, support_gold, minnion_value):
    team_data= pd.concat([team_data, pd.DataFrame(team_data['scores'].to_list())], axis=1)
    team_data['passiveGold']= passive_gold
    team_data['scoresGold']= team_data['kills']*300 + team_data['assists']*150 + team_data['creepScore']*minnion_value
    
    team_data['supportGold']= 0.0
    team_data.loc[team_data['position'].isin(['SUPPORT','UTILITY']), 'supportGold']= support_gold
    team_data= team_data.drop(['wardScore', 'scores'], axis=1)
    return team_data        

def calc_teamGoldItems(team_data):
    allplayeritems= team_data['items'].to_list()
    total_prices = [sum(item['price'] for item in entry) for entry in allplayeritems]
    team_data['itemGold']= total_prices
    
    return team_data

def calc_teamTotalGold(activePlayer, team_data):
    team_data['currentGold']= (team_data['passiveGold']+ team_data['scoresGold']+ team_data['supportGold']) -team_data['itemGold']
    
    #we already know our gold so replace that value
    you_name= activePlayer['summonerName'].partition("#")[0] 
    team_data.loc[team_data['summonerName'] == you_name, 'currentGold']= activePlayer['currentGold']
    team_data['currentGold']= round(team_data['currentGold'],2)
    
    #add flag on jungler income
    team_data.loc[team_data['position'] == 'JUNGLE', 'position']= '*'+ team_data.loc[team_data['position'] == 'JUNGLE', 'position']
    
    return team_data

def main(allgamedata):
    activePlayer, allPlayers, events, gameData= parse_allgamedata(allgamedata)

    passive_gold= calc_passiveGold(gameData)
    support_gold= calc_supportPassiveGold(gameData)
    minnion_value= calc_minionValue(gameData)

    raw_team_data= get_teammates(activePlayer,allPlayers)
    team_data= calc_teamGold(raw_team_data, passive_gold, support_gold, minnion_value)
    team_data= calc_teamGoldItems(team_data)

    team_data_gold= calc_teamTotalGold(activePlayer, team_data)
    print('Time= ', str(datetime.timedelta(seconds=round(gameData['gameTime'],2))))
    print(team_data_gold[['championName', 'position','currentGold']])
    
#%% MAIN CODE
if __name__ == '__main__':
    live_data= True
    # could also try to make the call and if it fails, fall back on file
    # try:
    #     url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
    #     allgamedata= get_allgamedata(url)
    #     # rest of code
    # except requests.exceptions.RequestException as e:
    #     #run from example file
        
    if live_data:
        print('Game is active...')
        while True:
            url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
            allgamedata= get_allgamedata(url)
            main(allgamedata)
            
            time.sleep(1)  # Wait [sec] before the next iteration

            # Check for keyboard input
            if kbhit():
                break
    else:
        allgamedata = json.load(open('allgamedata_example.json'))
        main(allgamedata)

