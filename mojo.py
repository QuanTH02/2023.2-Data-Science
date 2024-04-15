from bs4 import BeautifulSoup
import urllib.request
import pprint as pp

class Movie:
    def __init__(self, id, title, month, year, budget, runtime, genres: list, mpaa, screens, domestic, international, worldwide):
        self.id = id
        self.title = title
        self.month = month
        self.year = year
        self.budget = budget
        self.runtime = runtime
        self.genres = genres
        self.mpaa = mpaa
        self.screens = screens
        self.domestic = domestic
        self.international = international
        self.worldwide = worldwide
        

def convert_to_min(runtime):
    if "hr" in runtime:
        runtime = runtime.replace("hr", "").replace("min", "").split()
        hours = int(runtime[0])
        minutes = int(runtime[1])
        return hours * 60 + minutes
    else:
        return int(runtime.split()[0].replace("min", ""))
    

def convert_month(month):
    dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }
    return dict[month]


def get_info_table(info_table):
    budget = None
    release_month = None
    mpaa = None
    runtime = None
    genres = None
    screens = None

    rows = info_table.find_all('div', {'class': "a-section a-spacing-none"})
    for row in rows:
        if "Budget" in row.text:
            budget = row.find('span', {'class': "money"}).text.replace("$", "").replace(",", "")

        elif "Release Date" in row.text:
            release_date = [row.text for row in row.find_all('a')]
            release_date = [date.replace(",", "").split() for date in release_date]
            release_month = []
            release_year = []
            for date in release_date:
                if len(date) == 3:
                    release_month.append(convert_month(date[0]))
                    release_year.append(int(date[2]))


        elif "MPAA" in row.text:
            mpaa = row.find_all('span')[1].text.split()

        elif "Running Time" in row.text:
            runtime = row.find_all('span')[1].text
            runtime = convert_to_min(runtime)

        elif "Genres" in row.text:
            genres = row.find_all('span')[1].text.split()

        elif "Widest Release" in row.text:
            screens = row.find_all('span')[1].text
            screens = screens.split()[0]

    return budget, release_month, release_year, mpaa, runtime, genres, screens


def get_grosses(grosses):
    domestic = None
    international = None
    worldwide = None

    rows = grosses.find_all('div', {'class': "a-section a-spacing-none"})
    for row in rows:
        if "Domestic" in row.text:
            domestic = row.find('span', {'class': "money"}).text.replace("$", "").replace(",", "")
        elif "International" in row.text:
            international = row.find('span', {'class': "money"}).text.replace("$", "").replace(",", "")
        elif "Worldwide" in row.text:
            worldwide = row.find('span', {'class': "money"}).text.replace("$", "").replace(",", "")

    return domestic, international, worldwide
    

def crawl(release_id):
    url = f"https://www.boxofficemojo.com/release/{release_id}/"
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')

    title = soup.find('h1', {'class': "a-size-extra-large"}).text
    grosses = soup.find('div', {'class': "a-section a-spacing-none mojo-performance-summary-table"})
    info_table = soup.find('div', {'class': "a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile"})

    budget, release_month, release_year, mpaa, runtime, genres, screens = get_info_table(info_table)

    domestic, international, worldwide = get_grosses(grosses)

    return Movie(release_id, title, release_month, release_year, budget, runtime, genres, mpaa, screens, domestic, international, worldwide)
    

def main():
    with open("link_movie.txt", "r") as f:
        out = open("output.csv", "a")
        out.write("id,title,month,year,budget,runtime,genres,mpaa,screens,domestic,international,worldwide\n")
        for line in f:
            release_id = line.strip()
            movie = crawl(release_id)
            out.write(f"{movie.id},{movie.title},{movie.month},{movie.year},{movie.budget},{movie.runtime},{movie.genres},{movie.mpaa},{movie.screens},{movie.domestic},{movie.international},{movie.worldwide}\n")

