import matplotlib.pyplot as plt
import seaborn as sns


def plot_avg_game_score(xlabel, ylabel, title, review_score=None, metacritic=None, rating=None):
    if review_score is not None:
        review_score.hist(alpha=0.5, label="Steam")
    if metacritic is not None:
        metacritic.hist(alpha=0.5, label="Metacritic")
    if rating is not None:
        rating.hist(alpha=0.5, label="RAWG")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()


def plot_publishers_analysis_results(sorted_publishers, score_from):
    sns.pointplot(y='publisher_steam', x=score_from,
                  data=sorted_publishers, join=False)
    plt.title("Dystrybucja ocen dla top 20 wydawców")
    plt.show()


def plot_avg_game_score_by_years(score_from, games_by_year):
    sns.pointplot(y=score_from, x='year',
                  data=games_by_year, join=False)
    plt.title("Średnia ocen w kolejnych latach")
    plt.show()


def plot_scaled_avg_game_score_by_years(score_from, games_by_year):
    sns.pointplot(y=score_from, x='year',
                  data=games_by_year, join=False)
    plt.title("Średnia ocen w kolejnych latach")
    plt.ylim(0, 10)
    plt.show()


def plot_his_game_amount(years, games_by_year):
    plt.bar(years, games_by_year)
    plt.title("Ilośc gier wydanych w kolejnych latach")
    plt.xlabel("rok")
    plt.ylabel("ilość gier")
    plt.show()


def plot_game_year_analysis(score_from, years, game_amount, games_by_year):
    plot_avg_game_score_by_years(score_from, games_by_year)
    plot_scaled_avg_game_score_by_years(score_from, games_by_year)
    plot_his_game_amount(years, games_by_year)
