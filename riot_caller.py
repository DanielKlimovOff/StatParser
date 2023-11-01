from urllib import request
import requests
from pprint import pprint
import json


API_KEY = 'RGAPI-9a822dba-9b14-42a6-b3b8-4fe96b477a08'

def main():
    user_data = input_user_data()
    if not good_ending_test(user_data):
        print(user_data.args[0])
        return 1

    print(user_data)
    print()

    user_information = get_user_information(user_data)
    if not good_ending_test(user_information):
        print(user_information.args[0])
        return 2

    user_information = get_user_puuid(user_information)
    if not good_ending_test(user_information):
        print(user_information.args[0])
        return 3

    pprint(user_information)
    print()

    user_last_match_information = get_user_last_matchid(user_information)
    if not good_ending_test(user_information):
        print(user_information.args[0])
        return 4

    user_last_match_information = get_match_information(user_last_match_information)
    if not good_ending_test(user_information):
        print(user_information.args[0])
        return 4

    pprint(user_last_match_information)
    print()

    return 0

def good_ending_test(function_result):
    if isinstance(function_result, Exception):
        return False
    
    return True


def input_user_data():
    try: 
        user_data_file = open('input_data.txt', "r")
    except:
        return Exception('OpenInputFileError')
    
    user_data = user_data_file.read()
    user_data_file.close()

    return user_data

def get_user_information(user_data):
    try:
        user_information = {}
        user_information['game_name'] = user_data.split('\n')[0].split('#')[0]
        user_information['tag_line'] = int(user_data.split('\n')[0].split('#')[1])
        user_information['region'] = user_data.split('\n')[1].lower()
    except:
        return Exception('InputFileFormatError')

    return user_information

def get_user_puuid(user_information):
    try:
        request_text = f'https://{user_information["region"]}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{user_information["game_name"]}/{user_information["tag_line"]}?api_key={API_KEY}'
        response = requests.get(request_text)
    except:
        return Exception('RequestSendError')

    if response.status_code != 200:
        return Exception('RequestResponseError (code={response.status_code})')

    user_information['puuid'] = json.loads(response.content)['puuid']

    return user_information

def get_user_last_matchid(user_information):
    try:
        request_text = f'https://{user_information["region"]}.api.riotgames.com/lol/match/v5/matches/by-puuid/{user_information["puuid"]}/ids?start={0}&count={1}&api_key={API_KEY}'
        response = requests.get(request_text)
    except:
        return Exception('RequestSendError')
    
    if response.status_code != 200:
        return Exception('RequestResponseError (code={response.status_code})')
    
    match_information = {}
    match_information['region'] = user_information['region']
    match_information['matchid'] = json.loads(response.content)[0]

    return match_information

def get_match_information(match_information):
    try:
        request_text = f'https://{match_information["region"]}.api.riotgames.com/lol/match/v5/matches/{match_information["matchid"]}?api_key={API_KEY}'
        response = requests.get(request_text)
    except:
        return Exception('RequestSendError')
    
    if response.status_code != 200:
        return Exception('RequestResponseError (code={response.status_code})')
    
    match_raw_data = json.loads(response.content)

    match_information['players'] = get_players_stats_from_json(match_raw_data)

    return match_information

def get_players_stats_from_json(match_raw_data):
    players = []

    for player in match_raw_data['info']['participants']:
        players.append([player['summonerName'], player['championName'], player['kills'], player['deaths'], player['assists'], player['teamId'], player['win']])

    return players


if __name__ == '__main__':
    main()
