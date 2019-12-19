#!/usr/bin/python3
# import sys
# sys.path.insert(0, '/home/pi/Desktop/')
import datetime as dt
from dateutil.parser import parse

from apis.news.coindar import *
from apis.news.coinmarketcal import *
from apis.prices.cmc import CoinMarketCap

from common.models.event_hunter.NewsEvent import NewsEvent
from common.utilities.helper import Helper
from common.database import mongo



# -*- coding: utf-8 -*-


class EventHunter:
    def __init__(self):
        # APIs needed
        self.helper = Helper()

        self.coinmarketcap = CoinMarketCap()
        self.cm_cal = CoinMarketCal()
        # self.coindar = CoinDar()

        # data structures needed
        self.events = {}
        self.events_list = []
        self.processed_events = []
        self.dailies_updated = []

        self.news_collection = 'news_events'
        self.events_collection = 'events'

        self.db = mongo.DB('MaxBotDB')

    def update_dailies(self):
        daily_events = self.db.get_events_for_today(self.news_collection)

        second_run = dt.time(hour=6, minute=0)
        third_run = dt.time(hour=12, minute=0)
        fourth_run = dt.time(hour=18, minute=0)

        timestamp = dt.datetime.now().time()

        if timestamp < second_run:
            time_of_day = 1
        elif timestamp >= second_run and timestamp < third_run:
            time_of_day = 2
        elif timestamp >= third_run and timestamp < fourth_run:
            time_of_day = 3
        elif timestamp > fourth_run:
            time_of_day = 4


        for event_to_update in daily_events:

            for token_to_update, financials in event_to_update['financials'].items():
                price_usd, price_btc, \
                volume_usd_24h, volume_btc_24h, \
                change_usd_1h, change_btc_1h, \
                change_usd_24h, change_btc_24h, \
                change_usd_7d, change_btc_7d, \
                marketcap_usd, marketcap_btc = self.coinmarketcap.get_asset_financials(event_to_update)

                new_info = {
                    f'run_{time_of_day}': {
                        'USD': {
                            'price': price_usd,
                            'volume_24h': volume_usd_24h,
                            'change_1h': change_usd_1h,
                            'change_24h': change_usd_24h,
                            'change_7d': change_usd_7d,
                            'marketcap': marketcap_usd,
                        },
                        'BTC': {
                            'price': price_btc,
                            'volume_24h': volume_btc_24h,
                            'change_1h': change_btc_1h,
                            'change_24h': change_btc_24h,
                            'change_7d': change_btc_7d,
                            'marketcap': marketcap_btc,
                        },
                        'created_date': dt.datetime.now()
                    }
                }
                self.db.add_financial_event(self.news_collection, event_to_update, token_to_update, new_info)

        # self.dailies_updated.append(event)

        # if time_of_day > 0:
        # for event in self.dailies_updated:
        #     self.db.update_entry2(time_of_day, event.start_date,
        #                           event.ticker, event.token,
        #                           event.price_usd, event.price_btc,
        #                           event.change_24h, event.change_7d)
        #     self.db.write()

    def insert_upcoming(self):
        for date, event in self.events.items():
            for e in event:
                self.db.insert_event(self.news_collection, e)

    def create_cluster(self, start_date, event):
        if len(self.events) == 0:
            self.events[start_date] = [event]
        elif start_date not in self.events:
            self.events[start_date] = [event]
        else:
            self.events[start_date].append(event)

    def group_events(self):
        event_date = ''

        for idx, event in enumerate(self.processed_events):
            if parse(event['event_date']).date() >= dt.date.today():

                if event_date != event['event_date']:
                    event_date = event['event_date']

                # cluster events by date
                self.create_cluster(event_date, event)

    def create_model(self, event):
        if 'coin_symbol' in event:
            return self.coindar.build_model(event)
        elif 'coins' in event:
            return self.cm_cal.build_model(event)

    def process_events(self):
        for idx, event in enumerate(self.events_list):
            self.processed_events.append(self.create_model(event))

    def gather_raw_event_data(self):
        # if self.coindar:
        #     self.events_list = sorted(self.coindar.api_news1_last_events(), key=lambda k: k['start_date'])

        if self.cm_cal:
            self.events_list.extend(sorted(self.cm_cal.get_events(), key=lambda k: k['date_event']))

    def run(self):
        # get events from APIs
        self.gather_raw_event_data()

        # process events and 'clean' them
        self.process_events()

        self.helper.options['START']()

        self.group_events()

        self.insert_upcoming()
        self.update_dailies()

        self.helper.options['FINISH']([self.events, self.events_list,
                                       self.dailies_updated, self.processed_events,
                                       self.dailies_updated])


test = EventHunter()
test.run()
