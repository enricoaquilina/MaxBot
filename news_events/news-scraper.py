# import bs4
# import time
# import math
# from apis.cmc import get_asset
# from apis.news.coindar import get_news_data
# from database import sqlite
# import dateutil.parser as parser
# from datetime import date
# import datetime
# from models.NewsEvent import NewsEvent
#
# # -*- coding: utf-8 -*-
# import sys
# import codecs
#
# class NewsScraper:
#     def __init__(self):
#         self.news_events = set()
#         self.events = []
#         self.count = 1
#         self.daily_events = set()
#         # 6 hours
#         # self.TIME_TO_SLEEP = 21600
#         self.TIME_TO_SLEEP = 1
#
#     def clean_slate(self):
#         self.news_events.clear()
#         self.exists = False
#
#     def write_to_csv(self):
#         self.db = sqlite.DB()
#         print('\nStoring info...')
#         for event_id, news_event in enumerate(self.events):
#             if event_id == math.floor((len(self.events)) * 0.5):
#                 print('Progress 50%%(%s news events)' % str(len(self.events)))
#
#             self.db.insert_entry(news_event)
#         self.db.write()
#         self.db.close()
#
#     def update_dailies(self, time_of_day, daily_events):
#         self.db = sqlite.DB()
#
#         if time_of_day > 1:
#             for event in daily_events:
#                 self.db.update_entry(time_of_day, event.date,
#                                      event.ticker, event.token,
#                                      event.price_usd, event.price_btc,
#                                      event.change_24h, event.change_7d)
#                 self.db.write()
#
#     def get_element_children(self, child_element, dom_type, class_name):
#         return len(child_element.find_all(dom_type, {'class': class_name}))
#
#
#     def run(self):
#         while True:
#             print('Starting to gather info...')
#             print('Identified %s news events' % len(get_news_data()))
#
#             for idx, child in enumerate(get_news_data()):
#
#                 if idx == math.floor((len(get_news_data())) * 0.5):
#                     print('Progress 50%%(%s news events)' % str(len(get_news_data())))
#
#                 if type(child) is bs4.element.Tag:
#                     if self.get_element_children(child, 'span', 'day') > 0:
#                         event_date = parser.parse(str(child.contents[1].contents[0]).strip().replace(',', '')).strftime("%d/%m/%Y")
#                         self.clean_slate()
#
#                     if self.get_element_children(child, 'div', 'coin') > 0:
#                         ticker = child.contents[1].contents[3].contents[0]
#                         if ticker not in self.news_events:
#                             self.news_events.add(ticker)
#                             exists = False
#                         else:
#                             exists = True
#
#                         token = child.contents[1].contents[1].contents[0]
#                         if len(child.find_all('div', {'class': 'info'})[0].contents[5].contents) > 1:
#                             element_count = len(child.find_all('div', {'class': 'info'})[0].contents[-2])
#                             if element_count == 3:
#                                 category = child.find_all('div', {'class': 'info'})[0].contents[-2]\
#                                     .contents[1].text
#                             else:
#                                 category = child.find_all('div', {'class': 'info'})[0].contents[-2]\
#                                     .contents[0].strip()
#                         else:
#                             category = 'N/A'
#
#                         if len(child.find_all('div', {'class': 'info'})[0].contents[1].contents[1].contents[0].contents) > 0:
#                             news = child.find_all('div', {'class': 'info'})[0].contents[1].contents[1].contents[0].contents[0] \
#                                 .replace(',', ' and')
#                         else:
#                             news = child.find_all('div', {'class': 'info'})[0].contents[1].contents[3].contents[0].contents[0]
#
#
#                         asset = get_asset(token, ticker)
#
#                         if asset:
#                             if 'price_usd' in asset[0]:
#                                 price_usd = asset[0]['price_usd']
#                             if 'price_btc' in asset[0]:
#                                 price_btc = asset[0]['price_btc']
#                             if 'percent_change_24h' in asset[0]:
#                                 if asset[0]['percent_change_24h'] is not None:
#                                     change_24h = asset[0]['percent_change_24h']
#                                 else:
#                                     change_24h = 'NULL'
#                             if 'percent_change_7d' in asset[0]:
#                                 if asset[0]['percent_change_7d'] is not None:
#                                     change_7d = asset[0]['percent_change_7d']
#                                 else:
#                                     change_7d = 'NULL'
#
#
#                             if not exists:
#                                 event = NewsEvent(event_date, ticker,
#                                                   token, news,
#                                                   category, price_usd,
#                                                   price_btc, change_24h, change_7d)
#                                 self.events.append(event)
#
#                                 if datetime.datetime.strptime(event_date, '%d/%m/%Y').date() == date.today():
#                                     self.daily_events.add(event)
#
#
#                             else:
#                                 event = [event for event in self.events if event.ticker == ticker]
#                                 event[0].event += ' AND ' + news
#
#             self.write_to_csv()
#             self.update_dailies(self.daily_events)
#             self.events.clear()
#             print('\nSleeping for '+str(self.TIME_TO_SLEEP/60/60)+' hours ('+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))+')')
#             print('zzzzzz...zzzzzzzzzzzzzz...zzzzz..')
#             self.count += 1
#             if self.count > 4:
#                 self.count = 0
#             time.sleep(self.TIME_TO_SLEEP)
#
#
# test = NewsScraper()
# test.run()
