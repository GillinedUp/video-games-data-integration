import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

from data_visualization import *


def filter_genres(df):
    genres_to_remove = ['Audio Production', 'Photo Editing', 'Video Production', 'Web Publishing',
                        'Animation & Modeling', 'Game Development', 'Utilities', 'Design & Illustration']
    return df[~df['genres'].isin(genres_to_remove)]


def parse_steam(df):
    return df[df["review_score"] > 0.]


def parse_rawg(df):
    df = df[df["rating"] > 0.]
    df["rating"] *= 2
    return df


def parse_metacritic(df):
    df = df[df["metacritic"] != ' ']
    df["metacritic"] = df["metacritic"].astype(float)
    df["metacritic"] /= 10.
    return df


def avg_for_all(df):
    df = parse_steam(df)
    print(f"Z recenzją na steam{len(df['review_score'])}")
    df = parse_rawg(df)
    df = parse_metacritic(df)
    avg_steam = df["review_score"].mean()
    avg_meta = df["metacritic"].mean()
    avg_rawg = df["rating"].mean()

    print("Wszystkie maja ocene na każdym portalu")
    print(f"steam avg:{avg_steam} ")
    print(f"rawg avg:{avg_rawg}")
    print(f"metacritic avg: {avg_meta}")

    plot_avg_game_score("oceny", "liczba", "Rozklad ocen dla trzech portali", review_score=df["review_score"]
                        , metacritic=df["metacritic"], rating=df["rating"])


def avg_RAWG_STEAM(df):
    df = parse_rawg(df)
    print(f"Z recenzją na RAWG{len(df['rating'])}")
    df = parse_steam(df)

    avg_steam = df["review_score"].mean()
    avg_rawg = df["rating"].mean()

    print("Oceny dla RAWG i Steam")
    print(f"steam avg:{avg_steam} ")
    print(f"rawg avg:{avg_rawg}")

    plot_avg_game_score("oceny", "liczba", "Rozklad ocen dla RAWG i Steam", review_score=df["review_score"]
                        , rating=df["rating"])


def avg_RAWG_metacritic(df):
    df = parse_metacritic(df)
    print(f"Z recenzją na Metacritic{len(df['metacritic'])}")

    df = parse_rawg(df)

    avg_rawg = df["rating"].mean()
    avg_meta = df["metacritic"].mean()

    print("Oceny dla RAWG i Metacritic")
    print(f"metacritic avg:{avg_meta} ")
    print(f"rawg avg:{avg_rawg}")

    plot_avg_game_score("oceny", "liczba", "Rozklad ocen dla Metacritic i RAWG",
                        metacritic=df["metacritic"], rating=df["rating"])


def avg_metacritic_STEAM(df):
    df = parse_steam(df)
    df = parse_metacritic(df)

    avg_steam = df["review_score"].mean()
    avg_meta = df["metacritic"].mean()

    print("Oceny dla Metacritic i Steam")
    print(f"steam avg:{avg_steam} ")
    print(f"metacritic avg:{avg_meta}")

    plot_avg_game_score("oceny", "liczba", "Rozklad ocen dla Metacritic i Steam",
                        review_score=df["review_score"], metacritic=df["metacritic"])




def scenario1(df):
    avg_for_all(df)
    avg_metacritic_STEAM(df)
    avg_RAWG_metacritic(df)
    avg_RAWG_STEAM(df)


def get_top_20_publishers(df):
    developers = df[df.duplicated(subset=['publisher_steam'], keep=False)]["publisher_steam"]
    df = df[df['publisher_steam'].isin(developers)]
    df2 = df.groupby(["publisher_steam"])['total_reviews'].sum().reset_index()
    indexes = df2.sort_values(by='total_reviews', ascending=False).head(20)['publisher_steam'].values
    return df[df['publisher_steam'].isin(indexes)]


def sort_publishers_by_games_number(df):
    developers_20 = get_top_20_publishers(df)
    developers_20['num_games'] = developers_20.groupby('publisher_steam')['id'].transform('count')
    return developers_20.sort_values(['num_games', 'publisher_steam'], ascending=False)


def print_analysis_results(publisher, variance, std, mean):
    print("dla developera " + publisher)
    print(f"wariancja: {variance}")
    print(f"odchylenie: {std}")
    print(f"średnia: {mean} ")
    print("\n")

def get_score_column(portal):
    if portal == 'RAWG':
        return "rating"
    elif portal == 'Steam':
        return 'review_score'
    return 'metacritic'


def parse_score(portal, df):
    if portal == 'RAWG':
        return parse_rawg(df)
    elif portal == 'Steam':
        return parse_steam(df)
    return parse_metacritic(df)


def analysis_for_games_publishers(df, portal):
    score_from = get_score_column(portal)
    df = parse_score(portal, df)

    sorted_publishers = sort_publishers_by_games_number(df)
    publishers_list = sorted_publishers['publisher_steam'].unique()
    print(publishers_list)

    x = []
    y = []
    e = []
    for i in publishers_list:
        df = sorted_publishers[sorted_publishers['publisher_steam'] == i]
        variance = df[score_from].var()
        std = df[score_from].std()
        mean = df[score_from].mean()

        print_analysis_results(i, variance, std, mean)

        x.append(mean)
        y.append(i)
        e.append(std)

    plot_publishers_analysis_results(sorted_publishers, score_from)


def scenario3(df):
    analysis_for_games_publishers(df, 'RAWG')
    analysis_for_games_publishers(df, 'Steam')
    analysis_for_games_publishers(df, 'metacritic')


def add_year(df):
    df = df[df["released"] != ' '].reset_index()

    df['year'] = df['released']
    for i in range(len(df['year'])):
        df['year'][i] = df['year'][i][:4]

    df = df[df["year"] != '2020']
    return df.sort_values(by='released', ascending=False)


def print_years_analysis(year, variance, std, mean, game_amount):
    print("dla roku" + year)
    print(f"wariancja: {variance}")
    print(f"odchylenie: {std}")
    print(f"średnia: {mean} ")
    print(f"ilosc wydanych gier: {game_amount}")
    print("\n")


def years_analysis(df, portal):
    score_from = get_score_column(portal)
    df = parse_score(portal, df)

    games_by_year = add_year(df)
    year = games_by_year['year'].unique()

    x = []
    y = []
    e = []
    z = []
    for i in year:
        df = games_by_year[games_by_year['year'] == i]

        variance = df[score_from].var()
        std = df[score_from].std()
        mean = df[score_from].mean()
        game_amount = len(df[score_from])

        print_years_analysis(i, variance, std, mean, game_amount)

        x.append(df[score_from].mean())
        y.append(i)
        e.append(std)
        z.append(game_amount)

    y.reverse()
    x.reverse()
    z.reverse()

    sns.pointplot(y=score_from, x='year',
                  data=games_by_year, join=False)
    plt.title("Średnia ocen w kolejnych latach")
    plt.show()
    sns.pointplot(y=score_from, x='year',
                  data=games_by_year, join=False)
    plt.title("Średnia ocen w kolejnych latach")
    plt.ylim(0, 10)
    plt.show()

    plt.bar(y, z)
    plt.title("Ilośc gier wydanych w kolejnych latach")
    plt.xlabel("rok")
    plt.ylabel("ilość gier")
    plt.show()


def scenario5(df):
    years_analysis(df, 'RAWG')
    years_analysis(df, 'metacritic')
    years_analysis(df, 'Steam')


df = pd.read_csv('all_games.csv')
df = filter_genres(df)

scenario5(df)
