import requests
from bs4 import BeautifulSoup
import pandas as pd

# ratings
# user_vote
# country

def crawl(soup):
    user_vote_and_rating_element = soup.find("div", {"data-testid": "hero-rating-bar__aggregate-rating"})

    # ratings
    ratings = user_vote_and_rating_element.find("div", {"class": "sc-bde20123-2 cdQqzc"}).text.split("/")[0].strip()

    # user_vote
    user_vote = user_vote_and_rating_element.find("div", {"class": "sc-bde20123-3 gPVQxL"}).text.replace("K", "000").replace("M", "000000")

    print(ratings)
    print(user_vote)

    li_country_element = soup.find("li",{'data-testid': "title-details-origin"})
    ul_element = li_country_element.find("ul")
    all_country_li_element = ul_element.find_all("li")

    # country
    for country in all_country_li_element:
        print(country.text)

if __name__ == "__main__":
    df = pd.read_csv("../mojo/data/test.csv")
    url_title_list = df["url_title"].tolist()

    for url_title in url_title_list:
        print("\n" + url_title)
        url = "https://www.imdb.com/title/" + url_title + "/"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            crawl(soup)
        else:
            print("Failed to fetch data:", response.status_code)