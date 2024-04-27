import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("../mojo/data/test1.csv")
    movie_name_list = df["movie_name"].tolist()
    month_list = df["month"].tolist()
    year_list = df["year"].tolist()

    for month in month_list:
        if pd.isnull(month):
            month_list[month_list.index(month)] = ""
        else:
            month_list[month_list.index(month)] = int(month)

    for movie_name in movie_name_list:
        print(movie_name)
        print(month_list[movie_name_list.index(movie_name)])
        print(year_list[movie_name_list.index(movie_name)])
        print("-----------------------------------------------")

    