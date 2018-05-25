#!/usr/bin/python3

from apis.news.coindar import *
from apis.news.coinmarketcal import *

from common.database import sqlite
import datetime
from common.models.event_hunter.CDModel import CDModel

# -*- coding: utf-8 -*-

class EventHunter:
    def __init__(self):
        self.news_events = set()
        self.events = []
        self.count = 1
        self.daily_events = set()
        self.coindar = CoinDar()
        self.coinmarketcal = CoinMarketCal()

    def clean_slate(self):
        self.news_events.clear()
        self.exists = False

    def write_to_csv(self):
        self.db = sqlite.DB()
        print('News events discovered: %s, News events to be stored: %s,' % (len(self.events_list), len(self.events)))

        for event_id, news_event in enumerate(self.events):
            self.db.insert_entry(news_event)

        self.db.write()
        self.db.close()

    def update_dailies(self, daily_events):
        self.db = sqlite.DB()

        timestamp = datetime.datetime.now().time()

        second_run = datetime.time(hour=6, minute=0)
        third_run = datetime.time(hour=12, minute=0)
        fourth_run = datetime.time(hour=18, minute=0)

        if timestamp < second_run:
            time_of_day = 0
        elif timestamp >= second_run and timestamp < third_run:
            time_of_day = 2
        elif timestamp >= third_run and timestamp < fourth_run:
            time_of_day = 3
        elif timestamp > fourth_run:
            time_of_day = 4

        if time_of_day > 0:
            for event in daily_events:
                self.db.update_entry(time_of_day, event.date,
                                     event.ticker, event.token,
                                     event.price_usd, event.price_btc,
                                     event.change_24h, event.change_7d)
                self.db.write()

    def create_model(self, event):
        ticker = event['coin_symbol']
        token = event['coin_name']
        news = event['caption']
        proof = event['proof']
        end_date = event['end_date']
        start_date = event['start_date']
        public_date = event['public_date']
        # category = ??

        return CDModel(news, proof, public_date, start_date, end_date, token, ticker)

    def cluster_events(self, start_date, event):
        if len(self.events) == 0:
            self.events[start_date] = [event]
        elif start_date not in self.events:
            self.events[start_date] = [event]
        else:
            self.events[start_date].append(event)

    def run(self):
        # self.events_list = self.coindar.get_news_data()
        self.events_list = self.coindar.api_news1_last_events()
        # self.test2 = self.coindar.api_news1_coin_events("btc")
        # self.test3 = self.coindar.api_news1_custom_date(2018,1,1)

        self.events_list = sorted(self.events_list, key=lambda k: k['start_date'])

        # Coinmarketcal API
        # self.test4 = self.coinmarketcal.api_news2_get_access_token()
        # self.test5 = self.coinmarketcal.api_news2_get_list_of_coins()
        # self.test6 = self.coinmarketcal.api_news2_get_categories()
        # self.test7 = self.coinmarketcal.api_news2_get_events()

        # print('Starting news hunter job (' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ')')
        self.events = {}
        start_date = ''

        for idx, raw_event in enumerate(self.events_list):
            event = self.create_model(raw_event)

            # process and cluster start_date(remove time)
            if start_date != raw_event['start_date']:
                start_date = raw_event['start_date']

            self.cluster_events(start_date, event)

        # now we need to check if events exist or not
        # if they do -> do nothing
        # if not -> save them!


        self.write_to_csv()
        self.update_dailies(self.daily_events)
        self.events.clear()
        self.events_list.clear()
        print('Finished news hunter job (' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ')')
        print('________________________________________________________________________')


test = EventHunter()
test.run()
