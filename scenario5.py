import pandas as pd
import matplotlib.pyplot as plt
from helpers import filter_genres
import seaborn as sns

df = pd.read_csv('all_games.csv')
df = filter_genres(df)
# developers = df[df.duplicated(subset=['publisher_steam'], keep=False)]["publisher_steam"]
#
#
# df = df[df['publisher_steam'].isin(developers)]
#
# df2 = df.groupby(["publisher_steam"])['total_reviews'].sum().reset_index()
#
# indexes = df2.sort_values(by='total_reviews', ascending=False).head(20)['publisher_steam'].values
# developers_20 = df[df['publisher_steam'].isin(indexes)]



df = df[df["released"]!=' '].reset_index()
df=df[df["review_score"]>0.].reset_index()
# df["metacritic"] = df["metacritic"].astype(float)
# df["metacritic"] /=10
df['year']=df['released']
for i in range (len(df['year'])):
      df['year'][i]= df['year'][i][:4]

df=df[df["year"]!='2020']
games_by_year = df.sort_values(by='released',ascending=False)
year = games_by_year['year'].unique()
print(year)

x = []
y = []
e = []
z=[]
for i in year:
    df = games_by_year[games_by_year['year'] == i]
    print(i)
    # print(df["num_games"])
    # print("name: ")
    # print(df["name"])
    # print(df["review_score"])
    print("dla roku" + i )

    variance = df["review_score"].var()
    std=df["review_score"].std()
    print(f"wariancja: {variance}")
    print(f"odchylenie: {std}")
    x.append(df["review_score"].mean())
    y.append(i)
    e.append(std)
    z.append(len(df['review_score']))
    mean=df["review_score"].mean()
    print(f"średnia: {mean} ")
    print(f"ilosc wydanych gier: {len(df['review_score'])}")
    print("\n")
y.reverse()
x.reverse()
z.reverse()
sns.pointplot(y='review_score', x='year',
    data=games_by_year, join=False)
# plt.ylim(0, 10)
plt.title("Średnia ocen w kolejnych latach")
plt.show()
sns.pointplot(y='review_score', x='year',
    data=games_by_year, join=False)
# plt.ylim(0, 10)
plt.title("Średnia ocen w kolejnych latach")
plt.ylim(0, 10)
plt.show()
# plt.title("Średnia ocen dla gier w kolejnych latach")
# plt.xlabel("rok")
# plt.ylabel("ocena")
#
# plt.plot(y, x, 'ro')
# # plt.axis([0, 6, 0, 20])
# plt.show()
plt.bar(y,z)
plt.title("Ilośc gier wydanych w kolejnych latach")
plt.xlabel("rok")
plt.ylabel("ilość gier")
plt.show()
#
# developers_20['num_games'] = developers_20.groupby('publisher_steam')['id'].transform('count')
# abc =developers_20.sort_values(['num_games','publisher_steam'],ascending=False)
# abc1 = abc['publisher_steam'].unique()
# # developers_20 = df[df['developer_steam'].isin(abc)]
# print(abc1)
#
# x = []
# y = []
# e = []
# for i in abc1:
#     df = developers_20[developers_20['publisher_steam'] == i]
#     print(i)
#     # print(df["num_games"])
#     # print("name: ")
#     # print(df["name"])
#     # print(df["review_score"])
#     print("dla developera " + i )
#
#     variance = df["review_score"].var()
#     std=df["review_score"].std()
#     print(f"wariancja: {variance}")
#     print(f"odchylenie: {std}")
#     x.append(df["review_score"].mean())
#     y.append(i)
#     e.append(std)
#     mean=df["review_score"].mean()
#     print(f"średnia: {mean} ")
#     print("\n")
#
# data = {'developers': y,
#         'mean': x,
#         'std': e
#         }
# df3 = pd.DataFrame(data)
#
# sns.pointplot(y='publisher_steam', x='review_score',
#     data=abc, join=False)
# plt.title("Dystrybucja ocen dla top 20 wydawców")
# plt.show()
