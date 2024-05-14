import pandas as pd

df = pd.read_csv("../critic_metascore/data/all_data_critic_metascore.csv")
movie_name_list = df["movie_name"].tolist()

critic_vote_metacritic_list = df["critic_vote_metacritic"].tolist()
meta_score_metacritic_list = df["meta_score_metacritic"].tolist()
critic_vote_rotten_list = df["critic_vote_rotten"].tolist()
meta_score_rotten_list = df["meta_score_rotten"].tolist()

index = 0
for movie_name in movie_name_list:
    if pd.isnull(critic_vote_metacritic_list[movie_name_list.index(movie_name)]) and pd.isnull(critic_vote_rotten_list[movie_name_list.index(movie_name)]):
        index += 1

print(index)
