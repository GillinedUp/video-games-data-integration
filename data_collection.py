import csv
import json

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
