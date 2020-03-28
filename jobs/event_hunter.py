#!/usr/bin/python3
import sys
# sys.path.insert(0, '/home/p3rditus/Desktop/MaxBot')

import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dateutil.parser import parse

from apis.news.coinmarketcal import *
from apis.prices.coinmarketcap import CoinMarketCap
from apis.news.coindar import CoinDar

from common.utilities.helper import Helper
from common.database import mongo
import common.config as cfg

import datetime as dt

# -*- coding: utf-8 -*-

class EventHunter:

    def __init__(self):
        self.set_local_vars()

    def set_local_vars(self):
        self.helper = Helper()
        self.coinmarketcap = CoinMarketCap()
        self.coinmarketcal = CoinMarketCal()
        self.coindar = CoinDar()

        self.events = {}
        self.events_list = []
        self.processed_events = []
        self.dailies_updated = []

        self.news_collection = cfg.settings['coll_news_events']
        self.run_id = self.helper.options['GET_RUN']()
        
        self.db = mongo.DB(cfg.settings['db_name'])

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
        date = parse(event.event_date).date()
        if str(date) not in self.events:
            self.events[str(date)] = []
        
        # if event does not exist, insert
        events_to_compare = self.events[str(date)]

        found = False
        for e in events_to_compare:
            # check both events and if they're not similar, insert
            # otherwise pass
            if e.event_date == str(date) and next(iter(e.financials.keys())) == next(iter(event.financials.keys())):
                found = True
            
        if not found:
            self.events[str(date)].append(event)

    def group_events(self):
        for event in self.processed_events:
            if parse(event.event_date).date() >= dt.date.today():
                self.create_cluster(event)

    def create_model(self, event):
        if 'coin_id' in event:
            return self.coindar.build_model(event)
        if 'coins' in event:
            return self.coinmarketcal.build_model(event)

    def process_events(self):
        for event in self.events_list:
            self.processed_events.append(self.create_model(event))
        self.processed_events = sorted(self.processed_events, key=lambda k: parse(k.event_date).date())

    def get_raw_data(self):
        if self.coindar:
            self.events_list = self.coindar.get_events()

        if self.coinmarketcal:
            self.events_list.extend(self.coinmarketcal.get_events())

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


# TODO
# check for repeated events in 2nd API
# dont update events' same prices more than once

# remove social counts which are 0 and sites which are empty
# clarify event source instead of relying on one single attribute (coin_id)
# move token details, financials to coinmarketcal
