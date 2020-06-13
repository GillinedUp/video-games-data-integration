import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

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
    return X, y_test

def split_data(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=42) 

def train_svr(X_train, X_test, y_train, y_test)
    regr = svm.SVR()
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)
    return mean_absolute_error(y_test, y_pred)

def get_simple_prediction_mean_absolute_error(y_test):
    y_pred_mean = np.empty(y_test.shape)
    y_pred_mean.fill(y_test.mean())
    return mean_absolute_error(y_test, y_pred_mean)

