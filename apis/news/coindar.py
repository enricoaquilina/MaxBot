import bs4
from urllib.request import urlopen


def get_news_data():
    url = "http://www.coindar.org"
    soup = bs4.BeautifulSoup(urlopen(url), 'lxml')
    return soup.find_all('div', {'class': 'calendar'})[0]