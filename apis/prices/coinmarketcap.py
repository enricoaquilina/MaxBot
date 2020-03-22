import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import urllib
from urllib.request import urlopen, Request
import datetime as dt
import common.config as cfg
from common.http import request

class CoinMarketCap:
    def __init__(self):
        self.req = request.MyRequest()
        self.headers = { 'X-CMC_PRO_API_KEY': cfg.settings['X-CMC_PRO_API_KEY']}
        self.assets = self.get_assets()

    def get_assets(self):
        assets = []

        assetsUSD = self.req.get_data(cfg.settings['COINMARKETCAP_LISTINGS'], self.headers, cfg.settings['params']['USD'])
        assetsBTC = self.req.get_data(cfg.settings['COINMARKETCAP_LISTINGS'], self.headers, cfg.settings['params']['BTC'])

        for idx, asset in enumerate(assetsUSD):

            assets.append(
                {
                    'name':                 asset['name'],
                    'symbol':               asset['symbol'],
                    'financials': {
                        'USD': {
                            'price':                asset['quote']['USD']['price'],
                            'volume_24h':           asset['quote']['USD']['volume_24h'],
                            'percent_change_1h':    asset['quote']['USD']['percent_change_1h'],
                            'percent_change_24h':   asset['quote']['USD']['percent_change_24h'],
                            'percent_change_7d':    asset['quote']['USD']['percent_change_7d'],
                            'market_cap':           asset['quote']['USD']['market_cap'],
                        },
                        'BTC': {
                            'price':                assetsBTC[idx]['quote']['BTC']['price'],
                            'volume_24h':           assetsBTC[idx]['quote']['BTC']['volume_24h'],
                            'percent_change_1h':    assetsBTC[idx]['quote']['BTC']['percent_change_1h'],
                            'percent_change_24h':   assetsBTC[idx]['quote']['BTC']['percent_change_24h'],
                            'percent_change_7d':    assetsBTC[idx]['quote']['BTC']['percent_change_7d'],
                            'market_cap':           assetsBTC[idx]['quote']['BTC']['market_cap'],
                        },
                        'created_date': dt.datetime.now()
                    },
                }
            )

        return assets

    def get_asset(self, token_to_update):
        if list(filter(lambda n: n.get('symbol').lower() == token_to_update.lower(), self.assets)):
            return self.assets[
                self.assets.index(list(filter(lambda n: n.get('symbol').lower() == token_to_update.lower(), self.assets))[0])]

    def get_financials(self, token_to_update):
        asset = self.get_asset(token_to_update)

        if asset:
            return asset['financials']
