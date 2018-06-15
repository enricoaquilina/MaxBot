#!/usr/bin/python3

from apis.news.coindar import *
from apis.news.coinmarketcal import *
from apis.prices.cmc import CoinMarketCap
from common.models.event_hunter.NewsEvent import NewsEvent


from common.database import sqlite
import datetime
# from datetime import datetime
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
        self.events_list = []
        self.processed_events = []

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

        self.dailies_updated = []
        for event in daily_events:

            price_usd, price_btc, change_24h, change_7d = self.cmc.get_asset_prices(event[5], event[6])
            event = NewsEvent(start_date=event[3], public_date=event[2], end_date=[4],
                              ticker=event[6], token=event[5], event=event[0],
                              price_usd=price_usd, price_btc=price_btc, change_24h=change_24h, change_7d=change_7d)
            self.dailies_updated.append(event)

        if time_of_day > 0:
            for event in self.dailies_updated:
                self.db.update_entry2(time_of_day, event.start_date,
                                     event.ticker, event.token,
                                     event.price_usd, event.price_btc,
                                     event.change_24h, event.change_7d)
                self.db.write()

    def extract_date_from_string(self, event, type):
        date = event[type]

        if len(date.split('-')) > 2:
            day = date.split('-')[2]
            if len(day.split(' ')) == 2:
                date = event[type].split('-')[0]+'-'+event[type].split('-')[1]+'-'+day.split()[0]

        # this is to get padded month and days which are less than 10
        if date != '':
            if len(date.split('-')) > 2:
                date = str(datetime.datetime.strptime(date, '%Y-%m-%d')).split(' ')[0]
            elif len(date.split('-')) == 2:
                # date = str(datetime.datetime.strptime(date, '%Y-%m')).split(' ')[0]
                return date
        return date

    def create_model(self, event):
        proof = event['proof']

        if 'coin_symbol' in event:
            ticker = event['coin_symbol']
            token = event['coin_name']
            event_title = event['caption']
            start_date = self.extract_date_from_string(event, 'start_date')
            public_date = self.extract_date_from_string(event, 'public_date')
            end_date = self.extract_date_from_string(event, 'end_date')
            return NewsEvent(start_date=start_date, public_date=public_date, end_date=end_date,
                             event_title=event_title, ticker=ticker, token=token, proof=proof)
        elif 'coins' in event:
            event_title = event['title']
            event_description = event['description']
            category = event['categories'][0]['name']
            ticker = event['coins'][0]['symbol']
            token = event['coins'][0]['name']
            start_date = self.extract_date_from_string(event, 'date_event')
            public_date = self.extract_date_from_string(event, 'created_date')
            vote_count = event['vote_count']
            pos_vote_count = event['positive_vote_count']
            percent = event['percentage']
            source = event['source']
            return NewsEvent(event_title=event_title, event_description=event_description, category=category,
                             ticker=ticker, token=token,
                             start_date=start_date, public_date=public_date,
                             vote_count=vote_count, pos_vote_count=pos_vote_count, percent=percent,
                             proof=proof, source=source)

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
        self.events_list = self.coindar.api_news1_last_events()
        self.events_list = sorted(self.events_list, key=lambda k: k['start_date'])
        self.events_list.extend(self.coinmarketcal.api_news2_get_events())

        # Process events
        for idx, event in enumerate(self.events_list):
            self.processed_events.append(self.create_model(event))

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
