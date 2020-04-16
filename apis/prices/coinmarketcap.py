from common.http import request
from common.utilities.helper import Helper

import config.prices as cfg

import json
import datetime as dt

class CoinMarketCap:
    def __init__(self):
        self.req = request.MyRequest()
        self.helper = Helper()
        self.headers = { 'X-CMC_PRO_API_KEY': cfg.settings['COINMARKETCAP']['AUTH']['X-CMC_PRO_API_KEY1']}
        self.headers2 = { 'X-CMC_PRO_API_KEY': cfg.settings['COINMARKETCAP']['AUTH']['X-CMC_PRO_API_KEY2']}
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

    def compute_financials(self):
        assetsUSD = self.req.get_data(cfg.settings['COINMARKETCAP']['URLs']['LISTINGS']['LINK'], 
                    self.headers, cfg.settings['COINMARKETCAP']['URLs']['LISTINGS']['ARGS']['USD'])
                    
        assetsBTC = self.req.get_data(cfg.settings['COINMARKETCAP']['URLs']['LISTINGS']['LINK'], 
                    self.headers2, cfg.settings['COINMARKETCAP']['URLs']['LISTINGS']['ARGS']['BTC'])

        self.build_model(assetsUSD, assetsBTC)

    def does_coin_exist(self, token_name, token_symbol):
        self.coin = list(filter(lambda n: n.get('name').lower() == token_name.lower() and n.get('symbol').lower() == token_symbol.lower(), self.assets))

        if len(self.coin) == 0:
            self.coin = list(filter(lambda n: n.get('name').lower() == token_name.lower(), self.assets))
            if len(self.coin) > 0:
                self.helper.options['WARNING'](token_name, token_symbol, 2, 'coinmarketcap')
            
        if len(self.coin) == 0:
            self.coin = list(filter(lambda n: n.get('symbol').lower() == token_symbol.lower(), self.assets))
            if len(self.coin) > 0:
                self.helper.options['WARNING'](token_name, token_symbol, 3, 'coinmarketcap')
            else:
                return False
        asset = dict(self.assets[
                self.assets.index(list(filter(lambda n: n.get('symbol').lower() == token_symbol.lower(), self.assets))[0])])
        
        if len(self.coin) > 0:
            self.coin = dict(self.assets[self.assets.index(self.coin[0])])
        elif not any(self.coin):
            print('Did not find token {}, {} from Coingecko!!!'.format(token_name, token_symbol))

        if not any(asset):
            print('Did not find token {}, {} from Coinmarketcap!!!'.format(token_name, token_symbol))

        return any(asset)

    def trim_financials(self, token):
        financials = dict(self.assets[
                self.assets.index(list(filter(lambda n: n.get('symbol').lower() == token.lower(), self.assets))[0])])
        try:
            del financials["name"]
            del financials["symbol"]
        except KeyError:
            print("Key 'name'/'symbol' not found")
        
        return financials['financials']

    def get_asset(self, token):
        if list(filter(lambda n: n.get('symbol').lower() == token.lower(), self.assets)):
            return self.trim_financials(token)

    def get_financials(self, token):
        asset_financials = self.get_asset(token)
        return asset_financials if asset_financials else None
