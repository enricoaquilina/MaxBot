# import bs4
# from urllib.request import urlopen
# import requests
from common.http import request
from common.models.event_hunter.model_event import NewsEvent
from common.utilities.helper import Helper
import common.config as cfg

class CoinDar:
    # self.events_list = self.coindar.get_news_data()
    # self.test2 = self.coindar.api_news1_coin_events("btc")
    # self.test3 = self.coindar.api_news1_custom_date(2018,1,1)
    #

    def __init__(self):
        self.req = request.MyRequest()
        self.helper = Helper()
        self.get_news_data()

    def get_news_data(self):
        # url = "http://www.coindar.org"
        # soup = bs4.BeautifulSoup(urlopen(url), 'lxml')
        # return soup.find_all('div', {'class': 'event'})

        # access_token = '37949:XvvzaWNeECQuCXyJLZa'
        # url = f"https://coindar.org/api/v2/coins?access_token={access_token}"
        # querystring = {}
        # payload = ""

        # response = requests.request("GET", url, data=payload, params=querystring)
        # return response.json()
        pass


    def get_events(self, limit=50):
        # url = "https://coindar.org/api/v2/events?limit="+str(limit)
        return self.req.get_data(cfg.settings['COINDAR_EVENTS'], cfg.settings['COINDAR_HEADER'], cfg.settings['COINDAR_TOKEN'])


    def api_news1_coin_events(self, name):
        url = "https://coindar.org/api/v1/coinEvents?name="+name
        # url = "https://coindar.org/api/v1/coinEvents?name=btc"
        return self.req.get_data(url)

    def api_news1_custom_date(self, year, month, day):
        url = "https://coindar.org/api/v1/events?year="+str(year)+"&month="+str(month)+"&day="+str(day)
        return self.req.get_data(url)

    def build_model(self, event):
        ticker = event['coin_symbol']
        token = event['coin_name']
        event_title = event['caption']
        start_date = self.helper.process_date(event, 'start_date')
        public_date = self.helper.process_date(event, 'public_date')
        end_date = self.helper.process_date(event, 'end_date')
        proof = event['proof']

        return NewsEvent(event)
