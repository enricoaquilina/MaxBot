#!/usr/bin/python3
import sys
# sys.path.insert(0, '/home/p3rditus/Desktop/MaxBot')

import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dateutil.parser import parse

from apis.news.coinmarketcal import CoinMarketCal
from apis.news.coindar import CoinDar

from apis.prices.coinmarketcap import CoinMarketCap
from apis.prices.coingecko import CoinGecko

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
        # get APIs needed
        self.coinmarketcal = CoinMarketCal()
        self.coindar = CoinDar()
        self.coinmarketcap = CoinMarketCap()
        self.coingecko = CoinGecko()

        self.events = {}
        self.events_list = []
        self.processed_events = []
        self.dailies_updated = []

        self.news_collection = cfg.settings['coll_news_events']
        self.run_id = self.helper.options['GET_RUN']()
        
        self.db = mongo.DB(cfg.settings['db_name'])

    def get_financials(self, token_name, token_symbol):
        financial_info = {}

        if self.coingecko.does_coin_exist(token_name, token_symbol):
            financial_info['coingecko'] = self.coingecko.get_coin_financials()

        if self.coinmarketcap.does_coin_exist(token_name, token_symbol): 
            financial_info['coinmarketcap'] = self.coinmarketcap.get_financials(token_symbol)
        
        return financial_info

    def update_event(self, event):
        token_events = 0
        for asset in event['financials'].keys():
            new_field = f'financials.{asset}.run{self.run_id}'
            new_info = self.get_financials(event['token_details'][asset]['name'], event['token_details'][asset]['symbol'])

            result = self.db.create_financial_event(self.news_collection, event, new_field, new_info)
            
            token_events += 1 if result['ok'] == 1 else token_events

        return '{}/{}\n'.format(token_events, len(event['financials'].keys()))

    def update_dailies(self):
        summary = ''
        dailies = self.db.get_events_for_today(self.news_collection)

        for idx, event in enumerate(dailies):
            summary += 'Event {}: '.format(idx+1) + self.update_event(event)

        self.helper.options['UPDATE'](summary, dailies.count())


    def insert_upcoming(self):
        count = 0
        for event in self.events.values():
            for e in event:
                result = self.db.insert_event(self.news_collection, e)
                count += result['n']

        self.helper.options['INSERT'](count)

    def update_existing(self, existing_event, new_event):
        old_fields = set(vars(existing_event).keys())
        new_fields = set(vars(new_event).keys())

        for field in new_fields:
            if field not in old_fields:
                vars(existing_event)[field] = vars(new_event)[field]
        
        return existing_event

    def create_cluster(self, new_event):
        date = new_event.event_date.date()

        if str(date) not in self.events:
            self.events[str(date)] = []
        
        # if event does not exist, insert
        events_to_compare = self.events[str(date)]

        found = False
        for existing_event in events_to_compare:
            # check both events and if they're similar, update existing
            if str(existing_event.event_date.date()) == str(date) and existing_event.category == new_event.category and\
                next(iter(existing_event.financials.keys())) == next(iter(new_event.financials.keys())):
                existing_event = self.update_existing(existing_event, new_event)
                found = True
        
        # if we encounter new event, insert here
        if not found:
            self.events[str(date)].append(new_event)

    def group_events(self):
        for event in self.processed_events:
            if event.event_date.date() >= dt.datetime.today().date():
                self.create_cluster(event)

    def create_model(self, event):
        if 'coin_id' in event:
            return self.coindar.build_model(event)
        if 'coins' in event:
            return self.coinmarketcal.build_model(event)

    def process_events(self):
        for event in self.events_list:
            self.processed_events.append(self.create_model(event))
        self.processed_events = sorted(self.processed_events, key=lambda k: dt.datetime.strftime(k.event_date, '%Y-%m-%d'))

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
# test and clean config file

# once using coingecko, add extra fields (developer activity and social sentiment)

# refactor, especially coindar and coingecko

# dont update events' same prices more than once
# clarify event source instead of relying on one single attribute (coin_id)

# it's a test