from common.http import request
from common.models.event_hunter.NewsEvent import NewsEvent
from common.utilities.helper import Helper
import requests


class CoinMarketCal:

    def __init__(self):

        self.req = request.MyRequest()
        self.helper = Helper()
        self.headers = {
            'x-api-key': "iFQY61z1SD4PanhjChc8E4RMo4KdUHdT5AXCx8Y8",
            'Accept-Encoding': "deflate, gzip",
            'Accept': "application/json"
        }

    def get_coins(self):
        url = "https://developers.coinmarketcal.com/v1/coins"
        # querystring = {"max": "10", "coins": "bitcoin"}
        querystring = {}
        payload = ""

        response = requests.request("GET", url, data=payload, headers=self.headers, params=querystring)
        # return self.req.get_data(url)
        return response.json()

    def get_categories(self):
        url = "https://developers.coinmarketcal.com/v1/categories"
        # querystring = {"max": "10", "coins": "bitcoin"}
        querystring = {}
        payload = ""

        response = requests.request("GET", url, data=payload, headers=self.headers, params=querystring)
        # return self.req.get_data(url)
        return response.json()

    def get_events(self):
        url = "https://developers.coinmarketcal.com/v1/events"
        # querystring = {"max": "10", "coins": "bitcoin"}
        querystring = {}
        payload = ""

        response = requests.request("GET", url, headers=self.headers, params=querystring)
        # return self.req.get_data(url)
        return response.json()['body']

    def build_model(self, event):
        coins = {}
        if len(event['coins']) == 2:
            coins[event['coins'][1]['symbol']] = event['coins'][1]['name']
        elif len(event['coins']) > 2:
            for coin in event['coins'][1:]:
                coins[coin['symbol']] = coin['name']
        else:
            coins[event['coins'][0]['symbol']] = event['coins'][0]['name']

        event = {
            'event_title': event['title'],
            'category': event['categories'][0]['name'],
            'event_date': self.helper.process_date(event, 'date_event'),
            'source': event['source'],
            'proof': event['proof'],
            'coins': coins
        }

        # event_description = event['description']
        # public_date = self.helper.process_date(event, 'created_date')
        # vote_count = event['vote_count']
        # pos_vote_count = event['positive_vote_count']
        # percent = event['percentage']

        return event
        # return NewsEvent(event_title=event_title, category=category,
        #                  coins=coins, event_date=event_date, proof=proof, source=source)
