import requests
import time
import warnings
import sys

def kbhit():
    if sys.platform.startswith('win'):
        import msvcrt
        return msvcrt.kbhit()
    else:
        import select
        return select.select([sys.stdin], [], [], 0)[0]

def get_current_gold():
    url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
    while True:
        warnings.simplefilter("ignore")  # to suppress the warnings about insecure network request
        try:
            response = requests.get(url, verify=False)  # Ignore SSL certificate errors
            data = response.json()
            currentGold = data['activePlayer']['currentGold']
            print(f"{data['activePlayer']['summonerName']} currently has {round(currentGold, 2)}g at {round(data['gameData']['gameTime'], 2)} seconds")
        except requests.exceptions.RequestException as e:
            print("Error making request:", e)
        except KeyError:
            print("Unable to retrieve current gold value from the response.")
        time.sleep(1)  # Wait for 1 second before the next iteration

        # Check for keyboard input
        if kbhit():
            break

# Call the function to run it
get_current_gold()
