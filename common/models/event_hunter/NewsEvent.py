class NewsEvent(object):
    start_date = ''
    public_date = ''
    end_date = ''

    ticker = ''
    token = ''
    event = ''
    proof = ''
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

    def __init__(self, start_date, public_date, end_date,
                 ticker, token, event, proof='', category='',
                 price_usd=0, price_btc=0, change_24h=0, change_7d=0):

        self.start_date = start_date
        self.public_date = public_date
        self.end_date = end_date

        self.ticker = ticker
        self.token = token
        self.event = event
        self.proof = proof
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
