from common.http import request
from common.models.event_hunter.NewsEvent import NewsEvent
from common.utilities.helper import Helper
import requests
import datetime as dt

class CoinMarketCal:

    def __init__(self):
        self.req = request.MyRequest()
        self.helper = Helper()

        self.urls = {
            'COINMARKETCAL_DAILY_EVENTS':   'https://developers.coinmarketcal.com/v1/events',
            'COINMARKETCAL_COIN_LIST':      'https://developers.coinmarketcal.com/v1/coins',
            'COINMARKETCAL_CATEGORY_LIST':  'https://developers.coinmarketcal.com/v1/categories',
        }
    
    def get_coins(self):
        return self.req.get_data(self.urls['COINMARKETCAL_COIN_LIST'])

    def get_categories(self):
        return self.req.get_data(self.urls['COINMARKETCAL_CATEGORY_LIST'])

    def get_events(self):
        return self.req.get_data(self.urls['COINMARKETCAL_DAILY_EVENTS'])

    def build_model(self, event):
        financials = {}

        for coin in event['coins']:
            financials[coin['symbol']] = {}

        if event['categories'] is None:
            event['categories'] = [{'id': 0, 'name': 'N/A'}]

        tokens = {}

        for coin in event['coins']:
            tokens[coin['symbol']] = {
                'id': coin['id'],
                'name': coin['name'],
                'symbol': coin['symbol'],
                'full_name': coin['fullname'],
            }

        event = {
            'event_title': event['title'],
            'category': event['categories'][0]['name'],
            'event_date': self.helper.process_date(event, 'date_event'),
            'source': event['source'],
            'can_occur_before': event['can_occur_before'],
            'proof': event['proof'],
            'token_details': tokens,
            'financials': financials,
            'created_date': dt.datetime.now()
        }

        # event_description = event['description']
        # public_date = self.helper.process_date(event, 'created_date')
        # vote_count = event['vote_count']
        # pos_vote_count = event['positive_vote_count']
        # percent = event['percentage']

        return event
        # return NewsEvent(event_title=event_title, category=category,
        #                  coins=coins, event_date=event_date, proof=proof, source=source)
