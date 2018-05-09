from common.http import request


class CoinMarketCal:
    def __init__(self):
        self.client_id = '603_4xuth8ds5u8ss484gcg04wc884c4k8kowc4kko8cccoow44kwo'
        self.client_secret = 'd672epocs1s08kks8swsskg8kgw444coogwssw4ko0okws08w'

        self.req = request.MyRequest()
        self.access_token = self.api_news2_get_access_token()['access_token']

    def api_news2_get_access_token(self):
        url = 'https://api.coinmarketcal.com/oauth/v2/token?grant_type=client_credentials' \
              '&client_id='+self.client_id + \
              '&client_secret=' + self.client_secret

        return self.req.get_data(url)

    def api_news2_get_list_of_coins(self):
        url = 'https://api.coinmarketcal.com/v1/coins?access_token='+self.access_token
        return self.req.get_data(url)

    def api_news2_get_categories(self):
        url = 'https://api.coinmarketcal.com/v1/categories?access_token='+self.access_token
        return self.req.get_data(url)

    def api_news2_get_events(self, date_range_start=None,
                             date_range_end=None, coins=None,
                             categories=None, sort_by=None,
                             show_only=None, show_metadata=None,
                             page=1, max=16):
        # page (page_number
        # max (max value is 150
        # dates (dd/MM/YYYY
        # coins (string of multiple coins' IDs[ bytom,casinocoin
        # categories (string of multiple categories IDs[ 1,2
        # sort_by (created_desc, hot_events
        # show_only (hot_events, --
        # show_metadata (true, --
        url = 'https://api.coinmarketcal.com/v1/events?' \
              'access_token='+self.access_token +\
              '&page='+str(page) +\
              '&max='+str(max) +\
              '&dateRangeEnd=09%2F05%2F2018' \
              '&coins=bytom%2Ccasinocoin' \
              '&categories=9%2C8%2C7' \
              '&sortBy=created_desc' \
              '&showMetadata=true'
        return self.req.get_data(url)
