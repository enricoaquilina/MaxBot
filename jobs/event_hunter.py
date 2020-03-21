#!/usr/bin/python3
import sys
# sys.path.insert(0, '/home/p3rditus/Desktop/MaxBot')

import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dateutil.parser import parse

# from apis.news.coindar import *
from apis.news.coinmarketcal import *
from apis.prices.coinmarketcap import CoinMarketCap

from common.utilities.helper import Helper
from common.database import mongo



# -*- coding: utf-8 -*-

class EventHunter:

    def __init__(self):
        self.set_local_vars()

    def set_local_vars(self):
        self.helper = Helper()
        self.coinmarketcap = CoinMarketCap()
        self.coinmarketcal = CoinMarketCal()
        # self.coindar = CoinDar()

        self.events = {}
        self.events_list = []
        self.processed_events = []
        self.dailies_updated = []

        self.news_collection = 'news_events'
        self.events_collection = 'events'
        self.run_id = self.helper.options['GET_RUN']()
        
        self.db = mongo.DB('maxbot')

    def get_financials(self, token):
        return self.coinmarketcap.get_financials(token)

    def update_event(self, event):
        for asset in event['financials'].keys():

            new_field = f'financials.{asset}.run{self.run_id}'
            new_info = self.get_financials(asset)

            self.db.create_financial_event(self.news_collection, event, new_field, new_info)

    def update_dailies(self):
        dailies = self.db.get_events_for_today(self.news_collection)

        for event in dailies:
            self.update_event(event)

    def insert_upcoming(self):
        for event in self.events.values():
            for e in event:
                self.db.insert_event(self.news_collection, e)

    def create_cluster(self, event):
        if event.event_date not in self.events:
            self.events[event.event_date] = []
        
        self.events[event.event_date].append(event)

    def group_events(self):
        for event in self.processed_events:
            if parse(event.event_date).date() >= dt.date.today():
                self.create_cluster(event)

    def create_model(self, event):
        # if 'coin_symbol' in event:
        #     return self.coindar.build_model(event)
        if 'coins' in event:
            return self.coinmarketcal.build_model(event)

    def process_events(self):
        for event in self.events_list:
            self.processed_events.append(self.create_model(event))

    def get_raw_data(self):
        # if self.coindar:
        #     self.events_list = sorted(self.coindar.api_news1_last_events(), key=lambda k: k['start_date'])

        if self.coinmarketcal:
            self.events_list.extend(sorted(self.coinmarketcal.get_events(), key=lambda k: k['date_event']))

    def run(self):
        self.helper.options['START']()

        # get events from APIs
        self.get_raw_data()

        # process events and 'clean' them
        self.process_events()

        # group them and touch the database
        self.group_events()
        self.insert_upcoming()
        self.update_dailies()
        
        self.helper.options['FINISH']([self.events, self.events_list,
                                       self.dailies_updated, self.processed_events,
                                       self.dailies_updated])

hunter = EventHunter()
hunter.run()
