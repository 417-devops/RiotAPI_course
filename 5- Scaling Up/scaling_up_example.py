"""
LAST MODIFIED: 2025-02-09

@author: 417-DevOps
1) get challenger player list
2) basic data manipulation of challenger list data
3) get account info of a challenger player
4) get match history of that player
5) find out how much gold they earned in their last game
"""

#%% ##--------- LOAD LIBRARIES ---------##
from riotwatcher import RiotWatcher, LolWatcher 
from dotenv import dotenv_values
import pandas as pd

def setup_env():
    '''Load the API keys from the config file''' #this is called a docstring and will show in some editors when you start typing the function name
    api_key = dotenv_values("../../config.env")['DEV_KEY']
    lol_watcher = LolWatcher(api_key) #for league of legends specific calls
    riot_watcher = RiotWatcher(api_key) #for all Riot games
    
    return lol_watcher, riot_watcher


def total_games(player_info):
    '''Calculate the total number of games played by a player'''
    total_games= (player_info['wins']+ player_info['losses'])
    return total_games


def get_player_match_data(matchID, player_puuid):
    '''Get the gold earned by a player in a specific match.
    You can read what is in the match data via the Riot API documentation: https://developer.riotgames.com/apis#match-v5/GET_getMatch
    '''
    match_data= lol_watcher.match.by_id(region= 'na1', match_id= matchID)['info']['participants']
    #lol_watcher.match.by_id() returns match DTO (see Riot API docs above)
    #lol_watcher.match.by_id()[participants] returns a list of participants in the match by their PUUID (i.e. player1: puuid1, player2: puuid2, etc.)
    #similarly, lol_watcher.match.by_id()['info']['participants'][0] has the participants data (by index, mapping to the number listed in lol_watcher.match.by_id()[participants])

    # now get the data of that player
    for participant in match_data:
        if participant['puuid'] == player_puuid: #once we find the player, we can return the gold earned
            return participant['goldEarned']
        else:
            pass
    

#%%--------- LOAD CONFIG DATA ---------##
lol_watcher, riot_watcher= setup_env() #load in the API keys


#%%--------- GET THE RAW DATA ---------##
player_region= 'NA1'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
queue_type= 'RANKED_SOLO_5x5' #acceptable parameters are [RANKED_SOLO_5x5, RANKED_FLEX_SR, RANKED_FLEX_TT], see https://developer.riotgames.com/apis#league-v4/GET_getChallengerLeague
#for gamemode list see: https://static.developer.riotgames.com/docs/lol/gameModes.json

#now lets get the challenger ladder, see https://riot-watcher.readthedocs.io/en/latest/riotwatcher/LeagueOfLegends/LeagueApiV4.html?highlight=ranked_solo_5x5#riotwatcher._apis.league_of_legends.LeagueApiV4.challenger_by_queue
challenger_ladder= lol_watcher.league.challenger_by_queue(region= player_region, queue=queue_type) #returns LeagueListDTO

# What is in challenger_ladder? you can read the info on https://developer.riotgames.com/apis#league-v4/GET_getChallengerLeague
# OR we can clean up the data by converting to a dataframe as we eventually want to work with it!
raw_data= pd.DataFrame.from_dict(challenger_ladder) 
print(raw_data.head()) #print the first few rows to see what the data looks like
print('Fields= ', list(raw_data)) 

#print(challenger_ladder['entries'][0]) # I.e. originally we would have to guess what the first player on the challenger ladder is
#print(raw_data['entries'][0]) # But now we can see the various attributes of challenger_ladder and more easily manage the data


#%%--------- EXTRACT RELEVANT DATA ---------##
challenger_players= pd.DataFrame.from_dict(challenger_ladder['entries']) #we only really care about the entries
print(challenger_players.head()) #uncomment these lines if you want to take a peak at the data!
print('Fields= ', list(challenger_players))

#just in case the data is not organized, let's sort it by leaguePoints (LP)
challenger_players= challenger_players.sort_values(by = 'leaguePoints', ascending = False) 
challenger_players.reset_index(drop=True, inplace=True) #reset index to match order


#%%--------- Comparing the top and bottom challengers ---------##
num1_player= challenger_players.iloc[0]
bottom_chall= challenger_players.iloc[-1]

#create function to analyze player (total games)
games_num1= total_games(num1_player)
games_numN= total_games(bottom_chall)

#note that the data only contains puuid's so we would need to make a second call to get their actual in-game names
#OR visit https://developer.riotgames.com/apis#account-v1/GET_getByPuuid and put in lol_watcher.summoner.by_id(region= player_region, encrypted_summoner_id= num1_player['summonerId'])['puuid']

print('\n#1 player: ', num1_player['puuid'], 'has played', games_num1, 'games')
print('Bottom player: ', bottom_chall['puuid'], 'has played', games_numN, 'games', '\n')

#you could get the names by 1) getting the PUUID, then 2) getting the game name
#backmap_PUUID= lol_watcher.summoner.by_id(region= player_region, encrypted_summoner_id= num1_player['summonerId'])['puuid']
#riot_watcher.account.by_puuid(player_routing, backmap_PUUID) #this is how to do puuid -> 'gameName' and 'tagLine' for the player


#%%--------- Now lets check a stat from the #1 player's last match ---------##
# to get match history, we need the player's puuid
# see docs: https://riot-watcher.readthedocs.io/en/latest/riotwatcher/LeagueOfLegends/MatchApiV5.html#riotwatcher._apis.league_of_legends.MatchApiV5

no1Player_puuid= num1_player['puuid']
#no1Player_puuid= lol_watcher.summoner.by_puuid(player_region, num1_player['puuid'])#get the puuid
last_match_id= lol_watcher.match.matchlist_by_puuid(region= player_region, puuid= no1Player_puuid)[0] #now return the match ID of the last game


# lets make a quick function to get the gold earned
gold_earned= get_player_match_data(matchID= last_match_id, player_puuid= no1Player_puuid)
print(f"The no.1 challenger player earned {gold_earned} gold in their last game.") 

# we could continue the above process for multiple matches if we wanted
matchlist= lol_watcher.match.matchlist_by_puuid(region= player_region, puuid= no1Player_puuid)
print('Last 3 matchIDs matchIDs= ', matchlist[0:3]) #latest match is matchlist[0]
# %%
