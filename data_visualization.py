import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_mean_steam_scores(mean_steam_scores):
    fig, ax = plt.subplots()
    ax.barh(mean_steam_scores_sorted.index, mean_steam_scores_sorted['review_score'], align='center')
    ax.invert_yaxis()
    ax.set_xlabel('Średnia ocena')
    ax.set_ylabel('Gatunek')
    ax.set_title('Średnia ocena według gatunku dla platformy Steam')
    plt.tight_layout()
    plt.savefig("steam_scores.png", dpi=300)

def plot_mean_rawg_scores(mean_rawg_scores):
    fig, ax = plt.subplots()
    ax.barh(mean_rawg_scores.index, mean_rawg_scores['rating'], align='center')
    ax.invert_yaxis()
    ax.set_xlabel('Średnia ocena')
    ax.set_ylabel('Gatunek')
    ax.set_title('Średnia ocena według gatunku dla platformy Rawg')
    plt.tight_layout()
    plt.savefig("rawg_scores.png", dpi=300)

def plot_mean_metacritic_scores(mean_metacritic_scores):
    fig, ax = plt.subplots()
    ax.barh(mean_metacritic_scores.index, mean_metacritic_scores['metacritic'], align='center')
    ax.invert_yaxis()
    ax.set_xlabel('Średnia ocena')
    ax.set_ylabel('Gatunek')
    ax.set_title('Średnia ocena według gatunku dla platformy Metacritic')
    plt.tight_layout()
    plt.savefig("metacritic_scores.png", dpi=300)

def scenario_2(mean_steam_scores, mean_rawg_scores, plot_mean_metacritic_scores):
    plot_mean_steam_scores(mean_steam_scores)
    plot_mean_rawg_scores(mean_rawg_scores)
    plot_mean_metacritic_scores(mean_metacritic_scores)