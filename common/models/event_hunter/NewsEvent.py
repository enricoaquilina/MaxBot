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
        for coin in raw_event['coins']:
            self.financials[coin['symbol']] = {}
            self.token_details[coin['symbol']] = {
                'id': coin['id'],
                'name': coin['name'],
                'symbol': coin['symbol'],
                'full_name': coin['fullname'],
            }

        self.event_title         = next(iter(raw_event['title'].values()))
        self.category            = raw_event['categories'][0]['name']
        self.event_date          = raw_event['date_event']
        self.source              = raw_event['source']
        self.can_occur_before    = raw_event['can_occur_before']
        self.proof               = raw_event['proof']
        self.created_date        = raw_event['created_date']