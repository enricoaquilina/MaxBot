import bs4
from urllib.request import urlopen
from common.http import request


class CoinDar:
    def __init__(self):
        self.req = request.MyRequest()

    def get_news_data(self):
        url = "http://www.coindar.org"
        soup = bs4.BeautifulSoup(urlopen(url), 'lxml')
        return soup.find_all('div', {'class': 'calendar'})[0]

    def api_news1_last_events(self, limit=50):
        url = "https://coindar.org/api/v1/lastEvents?limit="+str(limit)
        return self.req.get_data(url)

    def api_news1_coin_events(self, name):
        url = "https://coindar.org/api/v1/coinEvents?name="+name
        # url = "https://coindar.org/api/v1/coinEvents?name=btc"
        return self.req.get_data(url)

    def api_news1_custom_date(self, year, month, day):
        url = "https://coindar.org/api/v1/events?year="+str(year)+"&month="+str(month)+"&day="+str(day)
        return self.req.get_data(url)
