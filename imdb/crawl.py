import requests
from bs4 import BeautifulSoup
import pandas as pd

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111"

headers = {"User-Agent": user_agent, "Accept-Language": "en-US,en;q=0.5"}

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

def page_search(soup_search, movie_title, year_release):
    result_element = soup_search.find("ul", {"class": "ipc-metadata-list ipc-metadata-list--dividers-after sc-17bafbdb-3 WTcPP ipc-metadata-list--base"})

    all_li_results = result_element.find_all("li", recursive=False)

    for result in all_li_results:
        print(result.text)
        if result.find("a", {"class": "ipc-metadata-list-summary-item__t"}):
            movie_title_element = result.find("a", {"class": "ipc-metadata-list-summary-item__t"})
        else:
            continue
        
        movie_name = movie_title_element.text

        if result.find("span", {"class": "ipc-metadata-list-summary-item__li"}):
            year = result.find("span", {"class": "ipc-metadata-list-summary-item__li"}).text
        else:
            continue

        # print("\n" + movie_name + " - " + month + "/" + year)
        # print(movie_title + " - " + str(month_release) + "/" + str(year_release))

        if str(year) == str(year_release) and str(movie_name) == str(movie_title):
            # url
            url = "https://www.imdb.com" + movie_title_element["href"]
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print("OK")
                soup = BeautifulSoup(response.content, 'html.parser')
                crawl(soup)
                
            else:
                print("Failed to fetch data:", response.status_code)

            break

def search(movie_name, year_release):
    print("\n" + str(movie_name) + " - " + str(year_release))
    url = "https://www.imdb.com/find/?q=" + movie_name + "&s=tt&ttype=ft&ref_=fn_ft"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(sosup)
        page_search(soup, movie_name, year_release)
    else:
        print("Failed to fetch data:", response.status_code)

if __name__ == "__main__":
    df = pd.read_csv("../mojo/data/test.csv")
    url_title_list = df["url_title"].tolist()
    movie_name_list = df["movie_name"].tolist()
    year_list = df["year"].tolist()
    print(url_title_list)
    

    for url_title in url_title_list:
        if pd.isnull(url_title):
            search(movie_name_list[url_title_list.index(url_title)], year_list[url_title_list.index(url_title)])
        else:
            print("\n" + url_title)
            url = "https://www.imdb.com/title/" + url_title + "/"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                crawl(soup)
            else:
                print("Failed to fetch data:", response.status_code)

