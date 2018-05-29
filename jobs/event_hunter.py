#!/usr/bin/python3

from apis.news.coindar import *
from apis.news.coinmarketcal import *
from apis.prices.cmc import CoinMarketCap
from common.models.event_hunter.NewsEvent import NewsEvent


from common.database import sqlite
import datetime
from dateutil.parser import parse

# -*- coding: utf-8 -*-

class EventHunter:
    def __init__(self):
        self.news_events = set()
        self.events = []
        self.count = 1
        self.daily_events = set()
        self.coindar = CoinDar()
        self.coinmarketcal = CoinMarketCal()
        self.cmc = CoinMarketCap()

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

    def update_dailies(self):
        self.db = sqlite.DB('news_events')

        timestamp = datetime.datetime.now().time()
        daily_events = self.db.get_events_for_today(datetime.date.today())

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

        self.dailies_updated = []
        for event in daily_events:

            price_usd, price_btc, change_24h, change_7d = self.cmc.get_asset_prices(event[5], event[6])
            event = NewsEvent(date=event[3], ticker=event[6], token=event[5],
                              price_usd=price_usd, price_btc=price_btc, change_24h=change_24h, change_7d=change_7d)
            self.dailies_updated.append(event)

        if time_of_day > 0:
            for event in self.dailies_updated:
                self.db.update_entry(time_of_day, event.date,
                                     event.ticker, event.token,
                                     event.price_usd, event.price_btc,
                                     event.change_24h, event.change_7d)
                self.db.write()

    def extract_date_from_string(self, date, type):
        extracted = date[type]
        if len(date[type].split('-')) > 2:
            day = date[type].split('-')[2]
            if len(day.split(' ')) == 2:
                extracted = date[type].split('-')[0]+'-'+date[type].split('-')[1]+'-'+day.split()[0]
        return extracted

    def create_model(self, event):
        ticker = event['coin_symbol']
        token = event['coin_name']
        news = event['caption']
        proof = event['proof']
        end_date = self.extract_date_from_string(event, 'end_date')
        start_date = self.extract_date_from_string(event, 'start_date')
        public_date = self.extract_date_from_string(event, 'public_date')
        # category = ??

        return NewsEvent(start_date, public_date, ticker, token, news, proof=proof)

    def cluster_events(self, start_date, event):
        if len(self.events) == 0:
            self.events[start_date] = [event]
        elif start_date not in self.events:
            self.events[start_date] = [event]
        else:
            self.events[start_date].append(event)

    def insert_upcoming(self):
        self.db = sqlite.DB('news_events')

        for date, event in self.events.items():
            if len(event) == 1:
                self.db.check_or_insert(event[0])
            else:
                for e in event:
                    self.db.check_or_insert(e)

        self.db.write()

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
            if parse(raw_event['start_date']).date() >= datetime.date.today():
                event = self.create_model(raw_event)

                # process and cluster start_date(remove time)
                if start_date != raw_event['start_date']:
                    start_date = self.extract_date_from_string(raw_event, 'start_date')

                self.cluster_events(start_date, event)

        # now we need to check if events exist or not
        # if they do -> do nothing
        # if not -> save them!

        self.insert_upcoming()
        self.update_dailies()


        # self.write_to_csv()
        self.events.clear()
        self.events_list.clear()
        print('Finished news hunter job (' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ')')
        print('________________________________________________________________________')


test = EventHunter()
test.run()
