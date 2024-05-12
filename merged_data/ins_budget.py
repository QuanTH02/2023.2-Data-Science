import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import numpy as np
import re


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111"
headers = {"User-Agent": user_agent, "Accept-Language": "en-US,en;q=0.5"}

def convert_month_to_string(month):
    if month == 1:
        return "Jan"
    elif month == 2:
        return "Feb"
    elif month == 3:
        return "Mar"
    elif month == 4:
        return "Apr"
    elif month == 5:
        return "May"
    elif month == 6:
        return "Jun"
    elif month == 7:
        return "Jul"
    elif month == 8:
        return "Aug"
    elif month == 9:
        return "Sep"
    elif month == 10:
        return "Oct"
    elif month == 11:
        return "Nov"
    elif month == 12:
        return "Dec"
    
def movie_name_new(movie_name):
    match = re.match(r'(.+?)\(', movie_name)
    if match:
        str1 = match.group(1).strip()
        str2 = re.search(r'\((.+)\)', movie_name).group(1).strip()
        return str1, str2
    else:
        return None, None

def search_the_numbers(soup, movie_name, month, year):
    month = int(month)
    month = convert_month_to_string(month)

    table_element = soup.find_all("table")
    print("OK")

    if len(table_element) >= 2:
        all_tr_element = table_element[1].find_all("tr")
        for tr_element in all_tr_element:
            if all_tr_element.index(tr_element) % 2 == 1:
                all_td_element = tr_element.find_all("td")
                movie_name1, movie_name2 = movie_name_new(movie_name)
                print(movie_name1)


    return

if __name__ == "__main__":
    df = pd.read_csv("merged.csv")
    movie_name_list = df["movie_name"].tolist()
    month_list = df["month"].tolist()
    year_list = df["year"].tolist()

    budget_list = df["budget"].tolist()

    for budget in budget_list:
        if np.isnan(budget):
            print("Invalid budget")
            url = "https://www.the-numbers.com/custom-search?searchterm=" + movie_name_list[budget_list.index(budget)]
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                search_the_numbers(soup, movie_name_list[budget_list.index(budget)], month_list[budget_list.index(budget)], year_list[budget_list.index(budget)])
            else:
                print("Failed to fetch data:", response.status_code)

            break