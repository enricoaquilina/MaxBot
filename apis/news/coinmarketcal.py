from common.http import request
from common.models.event_hunter.model_event import NewsEvent 
from common.utilities.helper import Helper
import config.news as cfg

class CoinMarketCal:

    def __init__(self):
        self.req = request.MyRequest()
        self.helper = Helper()
        self.headers = { 'x-api-key': cfg.settings['COINMARKETCAL']['AUTH']['x-api-key']}
    
    def get_coins(self):
        return self.req.get_data(cfg.settings['COINMARKETCAL']['URLs']['COINS']['LINK'], self.headers)

    def get_categories(self):
        return self.req.get_data(cfg.settings['COINMARKETCAL']['URLs']['CATEGORIES']['LINK'], self.headers)

    def get_events(self):
        return sorted(
            self.req.get_data(cfg.settings['COINMARKETCAL']['URLs']['EVENTS']['LINK'], 
            self.headers, cfg.settings['COINMARKETCAL']['URLs']['EVENTS']['ARGS']), key=lambda k: k['date_event'])

    def build_model(self, event):
        self.event = dict(event)
        self.event['origin']         = 'coinmarketcal'
        self.event['category']       = ['N/A'] if 'categories' not in event else event['categories'][0]['name']
        self.event['event_date']     = self.helper.process_date(event, 'date_event')
        self.event['event_title']    = next(iter(event['title'].values()))

        self.event['financials'] = {}
        self.event['token_details'] = {}

        for coin in event['coins']:
            if coin['fullname'] != 'General Event (CRYPTO)' and coin['symbol'] != 'CRYPTO' and coin['name'] != 'General Event' and coin['id'] != 'cryptocurrencies':
                self.event['financials'][coin['symbol']] = {}

                self.event['token_details'][coin['symbol']] = {
                    'id': coin['id'],
                    'name': coin['name'],
                    'symbol': coin['symbol'],
                    'full_name': coin['fullname'],
                }

        return NewsEvent(self.event)
        
 