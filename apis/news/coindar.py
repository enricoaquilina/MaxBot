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
            cfg.settings['COINDAR_HEADER'], 
            { **cfg.settings['COINDAR_TOKEN'], **cfg.settings['COINDAR_EVENTS_ARGS'] }
        )
        return self.filter_events(events)


    def get_tags(self):
        return self.req.get_data(
            cfg.settings['COINDAR_TAGS_URL'], 
            cfg.settings['COINDAR_HEADER'], 
            cfg.settings['COINDAR_TOKEN']
        )

    def get_coins(self):
        return self.req.get_data(
            cfg.settings['COINDAR_COINS_URL'], 
            cfg.settings['COINDAR_HEADER'], 
            cfg.settings['COINDAR_TOKEN']
        )

    def get_socials(self):
        return self.req.get_data(
            cfg.settings['COINDAR_SOCIAL_URL'], 
            cfg.settings['COINDAR_HEADER'], 
            cfg.settings['COINDAR_TOKEN']
        )

    def aggregate_details(self):
        
        token_details = list(filter(lambda d: d['id'] == self.event['coin_id'], self.coins))[0]
        self.event['token_details'] = {
            'name':     token_details['name'],
            'symbol':    token_details['symbol']
        }
        self.event['financials'] = {}
        self.event['financials'][token_details['symbol']] = {
        }
        socials = list(filter(lambda d: d['coin_id'] == self.event['coin_id'], self.socials))[0]
        self.event['socials'] = {
            'bitcointalk':  socials['bitcointalk'],
            'facebook':     socials['facebook'],
            'github':       socials['github'],
            'reddit':       socials['reddit'],
            'telegram':     socials['telegram'],
            'youtube':      socials['youtube'],
            'twitter':      socials['twitter'],
            'explorer':     socials['explorer'],
            'website':     socials['website'],
            'counts': {
                "facebook": socials['facebook_count'],
                "telegram": socials['telegram_count'],
                "twitter":  socials['twitter_count'],
                "reddit":  socials['reddit_count'],
            }
        }


    def build_model(self, event):
        self.event = dict(event)
        self.event['origin']         = 'coindar'
        self.event['category']       = list(filter(lambda d: d['id'] == event['tags'], self.tags))[0]['name']

        self.event['event_date']     = self.helper.process_date(event, 'date_start')
        
        if self.helper.process_date(event, 'date_end') is not None:
            self.event['end_date'] = self.helper.process_date(event, 'date_end')

        self.event['event_title']    = event.pop('caption')

        self.aggregate_details()

        return NewsEvent(self.event)