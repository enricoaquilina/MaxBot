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


    def get_data(self, url, headers=None, params=None):
        try:
            req = requests.get(url, headers={**self.headers, **headers}, params=params).json()

            if 'body' in req:
                return req['body']
            if 'data' in req:
                return req['data']
                
        except (URLError, HTTPError) as e:
            print(e.reason)
