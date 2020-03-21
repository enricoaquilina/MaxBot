from common.http import request
from common.models.event_hunter.model_event import NewsEvent 
from common.utilities.helper import Helper
import datetime as dt
import common.config as cfg


class CoinMarketCal:

    def __init__(self):
        self.req = request.MyRequest()
        self.helper = Helper()
        self.headers = { 'x-api-key': cfg.settings['x-api-key']}
    
    def get_coins(self):
        return self.req.get_data(cfg.settings['COINMARKETCAL_COIN_LIST'], self.headers)

    def get_categories(self):
        return self.req.get_data(cfg.settings['COINMARKETCAL_CATEGORY_LIST'], self.headers)

    def get_events(self):
        return self.req.get_data(cfg.settings['COINMARKETCAL_DAILY_EVENTS'], self.headers)

    def build_model(self, event):
        event['category']       = ['N/A'] if event['categories'] is None else event['categories'][0]['name']
        event['event_date']     = self.helper.process_date(event, 'date_event')
        event['created_date']   = dt.datetime.now()

        return NewsEvent(event)
        
 