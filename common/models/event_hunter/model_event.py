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

    # event_description
    # start_date = ''
    # public_date = ''
    # end_date = ''
    # vote_count = 0
    # pos_vote_count = 0
    # percent = 0
    # event_description = ''

    def __init__(self, raw_event):
        self.event_title         = next(iter(raw_event['title'].values()))
        self.category            = raw_event['category']
        self.event_date          = raw_event['event_date']
        self.source              = raw_event['source']
        self.can_occur_before    = raw_event['can_occur_before']
        self.proof               = raw_event['proof']
        self.created_date        = raw_event['created_date']
        
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

