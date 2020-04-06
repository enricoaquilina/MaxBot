#!/usr/bin/env python
from datetime import date

settings = {
    # mongo
    'hostname':                     '127.0.0.1',
    'port':                         '27017',
    'db_name':                      'maxbot',
    'coll_news_events':             'news_events',
    'coll_news_articles':           'news_articles',

    # coinmarketcal
    'COINMARKETCAL_DAILY_EVENTS':   'https://developers.coinmarketcal.com/v1/events',
    'x-api-key':                    'iFQY61z1SD4PanhjChc8E4RMo4KdUHdT5AXCx8Y8',
    'COINMARKETCAL_COIN_LIST':      'https://developers.coinmarketcal.com/v1/coins',
    'COINMARKETCAL_CATEGORY_LIST':  'https://developers.coinmarketcal.com/v1/categories',

    # coinmarketcap
    'X-CMC_PRO_API_KEY1':            'c3876b59-a8d3-4a8f-bf51-e2aad4ca9a5c', #joedimech75
    'X-CMC_PRO_API_KEY2':            'b77602e7-a160-4384-aedd-2d4f4f4a308e', #tappiera
    'COINMARKETCAP_LISTINGS':        'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
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

    # coindar
    'COINDAR_EVENTS_URL':           'https://coindar.org/api/v2/events',
    'COINDAR_TAGS_URL':             'https://coindar.org/api/v2/tags',
    'COINDAR_COINS_URL':            'https://coindar.org/api/v2/coins',
    'COINDAR_SOCIAL_URL':           'https://coindar.org/api/v2/social',
    'COINDAR_HEADER': {
    },
    'COINDAR_TOKEN': {
        'access_token': '37949:XvvzaWNeECQuCXyJLZa'
    },
    'COINDAR_EVENTS_ARGS': {
        'filter_date_start':    date.today(),
        'page_size':            '15'
    },

    # coingecko
    'COINGECKO': {
        'COINS_LIST_URL':                   'https://api.coingecko.com/api/v3/coins/list',
        'COINS_MARKETS_URL':                'https://api.coingecko.com/api/v3/coins/markets',
        'params': {
            'standard': {
                'per_page': 250,
                'sparkline': True,
                'page': '{0}'
            },
            'USD': {
                'vs_currency': 'USD',
            },
            'BTC': {
                'vs_currency': 'BTC',
            }
        }
    }

}