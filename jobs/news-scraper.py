#!/usr/bin/python3

from apis.news.coindar import *
from apis.news.coinmarketcal import *
from apis.prices.cmc import CoinMarketCap
from common.models.event_hunter.NewsEvent import NewsEvent
from common.database import mongo


import time
import dateutil.parser as parser
from datetime import date
import datetime

# -*- coding: utf-8 -*-


class NewsScraper:
    def __init__(self):
        self.news_events = set()
        self.events = []
        self.count = 1
        self.daily_events = set()
        self.coindar = CoinDar()
        # self.coinmarketcal = CoinMarketCal()
        self.cmc = CoinMarketCap()

    def clean_slate(self):
        self.news_events.clear()
        self.exists = False

    def write_to_csv(self):
        self.db = mongo.DB('events')
        print('News events discovered: %s, News events to be stored: %s,' % (len(self.events_list), len(self.events)))

        for event_id, news_event in enumerate(self.events):
            self.db.insert_entry(news_event)

        self.db.write()
        self.db.close()

    def update_dailies(self, daily_events):
        self.db = mongo.DB('events')

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
                self.db.update_entry(time_of_day, event.start_date,
                                     event.ticker, event.token,
                                     event.price_usd, event.price_btc,
                                     event.change_24h, event.change_7d)
            self.db.write()

    def get_element_children(self, child_element, dom_type, class_name):
        return len(child_element.find_all(dom_type, {'class': class_name}))

    def run(self):
        self.events_list = self.coindar.get_news_data()
        self.test = self.coindar.api_news1_last_events()
        self.test2 = self.coindar.api_news1_coin_events("btc")
        self.test3 = self.coindar.api_news1_custom_date(2018,1,1)

        self.test4 = self.coinmarketcal.api_news2_get_access_token()
        self.test5 = self.coinmarketcal.api_news2_get_list_of_coins()
        self.test6 = self.coinmarketcal.api_news2_get_categories()
        self.test7 = self.coinmarketcal.api_news2_get_events()

        print('Starting news scraper job (' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ')')

        for idx, child in enumerate(self.events_list):
            if type(child) is bs4.element.Tag:
                if self.get_element_children(child, 'span', 'day') > 0:
                    if len(child.contents) == 3:
                        event_date = parser.parse(str(child.contents[1].contents[0]).strip().replace(',', '')).strftime("%d/%m/%Y")
                    else:
                        event_date = parser.parse(str(child.contents[3].contents[0]).strip().replace(',', '')).strftime(
                            "%d/%m/%Y")
                    self.clean_slate()

                if self.get_element_children(child, 'div', 'coin') > 0:
                    ticker = child.contents[1].contents[3].contents[0]
                    if ticker not in self.news_events:
                        self.news_events.add(ticker)
                        exists = False
                    else:
                        exists = True

                    token = child.contents[1].contents[1].contents[0]

                    category = child.find_all('div', {'class': 'info'})[0].contents[1]\
                        .contents[-2].contents[-2].contents[1].text

                    news = child.find_all('div', {'class': 'info'})[0].contents[1].contents[1]\
                        .text.replace('\n', '').replace(',',' and')

                    # asset = self.cmc.get_asset(token, ticker)

                    # if asset:
                    price_usd, price_btc, change_24h, change_7d = self.cmc.get_asset_prices(token, ticker)

                    if not exists:
                        event = NewsEvent(start_date=event_date, public_date=time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime()),
                                          ticker=ticker, token=token, event_description=news, category=category,
                                          price_usd=price_usd, price_btc=price_btc,
                                          change_24h=change_24h, change_7d=change_7d)
                        self.events.append(event)

                        if datetime.datetime.strptime(event_date, '%d/%m/%Y').date() == date.today():
                            self.daily_events.add(event)
                    else:
                        event = [event for event in self.events if event.ticker == ticker]
                        if len(event) > 0:
                            event[0].event += ' AND ' + news

        self.write_to_csv()
        self.update_dailies(self.daily_events)
        self.events.clear()
        self.events_list.clear()
        print('Finished news scraper job (' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ')')
        print('________________________________________________________________________')


test = NewsScraper()
test.run()
