from binance.client import Client
import operator

client = Client('AHghjW58wrSi51gWwK4TAthzgL4avxm4vuyxx7tp3m8N9JxuqP84WAvblZ0cEDw4',
                '2GJpmdkmLBoK9ZuTsSMQC6TitpDhIJivZYJboLyl4KJx5XKXhxtBWsRXCuGdSWeY')

prices = client.get_all_tickers()

info = client.get_account()


def in_balance(x): return float(x['free']) > 0


balances = list(filter(in_balance, info['balances']))
balances.sort(key=lambda t: float(t['free']))

status = client.get_account_status()

balance = client.get_asset_balance(asset='ETH')

trades = client.get_my_trades(symbol='VIBEETH')

orders = client.get_open_orders(symbol='VIBEETH')

for asset in balances:
    asset_trades = client.get_my_trades(symbol=asset['asset']+'ETH')
    buys = list(filter(lambda d: d['isBuyer'] is True, asset_trades))

    sells = list(filter(lambda d: d['isBuyer'] is False, asset_trades))
    print(asset_trades.len)

for price in prices:
    print(price)

