class CDModel(object):
    caption = ''
    proof = ''
    public_date = ''
    start_date = ''
    end_date = ''
    coin_name = ''
    coin_symbol = ''


    def __init__(self, caption, proof,
                 public_date, start_date, end_date,
                 coin_name, coin_symbol):
        self.caption = caption
        self.proof = proof
        self.public_date = public_date
        self.start_date = start_date
        self.end_date = end_date
        self.coin_name = coin_name
        self.coin_symbol = coin_symbol

