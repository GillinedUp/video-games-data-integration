import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

from helpers import filter_genres


def parse_steam(df):
    return df[df["review_score"] > 0.]


def parse_rawg(df):
    df=df[df["rating"] > 0.]
    df["rating"] *=2
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

    df["review_score"].hist(alpha=0.5, label="Steam")
    plot_his("oceny", "liczba", "Rozklad ocen dla trzech portali")
    df["metacritic"].hist(alpha=0.5, label="Metacritic")
    plot_his("oceny", "liczba", "Rozklad ocen dla trzech portali")
    df["rating"].hist(alpha=0.5, label="RAWG")
    plot_his("oceny", "liczba", "Rozklad ocen dla trzech portali")
    plt.legend()
    plt.show()


def avg_RAWG_STEAM(df):

    df = parse_rawg(df)
    print(f"Z recenzją na RAWG{len(df['rating'])}")
    df = parse_steam(df)

    avg_steam = df["review_score"].mean()
    avg_rawg = df["rating"].mean()

    print("Oceny dla RAWG i Steam")
    print(f"steam avg:{avg_steam} ")
    print(f"rawg avg:{avg_rawg}")

    df["review_score"].hist(alpha=0.5, label="Steam")
    plot_his("oceny", "liczba", "Rozklad ocen dla RAWG i Steam")
    df["rating"].hist(alpha=0.5, label="RAWG")
    plot_his("oceny", "liczba", "Rozklad ocen dla RAWG i Steam")
    plt.legend()
    plt.show()


def avg_RAWG_metacritic(df):
    df = parse_metacritic(df)
    print(f"Z recenzją na Metacritic{len(df['metacritic'])}")

    df = parse_rawg(df)

    avg_rawg = df["rating"].mean()
    avg_meta = df["metacritic"].mean()

    print("Oceny dla RAWG i Metacritic")
    print(f"metacritic avg:{avg_meta} ")
    print(f"rawg avg:{avg_rawg}")

    df["metacritic"].hist(alpha=0.5, label="Metacritic")
    plot_his("oceny", "liczba", "Rozklad ocen dla RAWG i Metacritic")
    df["rating"].hist(alpha=0.5, label="RAWG")
    plot_his("oceny", "liczba", "Rozklad ocen dla RAWG i Metacritic")
    plt.legend()
    plt.show()


def avg_metacritic_STEAM(df):
    df = parse_steam(df)
    df = parse_metacritic(df)

    avg_steam = df["review_score"].mean()
    avg_meta = df["metacritic"].mean()

    print("Oceny dla Metacritic i Steam")
    print(f"steam avg:{avg_steam} ")
    print(f"metacritic avg:{avg_meta}")

    df["review_score"].hist(alpha=0.5, label="Steam")
    plot_his("oceny", "liczba", "Rozklad ocen dla Metacritic i Steam")
    df["metacritic"].hist(alpha=0.5, label="Metacritic")
    plot_his("oceny", "liczba", "Rozklad ocen dla Metacritic i Steam")
    plt.legend()
    plt.show()


def plot_his(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)


df = pd.read_csv('all_games.csv')
df = filter_genres(df)

# avg_for_all(df)
# avg_metacritic_STEAM(df)
# avg_RAWG_metacritic(df)
avg_RAWG_STEAM(df)
