import pandas as pd
import numpy as np

def get_list_of_genres(all_games_df):
    return list(set(list(all_games_df['genres'].dropna())))

def get_scenario_2_data(all_games_df):
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

