import pandas as pd

df = pd.read_csv("mojo/data/copy_mojo_quan.csv", encoding="latin1")
movie_name_list = df["movie_name"].tolist()

# Chuyển đổi tất cả các chuỗi trong danh sách thành chữ thường
movie_name_list = [movie.lower() for movie in movie_name_list]

index = 0
for movie_name in movie_name_list:
    for movie in movie_name_list:
        print(movie + " " + movie_name)
        # So sánh các chuỗi đã chuyển đổi thành chữ thường
        if movie_name_list.index(movie) != movie_name_list.index(movie_name) and movie == movie_name:
            index += 1
            print("\n" + movie + " " + movie_name)
            print("YES: " + str(movie_name_list.index(movie)))

print(index)