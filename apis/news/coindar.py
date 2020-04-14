from common.http import request
from common.models.event_hunter.model_event import NewsEvent
from common.utilities.helper import Helper
import common.config as cfg

class CoinDar:
    def __init__(self):
        self.req = request.MyRequest()
        self.helper = Helper()
        self.get_all_info()

    def get_all_info(self):
        self.tags = self.get_tags()
        self.coins = self.get_coins()
        self.socials = self.get_socials()
        self.event = {}

    def filter_events(self, events):
        reliable_sources = list(filter(lambda d: d['source_reliable'] == 'true' and len(d['date_start'].split('-')) == 3, events))
        return sorted(reliable_sources, key=lambda k: k['date_start'])
        
    def get_events(self):
        events = self.req.get_data(
            cfg.settings['COINDAR_EVENTS_URL'], 
            params={ **cfg.settings['COINDAR_TOKEN'], **cfg.settings['COINDAR_EVENTS_ARGS'] }
        )
        return self.filter_events(events)


    def get_tags(self):
        return self.req.get_data(
            cfg.settings['COINDAR_TAGS_URL'], 
            params=cfg.settings['COINDAR_TOKEN']
        )

    def get_coins(self):
        return self.req.get_data(
            cfg.settings['COINDAR_COINS_URL'], 
            params=cfg.settings['COINDAR_TOKEN']
        )

    def get_socials(self):
        return self.req.get_data(
            cfg.settings['COINDAR_SOCIAL_URL'], 
            params=cfg.settings['COINDAR_TOKEN']
        )

    def compute_financials(self):
        self.event['financials'] = {}
        self.event['financials'][self.token_details['symbol']] = {
        }
    
    def compute_socials(self):
        socials = list(filter(lambda d: d['coin_id'] == self.event['coin_id'], self.socials))[0]
        socials = { k: v for k, v in socials.items() if v != '' and v != '0' }

        accounts = ['bitcointalk', 'facebook', 'github', 'reddit', 'telegram', 'youtube', 'twitter', 'explorer', 'website']
        counts = ['facebook_count', 'telegram_count', 'twitter_count', 'reddit_count']
        
        self.event['socials'] = {}
        self.event['socials']['accounts'] = {}
        self.event['socials']['counts'] = {}
        
        for attr in socials:
            if attr in accounts:
                self.event['socials']['accounts'][attr] = socials[attr] 
            if attr in counts:
                self.event['socials']['counts'][attr] = socials[attr]  

    def aggregate_details(self):
        self.event['token_details'] = {}
        self.event['token_details'][self.token_details['symbol']] = {
            'name': self.token_details['name'],
            'symbol':  self.token_details['symbol']
        }

        self.compute_financials()
        self.compute_socials()      


    def build_model(self, event):
        self.event = dict(event)
        self.token_details = list(filter(lambda d: d['id'] == self.event['coin_id'], self.coins))[0]

        self.event['origin']         = 'coindar'
        self.event['category']       = list(filter(lambda d: d['id'] == event['tags'], self.tags))[0]['name']

        self.event['event_date']     = self.helper.process_date(event, 'date_start')
        
        if self.helper.process_date(event, 'date_end') is not None:
            self.event['end_date'] = self.helper.process_date(event, 'date_end')

        self.event['event_title']    = event.pop('caption')

        self.aggregate_details()

        return NewsEvent(self.event)