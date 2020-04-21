from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from simplejson.errors import JSONDecodeError
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
        res = None
        try:
            if dynamic is not None:
                for k, v in params.items():
                    if v == '{}':
                        params[k] = dynamic[k]

            headers = {} if headers is None else headers

            res = requests.get(url, headers={**self.headers, **headers}, params=params).json()

            if 'body' in res:
                return res['body']
            elif 'data' in res:
                return res['data']
            else:
                return res
        
            # req['data'] = [{'originator': 'Coinmarketcap'}] + req['data'] 
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}') 
        except URLError as url_err:
            print(f'URL error occurred: {url_err}')
        except JSONDecodeError as e:
            print('JSON Parse failed: {0}'.format(e))
        except (TypeError, AttributeError) as e:
            print('Type Error : {0}'.format(e))
            
