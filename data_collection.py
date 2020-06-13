import json
import requests
import pandas as pd
import time
import numpy as np

def collect_steam_store_data():

steam_store_url = 'https://store.steampowered.com/api/appdetails'

for year in years:
    url_list = None
    with open('outfile' + year) as f:
        url_list = f.readlines()

    app_list = [url.strip().split('/')[4] for url in url_list]

    game_list = []

    for game_id in app_list:
        r = requests.get(steam_store_url, params = {'appids':game_id})

        if r.status_code == 200:
            game_json = r.json()[game_id]
            if game_json['success'] == True and game_json['data']['type'] == 'game':      
                game_data = game_json['data']
                game_dict = {
                    'id': game_id,
                    'title': game_data['name'],
                    'developer': '',
                    'publisher': '',
                    'release_date': '',
                    'genres': ''
                }

                if 'developers' in game_data:
                    game_dict['developer'] = game_data['developers'][0]
                if 'publishers' in game_data:
                    game_dict['publisher'] = game_data['publishers'][0]
                if 'release_date' in game_data:
                    game_dict['release_date'] = game_data['release_date']['date']
                if 'genres' in game_data:
                    game_dict['genres'] = game_data['genres'][0]['description']

                game_list.append(game_dict)
        else:
            print('game id: {}, error code: {}'.format(game_id, r.status_code))

        time.sleep(2)

    steam_df = pd.DataFrame.from_dict(game_list)

    steam_df.to_csv('steam_data_' + year + '.csv')