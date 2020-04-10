import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import urllib
from urllib.request import urlopen, Request
import datetime as dt
import common.config as cfg
from common.http import request
import math
import random
import time


class CoinGecko:
    def __init__(self):
        self.req = request.MyRequest()
        self.headers = {}
        self.compute_financials()

    def build_model(self, assetsUSD, assetsBTC):
        self.assets = []

        for idx, asset in enumerate(assetsUSD):
            self.assets.append(
                {
                    'name':                 asset['name'],
                    'symbol':               asset['symbol'],
                    'financials': {
                        'USD': {
                            'price':                                asset['current_price'],
                            'market_cap':                           asset['market_cap'],
                            'market_cap_rank':                      asset['market_cap_rank'],
                            'high_24h':                             asset['high_24h'],
                            'low_24h':                              asset['low_24h'],
                            'price_change_24h':                     asset['price_change_24h'],
                            'total_volume':                         asset['total_volume'],
                            'ath':                                  asset['ath'],
                            'ath_change_percentage':                asset['ath_change_percentage'],
                            'ath_date':                             asset['ath_date'],
                            'market_cap_change_24h':                asset['market_cap_change_24h'],
                            'circulating_supply':                   asset['circulating_supply'],
                            'total_supply':                         asset['total_supply'],
                            'market_cap_change_percentage_24h':     asset['market_cap_change_percentage_24h'],
                            'percent_change_24h':                   asset['price_change_percentage_24h'],       
                            'roi':                                  asset['roi'],       
                            
                            # 'percent_change_1h':                    asset['percent_change_1h'],
                            # 'market_change_24h':                    asset['market_change_24h'],
                            # 'volume_24h':                           asset['volume_24h'],
                            # 'percent_change_7d':                    asset['quote']['USD']['percent_change_7d'],   
                        },
                        'BTC': {
                            'price':                                assetsBTC[idx]['current_price'],
                            'market_cap':                           assetsBTC[idx]['market_cap'],
                            'market_cap_rank':                      assetsBTC[idx]['market_cap_rank'],
                            'high_24h':                             assetsBTC[idx]['high_24h'],
                            'low_24h':                              assetsBTC[idx]['low_24h'],
                            'price_change_24h':                     assetsBTC[idx]['price_change_24h'],
                            'total_volume':                         assetsBTC[idx]['total_volume'],
                            'ath':                                  assetsBTC[idx]['ath'],
                            'ath_change_percentage':                assetsBTC[idx]['ath_change_percentage'],
                            'ath_date':                             assetsBTC[idx]['ath_date'],
                            'market_cap_change_24h':                assetsBTC[idx]['market_cap_change_24h'],
                            'circulating_supply':                   assetsBTC[idx]['circulating_supply'],
                            'total_supply':                         assetsBTC[idx]['total_supply'],
                            'market_cap_change_percentage_24h':     assetsBTC[idx]['market_cap_change_percentage_24h'],
                            'percent_change_24h':                   assetsBTC[idx]['price_change_percentage_24h'],       
                            'roi':                                  assetsBTC[idx]['roi'],        
                        },
                        'created_date': dt.datetime.now()
                    },
                }
            )

    def get_coin_financials(self):
        pass

    def compute_financials(self):

        coins_list = self.req.get_data(cfg.settings['COINGECKO']['COINS_LIST_URL'], self.headers)
        coin_count = math.ceil(len(coins_list) / cfg.settings['COINGECKO']['params']['standard']['per_page']) 
        
        assetsUSD = []
        assetsBTC = []
        for i in range(coin_count):
            time.sleep(random.randint(0,3))
            assetsUSD.extend(self.req.get_data(
                cfg.settings['COINGECKO']['COINS_MARKETS_URL'], 
                self.headers, 
                {
                    **cfg.settings['COINGECKO']['params']['USD'],
                    **cfg.settings['COINGECKO']['params']['standard'] 
                },
                { 'page': i+1 }
            ))
            assetsBTC.extend(self.req.get_data(
                cfg.settings['COINGECKO']['COINS_MARKETS_URL'], 
                self.headers, 
                {
                    **cfg.settings['COINGECKO']['params']['BTC'],
                    **cfg.settings['COINGECKO']['params']['standard'] 
                },
                { 'page': i+1 }
            ))

        self.build_model(assetsUSD, assetsBTC)

    def trim_financials(self, token):
        pass
        # financials = dict(self.assets[
        #         self.assets.index(list(filter(lambda n: n.get('symbol').lower() == token.lower(), self.assets))[0])])
        # try:
        #     del financials["name"]
        #     del financials["symbol"]
        # except KeyError:
        #     print("Key 'name'/'symbol' not found")
        
        # return financials['financials']

    def get_asset(self, token):
        pass
        # if list(filter(lambda n: n.get('symbol').lower() == token.lower(), self.assets)):
        #     return self.trim_financials(token)

    def get_financials(self, token):
        pass
        # asset_financials = self.get_asset(token)
        # return asset_financials if asset_financials else None
