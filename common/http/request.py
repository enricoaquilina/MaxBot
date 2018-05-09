import urllib.request as urlreq
import json


class MyRequest:
    def __init__(self):
        pass

    def get_data(self, url):
        req = urlreq.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/60.0.3112.113 Safari/537.36')
        response = urlreq.urlopen(req).read()
        json_data = json.loads(response.decode('utf-8'))
        return json_data
