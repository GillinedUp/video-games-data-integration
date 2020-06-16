import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

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

    plot_game_year_analysis(score_from, y, z, games_by_year)


def scenario5(df):
    years_analysis(df, 'RAWG')
    years_analysis(df, 'metacritic')
    years_analysis(df, 'Steam')



def get_list_of_genres(all_games_df):
    return list(set(list(all_games_df['genres'].dropna())))

def get_mean_scores_per_genre(all_games_df):
    non_game_genres = ['Audio Production', 'Photo Editing', 'Video Production', 'Web Publishing', 'Animation & Modeling', 'Game Development', 'Utilities', 'Design & Illustration']

    steam_reviews_df = all_games_df[['review_score', 'genres']].copy()
    steam_reviews_df.replace(0, np.nan, inplace=True)
    steam_reviews_df.dropna(inplace=True)
    mean_steam_scores = steam_reviews_df.groupby(['genres']).mean().sort_values(by=['review_score']).round(decimals=2)
    mean_steam_scores = mean_steam_scores.drop(non_game_genres)
    mean_steam_scores.to_csv('mean_steam_scores.csv')

    rawg_reviews = all_games_df[['rating', 'genres']].copy()
    rawg_reviews.replace(0.0, np.nan, inplace=True)
    rawg_reviews.dropna(inplace=True)
    mean_rawg_scores = rawg_reviews.groupby(['genres']).mean().sort_values(by=['rating']).round(decimals=2)
    mean_rawg_scores = mean_rawg_scores.drop(non_game_genres)
    mean_rawg_scores.to_csv('mean_rawg_scores.csv')

    metacritic_reviews = all_games_df[['metacritic', 'genres']].copy()
    metacritic_reviews['metacritic'].replace(' ', np.nan, inplace=True)
    metacritic_reviews.dropna(inplace=True)
    metacritic_reviews.astype({'metacritic': np.int64}, inplace=True)
    mean_metacritic_scores = metacritic_reviews.groupby(['genres']).mean().sort_values(by=['metacritic'])
    mean_metacritic_scores = mean_metacritic_scores.drop(non_game_genres)
    mean_metacritic_scores.to_csv('mean_metacritic_scores.csv')

    return mean_steam_scores, mean_rawg_scores, mean_metacritic_scores

def merge_developer_and_publisher_data(all_games_df):
    all_games_df['developer_steam'] = np.where(all_games_df['developer_steam'].isnull()
                                           & ~all_games_df['developer_rawg'].str.isspace(),
                                           all_games_df['developer_rawg'],
                                           all_games_df['developer_steam'])
    all_games_df['publisher_steam'] = np.where(all_games_df['publisher_steam'].isnull()
                                           & ~all_games_df['publisher_rawg'].isnull(),
                                           all_games_df['publisher_rawg'],
                                           all_games_df['publisher_steam'])
    return all_games_df

def transform_data_for_regressor(all_games_df):
    all_games_df = merge_developer_and_publisher_data(all_games_df)
    games_non_zero_score = all_games_df[all_games_df['review_score'] != 0].copy()
    data = games_non_zero_score[['developer_steam', 'publisher_steam', 'genres', 'released', 'tag1', 'tag2', 'tag3', 'tag4']].copy()
    data_lowercase = data.apply(lambda x: x.astype(str).str.lower())
    data_lowercase['released'] = data_lowercase['released'].apply(lambda x: str(x.year) if type(x) == pd._libs.tslibs.timestamps.Timestamp else '')
    X_raw = data_lowercase.values
    y = games_non_zero_score['review_score'].values
    enc = OneHotEncoder(handle_unknown='ignore')
    enc.fit(X_raw)
    X = enc.transform(X_raw)
    return X, y

def split_data(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_svr(X_train, X_test, y_train, y_test):
    regr = svm.SVR()
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)
    return mean_absolute_error(y_test, y_pred)

def get_simple_prediction_mean_absolute_error(y_test):
    y_pred_mean = np.empty(y_test.shape)
    y_pred_mean.fill(y_test.mean())
    return mean_absolute_error(y_test, y_pred_mean)

df = pd.read_csv('all_games.csv')
df = filter_genres(df)