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

    # Price in both currencies (USD, BTC)
    price_usd = 0
    price_usd2 = 0
    price_usd3 = 0
    price_usd4 = 0

    price_btc = 0
    price_btc2 = 0
    price_btc3 = 0
    price_btc4 = 0

    # Volume change over last 24 hours (USD, BTC)
    volume_usd_24h = 0
    volume_usd_24h2 = 0
    volume_usd_24h3 = 0
    volume_usd_24h4 = 0

    volume_btc_24h = 0
    volume_btc_24h2 = 0
    volume_btc_24h3 = 0
    volume_btc_24h4 = 0

    # Percent change over last hour (USD, BTC)
    change_usd_1h = 0
    change_usd_1h_2 = 0
    change_usd_1h_3 = 0
    change_usd_1h_4 = 0

    change_btc_1h = 0
    change_btc_1h_2 = 0
    change_btc_1h_3 = 0
    change_btc_1h_4 = 0

    # Percent change over last hour (USD, BTC)
    change_usd_24h = 0
    change_usd_24h_2 = 0
    change_usd_24h_3 = 0
    change_usd_24h_4 = 0

    change_btc_24h = 0
    change_btc_24h_2 = 0
    change_btc_24h_3 = 0
    change_btc_24h_4 = 0

    # Percent change over 7 days
    change_usd_7d = 0
    change_usd_7d2 = 0
    change_usd_7d3 = 0
    change_usd_7d4 = 0

    change_btc_7d = 0
    change_btc_7d2 = 0
    change_btc_7d3 = 0
    change_btc_7d4 = 0

    # Market cap change
    market_cap_usd_h = 0
    market_cap_usd_h2 = 0
    market_cap_usd_h3 = 0
    market_cap_usd_h4 = 0

    market_cap_btc_h = 0
    market_cap_btc_h2 = 0
    market_cap_btc_h3 = 0
    market_cap_btc_h4 = 0

    def __init__(self, event_title='', category='', event_date='',
                 coins='', proof='', source='',
                 price_usd=0, price_btc=0,
                 volume_usd_24h=0, volume_btc_24h=0,
                 change_usd_1h=0, change_btc_1h=0,
                 change_usd_24h=0, change_btc_24h=0,
                 change_usd_7d=0, change_btc_7d=0,
                 market_cap_usd=0, market_cap_btc=0):

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

        self.volume_usd_24h = volume_usd_24h
        self.volume_usd_24h2 = 0
        self.volume_usd_24h3 = 0
        self.volume_usd_24h4 = 0

        self.volume_btc_24h = volume_btc_24h
        self.volume_btc_24h2 = 0
        self.volume_btc_24h3 = 0
        self.volume_btc_24h4 = 0

        self.change_usd_1h = change_usd_1h
        self.change_usd_1h_2 = 0
        self.change_usd_1h_3 = 0
        self.change_usd_1h_4 = 0

        self.change_btc_1h = change_btc_1h
        self.change_btc_1h_2 = 0
        self.change_btc_1h_3 = 0
        self.change_btc_1h_4 = 0

        self.change_usd_24h = change_usd_24h
        self.change_usd_24h_2 = 0
        self.change_usd_24h_3 = 0
        self.change_usd_24h_4 = 0

        self.change_btc_24h = change_btc_24h
        self.change_btc_24h_2 = 0
        self.change_btc_24h_3 = 0
        self.change_btc_24h_4 = 0

        self.change_usd_7d = change_usd_7d
        self.change_usd_7d_2 = 0
        self.change_usd_7d_3 = 0
        self.change_usd_7d_4 = 0

        self.change_btc_7d = change_btc_7d
        self.change_btc_7d_2 = 0
        self.change_btc_7d_3 = 0
        self.change_btc_7d_4 = 0

        self.market_cap_usd = market_cap_usd
        self.market_cap_usd_2h = 0
        self.market_cap_usd_3h = 0
        self.market_cap_usd_4h = 0

        self.market_cap_btc = market_cap_btc
        self.market_cap_btc_2h = 0
        self.market_cap_btc_3h = 0
        self.market_cap_btc_4h = 0