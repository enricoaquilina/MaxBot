#!/usr/bin/python3
# import sys
# sys.path.insert(0, '/home/pi/Desktop/')
import datetime
from dateutil.parser import parse

from apis.news.coindar import *
from apis.news.coinmarketcal import *
from apis.prices.cmc import CoinMarketCap

from common.models.event_hunter.NewsEvent import NewsEvent
from common.utilities.helper import Helper
from common.database import sqlite


# -*- coding: utf-8 -*-


class EventHunter:
    def __init__(self):
        self.news_events = set()
        self.events = []
        self.count = 1
        self.daily_events = set()

        # APIs needed
        self.helper = Helper()

        self.cmc = CoinMarketCap()
        self.coindar = CoinDar()
        self.coinmarketcal = CoinMarketCal()

        # data structures needed
        self.events = {}
        self.events_list = []
        self.processed_events = []
        self.dailies_updated = []

    def update_dailies(self):
        self.db = sqlite.DB('news_events')

        daily_events = self.db.get_events_for_today()

        second_run = datetime.time(hour=6, minute=0)
        third_run = datetime.time(hour=12, minute=0)
        fourth_run = datetime.time(hour=18, minute=0)

        timestamp = datetime.datetime.now().time()

        if timestamp < second_run:
            time_of_day = 0
        elif timestamp >= second_run and timestamp < third_run:
            time_of_day = 2
        elif timestamp >= third_run and timestamp < fourth_run:
            time_of_day = 3
        elif timestamp > fourth_run:
            time_of_day = 4

        for event in daily_events:

            price_usd, price_btc, change_24h, change_7d = self.cmc.get_asset_prices(event[4], event[3])
            event = NewsEvent(start_date=event[5], public_date=event[6], end_date=event[7],
                              ticker=event[3], token=event[4], price_usd=price_usd, price_btc=price_btc,
                              change_24h=change_24h, change_7d=change_7d)
            self.dailies_updated.append(event)

        if time_of_day > 0:
            for event in self.dailies_updated:
                self.db.update_entry2(time_of_day, event.start_date,
                                     event.ticker, event.token,
                                     event.price_usd, event.price_btc,
                                     event.change_24h, event.change_7d)
                self.db.write()

    def insert_upcoming(self):
        self.db = sqlite.DB('news_events')

        for date, event in self.events.items():
            if len(event) == 1:
                self.db.check_or_insert(event[0])
            else:
                for e in event:
                    self.db.check_or_insert(e)
        self.db.write()

    def create_cluster(self, start_date, event):
        if len(self.events) == 0:
            self.events[start_date] = [event]
        elif start_date not in self.events:
            self.events[start_date] = [event]
        else:
            self.events[start_date].append(event)

    def group_events(self):
        start_date = ''

        for idx, event in enumerate(self.processed_events):
            if parse(event.start_date).date() >= datetime.date.today():

                if start_date != event.start_date:
                    start_date = event.start_date

                # cluster events by date
                self.create_cluster(start_date, event)

    def create_model(self, event):
        if 'coin_symbol' in event:
            return self.coindar.build_model(event)
        elif 'coins' in event:
            return self.coinmarketcal.build_model(event)

    def process_events(self):
        for idx, event in enumerate(self.events_list):
            self.processed_events.append(self.create_model(event))

    def gather_raw_event_data(self):
        self.events_list = self.coindar.api_news1_last_events()
        self.events_list = sorted(self.events_list, key=lambda k: k['start_date'])

        other_news = self.coinmarketcal.api_news2_get_events()
        self.events_list.extend(sorted(other_news, key=lambda k: k['date_event']))

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
