import requests


class CoinMarketCap:
    def __init__(self):
        self.get_assets()

    def get_assets(self):
        r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=2000')
        self.assets = r.json()

    def get_asset(self, token, ticker):
        asset = [asset for asset in self.assets if asset['id'] == token.lower().replace(' ', '-')]

        if not asset:
            asset = [asset for asset in self.assets if asset['id'] == token.lower().replace(' ', '-')
                .replace('\n', '')]
        if not asset:
            asset = [asset for asset in self.assets if asset['id'] == token.lower().replace(' ', '-')
                .replace('\n', '') + 'coin']
        if not asset:
            asset = [asset for asset in self.assets if asset['id'] == (token + '-' + ticker)
                .lower().replace(' ', '-').replace('\n', '')]
        if not asset:
            asset = [asset for asset in self.assets if (asset['symbol']).lower() == ticker.lower()]

        return asset

    def get_asset_prices(self, token, ticker):
        asset = self.get_asset(token, ticker)

        price_usd = 0
        price_btc = 0
        change_24h = 0
        change_7d = 0

        if asset:
            if 'price_usd' in asset[0]:
                price_usd = asset[0]['price_usd']
            if 'price_btc' in asset[0]:
                price_btc = asset[0]['price_btc']
            if 'percent_change_24h' in asset[0]:
                if asset[0]['percent_change_24h'] is not None:
                    change_24h = asset[0]['percent_change_24h']
                else:
                    change_24h = 'NULL'
            if 'percent_change_7d' in asset[0]:
                if asset[0]['percent_change_7d'] is not None:
                    change_7d = asset[0]['percent_change_7d']
                else:
                    change_7d = 'NULL'

        return price_usd, price_btc, change_24h, change_7d
