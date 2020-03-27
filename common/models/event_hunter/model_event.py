import datetime as dt

class NewsEvent:
    # source_reliable = None

    # vote_count = 0
    # pos_vote_count = 0
    # percent = 0
    # event_description = ''

    def __init__(self, raw_event):
        self.category      = raw_event['category']
        self.event_date    = raw_event['event_date']
        self.source        = raw_event['source']
        self.event_title   = raw_event['event_title']
        self.created_date  = dt.datetime.now()

        if 'proof' in raw_event and raw_event['proof'] != '':
             self.proof = raw_event['proof']

        self.determine_source(raw_event)
            
    def determine_source(self, raw_event):
        if raw_event['origin'] == 'coindar':
            self.process_coindar(raw_event)

        if raw_event['origin'] == 'coinmarketcal':
            self.process_coinmarketcal(raw_event)
    
    def process_coindar(self, raw_event):
        self.important      = raw_event['important']
        self.price_changes  = raw_event['coin_price_changes']
        self.token_details  = raw_event['token_details']
        self.financials     = raw_event['financials']
        self.socials     = raw_event['socials']
        
        if 'end_date' in raw_event:
            self.end_date = raw_event['end_date']
        
    def process_coinmarketcal(self, raw_event):
        self.can_occur_before  = raw_event['can_occur_before']
            
        self.financials = {}
        self.token_details = {}
        for coin in raw_event['coins']:
            self.financials[coin['symbol']] = {}
            self.token_details[coin['symbol']] = {
                'id': coin['id'],
                'name': coin['name'],
                'symbol': coin['symbol'],
                'full_name': coin['fullname'],
            }
        

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

