import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111"
headers = {"User-Agent": user_agent, "Accept-Language": "en-US,en;q=0.5"}

# CRAWL:

# ratings
# user_vote
# country
# genres

check_search_imdb_slenium = False
check_search_imdb_requests = False

# Crawl genres MOJO
def crawl_mojo_request(soup):
    div_all_element = soup.find('div', {'class': 'a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile'})

    all_div_results = div_all_element.find_all('div', recursive=False)

    for div_result in all_div_results:
        # print(div_result.text)
        if "Genres" in div_result.find_all('span')[0].text:
            genres_content = div_result.find_all('span')[1].text
            genres_array = genres_content.split('\n')
            genres = [genre.strip() for genre in genres_array if genre.strip()]

            if len(genres) > 0:
                print("Genres: " + ' '.join(genres))

            break

# Crawl country IMDB
def crawl_imdb_request(soup):
    country = []
    user_vote_and_rating_element = soup.find("div", {"data-testid": "hero-rating-bar__aggregate-rating"})

    # ratings
    ratings = user_vote_and_rating_element.find("div", {"class": "sc-bde20123-2 cdQqzc"}).text.split("/")[0].strip()

    # user_vote
    user_vote = user_vote_and_rating_element.find("div", {"class": "sc-bde20123-3 gPVQxL"}).text.replace("K", "000").replace("M", "000000")

    print("Rating: " + ratings)
    print("User vote: " + user_vote)

    li_country_element = soup.find("li",{'data-testid': "title-details-origin"})
    ul_element = li_country_element.find("ul")
    all_country_li_element = ul_element.find_all("li")

    # country
    for country_li in all_country_li_element:
        country.append(country_li.text)

    if len(country) > 0:
        print("Country: " + ' '.join(country))

# Crawl genres and country IMDB
def crawl_imdb_selenium(url):
    genres = []
    country = []

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 5000);")
    time.sleep(1)

    tag_storyline_element = driver.find_element(By.CSS_SELECTOR, "div[data-testid='storyline-header']").find_element(By.XPATH, "./..")
    driver.execute_script("arguments[0].scrollIntoView();", tag_storyline_element)
    time.sleep(5)

    if tag_storyline_element.find_element(By.CSS_SELECTOR, "li[data-testid='storyline-genres']"):
        li_all_genres_element = driver.find_element(By.CSS_SELECTOR, "li[data-testid='storyline-genres']")
        ul_genres_element = li_all_genres_element.find_element(By.TAG_NAME, "ul")
        li_genres_elements = ul_genres_element.find_elements(By.TAG_NAME, "li")

        for li_genres in li_genres_elements:
            genres.append(li_genres.text)

    
    tag_detail_element = driver.find_element(By.CSS_SELECTOR, "div[data-testid='title-details-header']").find_element(By.XPATH, "./..")

    if tag_detail_element.find_element(By.CSS_SELECTOR, "li[data-testid='title-details-origin']"):
        li_country_element = tag_detail_element.find_element(By.CSS_SELECTOR, "li[data-testid='title-details-origin']")
        ul_country_element = li_country_element.find_element(By.TAG_NAME, "ul")
        li_country_elements = ul_country_element.find_elements(By.TAG_NAME, "li")

        for li_country in li_country_elements:
            country.append(li_country.text)
    
    if len(genres) > 0:
        print("Genres: " + ' '.join(genres))
    if len(country) > 0:
        print("Country: " + ' '.join(country))
    
    driver.close()
    
# Search movie in mojo
def page_search_mojo(soup_search, movie_title, year_release):
    result_element = soup_search.find("div", {"class": "a-section mojo-gutter"})

    all_div_results = result_element.find_all("div", {"class": "a-fixed-left-grid"})

    for result in all_div_results:
        if result.find("a", {"class": "a-size-medium a-link-normal a-text-bold"}):
            movie_title_element = result.find("a", {"class": "a-size-medium a-link-normal a-text-bold"})
        else:
            continue
    
        movie_name = movie_title_element.text

        if movie_title_element.parent.find_all("span", {"class": "a-color-secondary"})[0]:
            year = movie_title_element.parent.find_all("span", {"class": "a-color-secondary"})[0].text
            year = year.strip().strip("()")
        else:
            continue

        if str(year) == str(year_release) and str(movie_name) == str(movie_title):
            # url
            url = "https://www.boxofficemojo.com" + movie_title_element["href"]
            # print("URL: " + url)
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                crawl_mojo_request(soup)
            else:
                print("Failed to fetch data:", response.status_code)

            break


 
# Search movie in imdb
def page_search_imdb(soup_search, movie_title, year_release):
    result_element = soup_search.find("ul", {"class": "ipc-metadata-list ipc-metadata-list--dividers-after sc-17bafbdb-3 WTcPP ipc-metadata-list--base"})

    all_li_results = result_element.find_all("li", recursive=False)

    for result in all_li_results:
        # print(result.text)
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
            if check_search_imdb_requests:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    crawl_imdb_request(soup)
                else:
                    print("Failed to fetch data:", response.status_code)
            elif check_search_imdb_slenium:
                crawl_imdb_selenium(url)

            break

def search_imdb(movie_name, year_release):
    print("\n" + str(movie_name) + " - " + str(year_release))
    url = "https://www.imdb.com/find/?q=" + movie_name + "&s=tt&ttype=ft&ref_=fn_ft"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(sosup)
        page_search_imdb(soup, movie_name, year_release)
    else:
        print("Failed to fetch data:", response.status_code)

if __name__ == "__main__":
    df = pd.read_csv("../mojo/data/test.csv")
    url_title_list = df["url_title"].tolist()
    movie_name_list = df["movie_name"].tolist()
    year_list = df["year"].tolist()

    genres_list = df["genres"].tolist()
    country_list = df["country"].tolist()

    

    for url_title in url_title_list:
        print("\nMovie: " + movie_name_list[url_title_list.index(url_title)])

        # Crawl imdb selenium
        if pd.isnull(country_list[url_title_list.index(url_title)]) and pd.isnull(genres_list[url_title_list.index(url_title)]):
            check_search_imdb_slenium = True
            print("Not two")
            if pd.isnull(url_title):
                search_imdb(movie_name_list[url_title_list.index(url_title)], year_list[url_title_list.index(url_title)])
            else:
                url = "https://www.imdb.com/title/" + url_title + "/"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    crawl_imdb_request(soup)
                else:
                    print("Failed to fetch data:", response.status_code)
            check_search_imdb_slenium = False

        # Crawl imdb requests
        elif pd.isnull(country_list[url_title_list.index(url_title)]):
            check_search_imdb_requests = True
            print("Not country") 
            if pd.isnull(url_title):
                search_imdb(movie_name_list[url_title_list.index(url_title)], year_list[url_title_list.index(url_title)])
            else:
                url = "https://www.imdb.com/title/" + url_title + "/"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    crawl_imdb_request(soup)
                else:
                    print("Failed to fetch data:", response.status_code)
            check_search_imdb_requests = False

        # Crawl Mojo
        elif pd.isnull(genres_list[url_title_list.index(url_title)]):
            print("Not Genres")
            url = "https://www.boxofficemojo.com/search/?q=" + movie_name_list[url_title_list.index(url_title)] + "/"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                page_search_mojo(soup, movie_name_list[url_title_list.index(url_title)], year_list[url_title_list.index(url_title)])
            else:
                print("Failed to fetch data:", response.status_code)
        else:
            print("OK")

        print("\n-----------------------------------------------")