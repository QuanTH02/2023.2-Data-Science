import pandas as pd

df = pd.read_csv("../themoviedb/data/data.csv")
movie_name_list = df["movie_name"].tolist()

sequel_list = df["sequel"].tolist()

index = 0
for movie_name in movie_name_list:
    if sequel_list[movie_name_list.index(movie_name)] == 0:
        index += 1

print(index)
