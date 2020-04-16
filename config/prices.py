#!/usr/bin/env python

settings = {
    'COINGECKO': {
        'URLs': {
            'COINLIST': {
                'LINK': 'https://api.coingecko.com/api/v3/coins/list',
            },
            'MARKETS': {
                'LINK': 'https://api.coingecko.com/api/v3/coins/markets',
                'ARGS': {
                    'STANDARD': {
                        'per_page': 250,
                        'sparkline': True,
                        'page': '{}'
                    },
                    'USD': {
                        'vs_currency': 'USD',
                    },
                    'BTC': {
                        'vs_currency': 'BTC',
                    }
                }
            },
            'FINANCIALS': {
                'LINK': 'https://api.coingecko.com/api/v3/coins/{0}',
                'ARGS': {
                    'STANDARD': {
                        'tickers': 'true',
                        'localization': 'false',
                        'sparkline': 'true',
                        'developer_data': 'true',
                        'community_data': 'true',
                        'market_data': 'true'
                    },
                }
            }             
        }
    },
    'COINMARKETCAP': {
        'URLs': {
            'LISTINGS': {
                'LINK':        'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
                'ARGS': {
                    'USD': {
                        'limit': '5000',
                        'convert': 'USD'
                    },
                    'BTC': {
                        'limit': '5000',
                        'convert': 'BTC'
                    }
                }
            }
        },
        'AUTH': {
            'X-CMC_PRO_API_KEY1':            'c3876b59-a8d3-4a8f-bf51-e2aad4ca9a5c', #joedimech75
            'X-CMC_PRO_API_KEY2':            'b77602e7-a160-4384-aedd-2d4f4f4a308e', #tappiera
        }
    }
}