from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import requests
import json

class MyRequest:
    def __init__(self):
        self.headers = {
            'Accept-Encoding':  'deflate, gzip',
            'Accept':           'application/json',
            'User-Agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }

     # defaultHeaders = requests.utils.default_headers()


    def get_data(self, url, headers=None, params=None, dynamic=None):
        try:
            if dynamic is not None:
                for k, v in params.items():
                    if v == '{}':
                        params[k] = dynamic[k]

            headers = {} if headers is None else headers

            req = requests.get(url, headers={**self.headers, **headers}, params=params).json()

            # req['data'] = [{'originator': 'Coinmarketcap'}] + req['data']
            
            if 'body' in req:
                return req['body']
            elif 'data' in req:
                return req['data']
            else:
                return req
                
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}') 
        except URLError as url_err:
            print(f'URL error occurred: {url_err}')
