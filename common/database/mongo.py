import datetime
import pymongo


class DB:
    def __init__(self, db_name):

        if not hasattr(self, 'db'):
            self.db = self.connect(db_name)

    def connect(self, db_name, hostname='localhost', port=27017):
        client = pymongo.MongoClient(f'mongodb://{hostname}:{port}/')
        return client[db_name]

    def insert_event(self, collection, event):
        self.db[collection].update_one(
            filter={'category': event['category'], 'event_date': event['event_date'], 'source': event['source']},
            update={
                '$set': event,
                '$currentDate':
                    {
                        'created_date': {'$type': 'date'}
                    }
            },
            upsert=True
        )

    def get_events_for_today(self, collection):
        return self.db[collection].find({'event_date': str(datetime.date.today())})

    def add_financial_event(self, collection, event_to_update, token_to_update, new_financial_info):
        return self.db[collection].update(
            {'_id': event_to_update['_id']},
            {
                '$currentDate':
                {
                    'modified_date': True
                },
                '$set':
                {
                    f'financials.{token_to_update}': new_financial_info
                }
            },
            upsert=True
        )

    def create_table(self):
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events(
            start_date      DATETIME,
            public_date      DATETIME,
            ticker    TEXT,
            token     TEXT,
            event     TEXT,
            category  TEXT,
            price_usd DECIMAL(10,5),
            price_usd2 DECIMAL(10,5),
            price_usd3 DECIMAL(10,5),
            price_usd4 DECIMAL(10,5),
            price_btc DECIMAL(10,5),
            price_btc2 DECIMAL(10,5),
            price_btc3 DECIMAL(10,5),
            price_btc4 DECIMAL(10,5),
            change_24h DECIMAL(10,5),
            change_24h2 DECIMAL(10,5),
            change_24h3 DECIMAL(10,5),
            change_24h4 DECIMAL(10,5),
            change_7d DECIMAL(10,5),
            change_7d2 DECIMAL(10,5),
            change_7d3 DECIMAL(10,5),
            change_7d4 DECIMAL(10,5),
            PRIMARY KEY(start_date, ticker))
        ''')
        self.write()

    def create_table2(self):
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_events(
            event_title   TEXT,
            event_description   TEXT,
            category   TEXT,
            ticker     TEXT,
            token     TEXT,
            event_date      DATETIME,
            public_date      DATETIME,
            end_date  DATETIME,
            vote_count DECIMAL(10,5),
            pos_vote_count DECIMAL(10,5),
            percent DECIMAL(10,5),
            proof TEXT,
            source TEXT,
            price_usd DECIMAL(10,5),
            price_usd2 DECIMAL(10,5),
            price_usd3 DECIMAL(10,5),
            price_usd4 DECIMAL(10,5),
            price_btc DECIMAL(10,5),
            price_btc2 DECIMAL(10,5),
            price_btc3 DECIMAL(10,5),
            price_btc4 DECIMAL(10,5),
            change_24h DECIMAL(10,5),
            change_24h2 DECIMAL(10,5),
            change_24h3 DECIMAL(10,5),
            change_24h4 DECIMAL(10,5),
            change_7d DECIMAL(10,5),
            change_7d2 DECIMAL(10,5),
            change_7d3 DECIMAL(10,5),
            change_7d4 DECIMAL(10,5),
            UNIQUE(event_date, ticker)
            PRIMARY KEY(event_date, ticker))
        ''')
        self.write()

    def insert_entry(self, news_event):
        self.cursor.execute('''INSERT OR IGNORE INTO events
        (start_date, public_date, ticker, token, event, category, price_usd, price_usd2,price_usd3,price_usd4, 
        price_btc, price_btc2,price_btc3,price_btc4,change_24h,change_24h2,change_24h3,change_24h4, 
        change_7d,change_7d2,change_7d3,change_7d4)
         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (news_event.start_date, news_event.public_date, news_event.ticker, news_event.token,
             news_event.event, news_event.category, news_event.price_usd, 0, 0, 0,
             news_event.price_btc, 0, 0, 0, news_event.change_24h, 0, 0, 0, news_event.change_7d, 0, 0, 0))

    def update_entry(self, time_of_day, start_date, ticker, token, price_usd, price_btc, change_24h, change_7d):
        self.cursor.execute('''UPDATE events
              SET 
                price_usd''' + str(time_of_day) + '''="'''+price_usd+'''",
                price_btc''' + str(time_of_day) + '''="'''+price_btc+'''",
                change_24h''' + str(time_of_day) + '''="'''+change_24h+'''",
                change_7d''' + str(time_of_day) + '''="'''+change_7d+'''"
                WHERE
                    start_date = "'''+str(start_date)+'''" AND 
                    token = "'''+str(token)+'''" AND 
                    ticker = "'''+str(ticker)+'"')
        self.write()

    def update_entry2(self, time_of_day, start_date, ticker, token, price_usd, price_btc, change_24h, change_7d):
        self.cursor.execute('''UPDATE news_events
              SET 
                price_usd''' + str(time_of_day) + '''="'''+str(price_usd)+'''",
                price_btc''' + str(time_of_day) + '''="'''+str(price_btc)+'''",
                change_24h''' + str(time_of_day) + '''="'''+str(change_24h)+'''",
                change_7d''' + str(time_of_day) + '''="'''+str(change_7d)+'''"
                WHERE
                    start_date = "'''+str(start_date)+'''" AND
                    token = "'''+str(token)+'''" AND 
                    ticker = "'''+str(ticker)+'"')
        self.write()


