import json
import requests
import pandas as pd
import time
import numpy as np

def collect_steam_store_data(steam_store_url, url_list):
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

    steam_games_df = pd.DataFrame.from_dict(game_list)
    steam_games_df.set_index('id')
    steam_games_df = steam_games_df.loc[~all_games_df.index.duplicated(keep='first')]
    steam_games_df.to_csv('steam_data.csv')
    return steam_games_df

def collect_steam_reviews_data(steam_games_df):
    reviews_list = []

    for _, row in steam_games_df.iterrows():
        game_id = row['id']
        try:
            r = requests.get(reviews_url + str(game_id), params = {'json': 1, 'language': 'all'})

            if r.status_code == 200:
                game_json = r.json()
                if game_json['success'] == 1:
                    game_json = game_json['query_summary']
                    game_dict = {
                        'id': game_id,
                        'review_score': None,
                        'total_positive': None,
                        'total_reviews': None
                    }

                    if 'review_score' in game_json:
                        game_dict['review_score'] = game_json['review_score']
                    if 'total_positive' in game_json:
                        game_dict['total_positive'] = game_json['total_positive']
                    if 'total_reviews' in game_json:
                        game_dict['total_reviews'] = game_json['total_reviews']

                    reviews_list.append(game_dict)
            else:
                print('game_id')
        except Exception as e:
            print('game_id')

    steam_reviews_df = pd.DataFrame.from_dict(reviews_list)
    steam_reviews_df = steam_reviews_df.set_index('id')
    steam_reviews_df.to_csv('steam_reviews.csv')


def merge_games_and_reviews(steam_games_df, steam_reviews_df):
    steam_games_df_with_reviews = steam_games_df.loc[steam_reviews_df.index]
    steam_games_and_reviews = pd.merge(steam_reviews_df, steam_games_df_with_reviews, how='inner', on=steam_games_df_with_reviews.index)
    steam_games_and_reviews.set_index('key_0', inplace=True)
    steam_games_and_reviews.to_csv('steam_games_and_reviews.csv')

steam_store_url = 'https://store.steampowered.com/api/appdetails'
reviews_url = 'http://store.steampowered.com/appreviews/'