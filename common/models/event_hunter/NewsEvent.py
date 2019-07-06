class NewsEvent(object):
    event_title = ''
    event_description = ''
    category = ''

    ticker = ''
    token = ''

    start_date = ''
    public_date = ''
    end_date = ''

    vote_count = 0
    pos_vote_count = 0
    percent = 0
    proof = ''
    source = ''

    price_usd = 0
    price_usd2 = 0
    price_usd3 = 0
    price_usd4 = 0

    price_btc = 0
    price_btc2 = 0
    price_btc3 = 0
    price_btc4 = 0

    change_24h = 0
    change_24h2 = 0
    change_24h3 = 0
    change_24h4 = 0

    change_7d = 0
    change_7d2 = 0
    change_7d3 = 0
    change_7d4 = 0

    def __init__(self, event_title='', category='', event_date='',
                 coins='', proof='', source='',
                 price_usd=0, price_btc=0, change_24h=0, change_7d=0):

        self.event_title = event_title
        self.category = category

        self.coins = coins

        self.event_date = event_date

        self.proof = proof
        self.source = source

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
