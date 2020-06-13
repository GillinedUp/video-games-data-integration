def filter_genres(df):
    genres_to_remove = ['Audio Production', 'Photo Editing', 'Video Production', 'Web Publishing',
                        'Animation & Modeling', 'Game Development', 'Utilities', 'Design & Illustration']
    return df[~df['genres'].isin(genres_to_remove)]
def parse_metacritic(df):
    df = df[df["metacritic"] != ' ']
    df["metacritic"] = df["metacritic"].astype(float)
    df["metacritic"] /= 10.
    return df
def parse_rawg(df):
    df=df[df["rating"] > 0.]
    df["rating"] *=2
    return df