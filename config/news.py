#!/usr/bin/env python

from datetime import date

settings = {
    'COINMARKETCAL': {
        'URLs': {
            'EVENTS': {
                'LINK': 'https://developers.coinmarketcal.com/v1/events',
            },
            'COINS': {
                'LINK': 'https://developers.coinmarketcal.com/v1/coins',
            },
            'CATEGORIES': {
                'LINK': 'https://developers.coinmarketcal.com/v1/categories',
            }
        },
        'AUTH': {
            'x-api-key': 'iFQY61z1SD4PanhjChc8E4RMo4KdUHdT5AXCx8Y8',
        },
    },
    'COINDAR': {
        'URLs': {
            'EVENTS': {
                'LINK': 'https://coindar.org/api/v2/events',
                'ARGS': {
                    'filter_date_start':    date.today(),
                    'page_size':            '15'
                },
            },
            'TAGS': {
                'LINK': 'https://coindar.org/api/v2/tags',
            },
            'COINS': {
                'LINK': 'https://coindar.org/api/v2/coins',
            },            
            'SOCIALS': {
                'LINK': 'https://coindar.org/api/v2/social',
            }   
        },
        'AUTH': {
            'access_token': '37949:XvvzaWNeECQuCXyJLZa'
        },
    }
}