from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json

class MyRequest:
    def __init__(self):
        self.headers = {
            'x-api-key':        'iFQY61z1SD4PanhjChc8E4RMo4KdUHdT5AXCx8Y8',
            'Accept-Encoding':  'deflate, gzip',
            'Accept':           'application/json',
            'User-Agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }

    def get_data(self, url):
        try:
            req = Request(url, headers=self.headers)
            return json.loads(urlopen(req).read().decode('UTF-8'))['body']
        except (URLError, HTTPError) as e:
            print(e.reason)
