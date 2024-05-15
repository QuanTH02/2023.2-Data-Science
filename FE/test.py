import pandas as pd

# df = pd.read_csv("../merge_data/final_merged.csv")
# movie_name_list = df["movie_name"].tolist()

# budget_list = df["budget"].tolist()

# index = 0
# for movie_name in movie_name_list:
#     if "," in movie_name:
#         print(movie_name)

string = ",,\"Dude, Where's My Car?\",PG-13,13000000.0,82.0,2087.0,13845914.0,46729374.0,5.5,146000.0,United States,Comedy Mystery Sci-Fi,79.0,19.01,0,12.0,2000.0"
str1 = string.split('"')
str2 = str1[2].split(",")
print(str2[6])