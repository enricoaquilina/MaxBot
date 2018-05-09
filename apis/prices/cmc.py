import requests

def get_asset(token, ticker):
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=2000')
    assets = r.json()

    asset = [asset for asset in assets if asset['id'] == token.lower().replace(' ', '-')]
    if not asset:
        asset = [asset for asset in assets if asset['id'] == token.lower().replace(' ', '-')
            .replace('\n', '')]
    if not asset:
        asset = [asset for asset in assets if asset['id'] == token.lower().replace(' ', '-')
            .replace('\n', '') + 'coin']
    if not asset:
        asset = [asset for asset in assets if asset['id'] == (token + '-' + ticker)
            .lower().replace(' ', '-').replace('\n', '')]
    if not asset:
        asset = [asset for asset in assets if (asset['symbol']).lower() == ticker.lower()]

    return asset