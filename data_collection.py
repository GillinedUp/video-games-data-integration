import csv
import json
import requests
import pandas as pd
import time
import numpy as np

import rawgpy

rawg = rawgpy.RAWG("student project for university")
date_from = "2019-01-01"
date_to = "2019-01-02"
results = rawg.get_request("https://api.rawg.io/api/games?dates=" + date_from + "," + date_to + "&platforms=4&stores=1")
url_list = []


def if_field_exists(field, game_data):
    if field in game_data:
        field = game_data[field]
    else:
        field = " "

    return field


def get_RAWG_data(results, outfile="games.csv", steam_file="steamFile"):
    is_next = True
    with open(outfile, 'a+', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "released", "rating", "exceptional",
                         "recommended", "meh", "skip", "metacritic", "tag1",
                         "tag2", "tag3", "tag4", "rating_count", "developer", "publisher"])

        while is_next:
            save_game_info(results, writer)
            if results["next"] is not None:
                try:
                    results = rawg.get_request(results["next"])
                    print(results["next"])
                except:
                    print("nie udało sie pobrac strony " + results["next"])
            else:
                is_next = False
    with open(steam_file, "w") as outfile:
        outfile.write("\n".join(str(item) for item in url_list))


def save_game_info(results, writer):
    for i in range(len(results["results"])):
        game = results["results"][i]["slug"]
        populated_game = rawg.get_game(game)
        populated_game.populate()
        json_game = populated_game.json

        steam_url = get_steam_url()
        id = parse_id(steam_url)
        rating1, rating2, rating3, rating4 = parse_rating(json_game)
        tag1, tag2, tag3, tag4 = parse_tags(json_game)
        name = if_field_exists("name")
        release = if_field_exists("released")
        rating = if_field_exists("rating")
        metacritic = if_field_exists("metacritic")
        ratings_count = if_field_exists("ratings_count")
        developer = parse_developer(json_game)
        publisher = parse_publisher(json_game)

        writer.writerow([id, name, release, rating,
                         rating1, rating2,
                         rating3, rating4,
                         metacritic, tag1,
                         tag2, tag3,
                         tag4,
                         ratings_count,
                         developer, publisher])


def get_steam_url(json_game):
    if len(json_game["stores"]) > 0:
        for j in range(len(json_game["stores"])):
            if json_game["stores"][j]['store']['id'] == 1:
                url = json_game["stores"][j]["url"]
                url_list.append(url)
                return url
    return None


def parse_id(steam_url):
    id = " "
    if steam_url is not None:
        id = steam_url.split("/")[4]
    return id


def parse_rating(json_game):
    rating1 = rating2 = rating3 = rating4 = ""
    if "ratings" in json_game:
        size = len(json_game["ratings"])
        rating1 = json_game["ratings"][0]["count"] if size > 0 else 0
        rating2 = json_game["ratings"][1]["count"] if size > 1 else 0
        rating3 = json_game["ratings"][2]["count"] if size > 2 else 0
        rating4 = json_game["ratings"][3]["count"] if size > 3 else 0
    return rating1, rating2, rating3, rating4


def parse_tags(json_game):
    tag1 = tag2 = tag3 = tag4 = " "
    if "tags" in json_game:
        size = len(json_game["tags"])
        tag1 = json_game["tags"][0]["name"] if size > 0 else " "
        tag2 = json_game["tags"][1]["name"] if size > 1 else " "
        tag3 = json_game["tags"][2]["name"] if size > 2 else " "
        tag4 = json_game["tags"][3]["name"] if size > 3 else " "
    return tag1, tag2, tag3, tag4


def parse_publisher(json_game):
    if "publishers" in json_game:
        size = len(json_game["publishers"])
        publisher = json_game["publishers"][0]["name"] if size > 0 else " "
    else:
        publisher = ""
    return publisher


def parse_developer(json_game):
    if "developers" in json_game:
        size = len(json_game["developers"])
        developer = json_game["developers"][0]["name"] if size > 0 else " "
    else:
        developer = ""
    return developer


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
    steam_games_df = steam_games_df.loc[~steam_games_df.index.duplicated(keep='first')]
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


def merge_steam_games_and_reviews(steam_games_df, steam_reviews_df):
    steam_games_with_reviews_df = steam_games_df.loc[steam_reviews_df.index]
    steam_games_and_reviews_df = pd.merge(steam_reviews_df, steam_games_with_reviews_df, how='inner', on=steam_games_with_reviews_df.index)
    steam_games_and_reviews_df.set_index('key_0', inplace=True)
    steam_games_and_reviews_df.to_csv('steam_games_and_reviews.csv')
    return steam_games_and_reviews_df

def merge_steam_and_rawg_games(steam_games_and_reviews_df, rawg_games_df):
    all_games_df = steam_games_and_reviews_df.join(rawg_games_df, how='inner', lsuffix='_steam', rsuffix='_rawg')
    all_games_df.index.name = 'id'
    all_games_df.to_csv('all_games.csv')
    return all_games_df

steam_store_url = 'https://store.steampowered.com/api/appdetails'
reviews_url = 'http://store.steampowered.com/appreviews/'