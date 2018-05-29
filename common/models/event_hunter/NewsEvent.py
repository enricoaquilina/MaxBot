class NewsEvent(object):
    date = ''
    date_inserted = ''
    ticker = ''
    event = ''
    category = ''
    price_usd = ''
    price_usd2 = ''
    price_usd3 = ''
    price_usd4 = ''
    price_btc = ''
    price_btc2 = ''
    price_btc3 = ''
    price_btc4 = ''
    change_24h = ''
    change_24h2 = ''
    change_24h3 = ''
    change_24h4 = ''
    change_7d = ''
    change_7d2 = ''
    change_7d3 = ''
    change_7d4 = ''

    def __init__(self, date, date_inserted,
                 ticker, token, event,
                 price_usd=0, price_btc=0,
                 change_24h=0, change_7d=0,
                 category='', proof=''):
        self.date_inserted = date_inserted
        self.date = date
        self.ticker = ticker
        self.token = token
        self.event = event
        self.category = category
        self.price_usd = price_usd
        self.price_usd2 = 0
        self.price_usd3 = 0
        self.price_usd4 = 0
        self.price_btc = price_btc
        self.price_btc2 = 0
        self.price_btc3 = 0
        self.price_btc4 = 0
        self.change_24h = change_24h
        self.change_24h2 = 0
        self.change_24h3 = 0
        self.change_24h4 = 0
        self.change_7d = change_7d
        self.change_7d2 = 0
        self.change_7d3 = 0
        self.change_7d4 = 0
