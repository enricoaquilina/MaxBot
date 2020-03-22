#!/usr/bin/env python
settings = {
    'hostname':                     '127.0.0.1',
    'port':                         '27017',
    'db_name':                      'maxbot',
    'coll_news_events':             'news_events',
    'coll_news_articles':           'news_articles',

    'COINMARKETCAL_DAILY_EVENTS':   'https://developers.coinmarketcal.com/v1/events',
    'COINMARKETCAL_COIN_LIST':      'https://developers.coinmarketcal.com/v1/coins',
    'COINMARKETCAL_CATEGORY_LIST':  'https://developers.coinmarketcal.com/v1/categories',
    'x-api-key':                    'iFQY61z1SD4PanhjChc8E4RMo4KdUHdT5AXCx8Y8',

    'X-CMC_PRO_API_KEY1':            'c3876b59-a8d3-4a8f-bf51-e2aad4ca9a5c', #joedimech75
    'X-CMC_PRO_API_KEY2':            'b77602e7-a160-4384-aedd-2d4f4f4a308e', #tappiera
    'COINMARKETCAP_LISTINGS':       'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
    'params': {
                'USD': {
                    'limit': '5000',
                    'convert': 'USD'
                },
                'BTC': {
                    'limit': '5000',
                    'convert': 'BTC'
                }
    },

    'COINDAR_1':                    'https://coindar.org/api/v2/coins?access_token=',
    'COINDAR_2':                    'https://coindar.org/api/v2/events?limit=',
    'COINDAR_3':                    'https://coindar.org/api/v1/coinEvents?name=',
    'COINDAR_4':                    'https://coindar.org/api/v1/events?year='
}