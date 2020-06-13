import pandas as pd
import matplotlib.pyplot as plt
from helpers import filter_genres
import seaborn as sns

df = pd.read_csv('all_games.csv')
df = filter_genres(df)
developers = df[df.duplicated(subset=['publisher_steam'], keep=False)]["publisher_steam"]


df = df[df['publisher_steam'].isin(developers)]

df2 = df.groupby(["publisher_steam"])['total_reviews'].sum().reset_index()

indexes = df2.sort_values(by='total_reviews', ascending=False).head(20)['publisher_steam'].values
developers_20 = df[df['publisher_steam'].isin(indexes)]
developers_20['num_games'] = developers_20.groupby('publisher_steam')['id'].transform('count')
abc =developers_20.sort_values(['num_games','publisher_steam'],ascending=False)
abc1 = abc['publisher_steam'].unique()
# developers_20 = df[df['developer_steam'].isin(abc)]
print(abc1)

x = []
y = []
e = []
for i in abc1:
    df = developers_20[developers_20['publisher_steam'] == i]
    print(i)
    # print(df["num_games"])
    # print("name: ")
    # print(df["name"])
    # print(df["review_score"])
    print("dla developera " + i )

    variance = df["review_score"].var()
    std=df["review_score"].std()
    print(f"wariancja: {variance}")
    print(f"odchylenie: {std}")
    x.append(df["review_score"].mean())
    y.append(i)
    e.append(std)
    mean=df["review_score"].mean()
    print(f"średnia: {mean} ")
    print("\n")

data = {'developers': y,
        'mean': x,
        'std': e
        }
df3 = pd.DataFrame(data)

# sns.pointplot(x='mean', y='developers',
#     data=data, join=False)
# plt.show()
#
# print(df.shape)
# d = df.groupby(["developer_steam"]).count()
# print(d)
# print(d.shape)
#
# # df=df.groupby(["total_reviews"])["total_reviews"].sum()
# df2 = df.groupby(["developer_steam"])['total_reviews'].sum().reset_index()
#
# # print(df.groupby(["total_reviews","developer_steam","name","review_score"]).sum())
# # print(df.groupby(["total_reviews","developer_steam","name","review_score"]).sum())
# indees = df2.sort_values(by='total_reviews', ascending=False).head(20)['developer_steam'].values
#
# developers_20 = df[df['developer_steam'].isin(indees)]
# developers = df['developer_steam']
#
# d = developers_20.groupby(["developer_steam"]).count()
# # print(d)
# # for i in indees:
# #     df= developers_20[developers_20['developer_steam']==i]
# #     print("dla developera "+i+" wariancja")
# #     variance= df["review_score"].var()
# #     print(variance)
# #     print("\n")
# #
# # print(df[df['developer_steam'].isin(indees)])
# # print(df.loc[indees])
# # print(df.loc[indees])
#
sns.pointplot(y='publisher_steam', x='review_score',
    data=abc, join=False)
plt.title("Dystrybucja ocen dla top 20 wydawców")
plt.show()
