class NewsEvent(object):
    event_title = None
    category = None
    event_date = None
    source = None
    proof = None
    can_occur_before = None
    token_details = {}
    financials = {}
    created_date = None

    end_date = None
    price_changes = None
    important = None
    # source_reliable = None

    # event_description
    # start_date = ''
    # public_date = ''
    # end_date = ''
    # vote_count = 0
    # pos_vote_count = 0
    # percent = 0
    # event_description = ''

    def __init__(self, raw_event):
        self.category      = raw_event['category']
        self.event_date    = raw_event['event_date']
        self.source        = raw_event['source']
        self.created_date  = raw_event['created_date']
        self.event_title   = raw_event['event_title']

        if 'proof' in raw_event:
            self.proof     = raw_event['proof']


        if raw_event['origin'] == 'coindar':
            self.process_coindar(raw_event)

        if raw_event['origin'] == 'coinmarketcal':
            self.process_coinmarketcal(raw_event)
            

    def process_coindar(self, raw_event):
        self.important      = raw_event['important']
        self.price_changes  = raw_event['coin_price_changes']
        self.end_date       = raw_event['end_date']
        self.token_details  = raw_event['token_details']
        self.financials     = raw_event['financials']
        
    def process_coinmarketcal(self, raw_event):
        self.can_occur_before    = raw_event['can_occur_before']
            
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

