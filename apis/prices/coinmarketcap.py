import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import urllib
from urllib.request import urlopen, Request
import datetime as dt

class CoinMarketCap:
    def __init__(self):
        self.assets = self.get_assets()

    def get_assets(self):
        assets = []

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        parameters = {
            'limit': '5000',
            'convert': 'USD'
        }
        parameters2 = {
            'limit': '5000',
            'convert': 'BTC'
        }

        defaultHeaders = requests.utils.default_headers()
        defaultHeaders['User-Agent'] = \
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'

        # tappiera00
        # headers = {
        #     'Accepts': 'application/json',
        #     'X-CMC_PRO_API_KEY': 'b77602e7-a160-4384-aedd-2d4f4f4a308e',
        # }

        # joedimech75
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'c3876b59-a8d3-4a8f-bf51-e2aad4ca9a5c',
        }

        session = Session()
        session.headers.update({**headers, **defaultHeaders})

        try:
            response = session.get(url, params=parameters)
            assetsUSD = json.loads(response.text)['data']

            response = session.get(url, params=parameters2)
            assetsBTC = json.loads(response.text)['data']

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        for idx, asset in enumerate(assetsUSD):
            assets.append(
                {
                    'id':                   asset['id'],
                    'name':                 asset['name'],
                    'symbol':               asset['symbol'],
                    'num_market_pairs':     asset['num_market_pairs'],
                    'max_supply':           asset['max_supply'],
                    'circulating_supply':   asset['circulating_supply'],
                    'total_supply':         asset['total_supply'],
                    'platform':             asset['platform'],
                    'cmc_rank':             asset['cmc_rank'],
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
                        }
                    },
                }
            )

        return assets

    def get_asset(self, token_to_update):
        # assets = []

        if list(filter(lambda n: n.get('symbol').lower() == token_to_update.lower(), self.assets)):
            return self.assets[
                self.assets.index(list(filter(lambda n: n.get('symbol').lower() == token_to_update.lower(), self.assets))[0])]

        # assets.append(coin_info)

        # return coin_info

    def get_financials(self, token_to_update):
        asset = self.get_asset(token_to_update)

        price_usd = 0
        price_btc = 0

        volume_usd_24h = 0
        volume_btc_24h = 0

        change_usd_1h = 0
        change_btc_1h = 0

        change_usd_24h = 0
        change_btc_24h = 0

        change_usd_7d = 0
        change_btc_7d = 0

        marketcap_usd = 0
        marketcap_btc = 0

        if asset:
            if 'price' in asset['financials']['USD']:
                price_usd = asset['financials']['USD']['price']
                # price_usd = asset['financials']['USD']['price'] if 'price' in asset['financials']['USD'] else 0

            if 'price' in asset['financials']['BTC']:
                price_btc = asset['financials']['BTC']['price']

            if 'volume_24h' in asset['financials']['USD']:
                if asset['financials']['USD']['volume_24h'] is not None:
                    volume_usd_24h = asset['financials']['USD']['volume_24h']

            if 'volume_24h' in asset['financials']['BTC']:
                if asset['financials']['BTC']['volume_24h'] is not None:
                    volume_btc_24h = asset['financials']['BTC']['volume_24h']

            if 'percent_change_1h' in asset['financials']['USD']:
                if asset['financials']['USD']['percent_change_1h'] is not None:
                    change_usd_1h = asset['financials']['USD']['percent_change_1h']

            if 'percent_change_1h' in asset['financials']['BTC']:
                if asset['financials']['BTC']['percent_change_24h'] is not None:
                    change_btc_1h = asset['financials']['BTC']['percent_change_1h']

            if 'percent_change_24h' in asset['financials']['USD']:
                if asset['financials']['USD']['percent_change_24h'] is not None:
                    change_usd_24h = asset['financials']['USD']['percent_change_24h']

            if 'percent_change_24h' in asset['financials']['BTC']:
                if asset['financials']['BTC']['percent_change_24h'] is not None:
                    change_btc_24h = asset['financials']['BTC']['percent_change_24h']

            if 'percent_change_7d' in asset['financials']['USD']:
                if asset['financials']['USD']['percent_change_7d'] is not None:
                    change_usd_7d = asset['financials']['USD']['percent_change_7d']

            if 'percent_change_7d' in asset['financials']['BTC']:
                if asset['financials']['BTC']['percent_change_7d'] is not None:
                    change_btc_7d = asset['financials']['BTC']['percent_change_7d']

            if 'market_cap' in asset['financials']['USD']:
                if asset['financials']['USD']['market_cap'] is not None:
                    marketcap_usd = asset['financials']['USD']['market_cap']

            if 'market_cap' in asset['financials']['BTC']:
                if asset['financials']['BTC']['market_cap'] is not None:
                    marketcap_btc = asset['financials']['BTC']['market_cap']

        financials = {
            'USD': {
                'price': price_usd,
                'volume_24h': volume_usd_24h,
                'change_1h': change_usd_1h,
                'change_24h': change_usd_24h,
                'change_7d': change_usd_7d,
                'marketcap': marketcap_usd,
            },
            'BTC': {
                'price': price_btc,
                'volume_24h': volume_btc_24h,
                'change_1h': change_btc_1h,
                'change_24h': change_btc_24h,
                'change_7d': change_btc_7d,
                'marketcap': marketcap_btc,
            },
            'created_date': dt.datetime.now()
        }

        return financials
