import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

df = pd.read_csv("../static/final_merged.csv")
movie_name_list = df["movie_name"].tolist()
month_list = df["month"].tolist()
mpaa_list = df["mpaa"].tolist()
domestic_box_office_list = df["domestic_box_office"].tolist()

domes = 0
index = 0
for movie_name in movie_name_list:
    if mpaa_list[movie_name_list.index(movie_name)] == "PG-13":
        domes = domes + int(domestic_box_office_list[movie_name_list.index(movie_name)])
        index = index + 1

print(domes/index)