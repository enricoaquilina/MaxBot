import sqlite3
import datetime

class DB:
    def __init__(self, db_name):
        self.db = self.connect(db_name)

    def connect(self, db_name):
        self.db = sqlite3.connect('../holy_grail/data/'+db_name+'.db')
        if db_name == 'news_events':
            self.create_table2()
        else:
            self.create_table()
        return self.db

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
            caption   TEXT,
            proof     TEXT,
            public_date     DATETIME,
            start_date      DATETIME,
            end_date  DATETIME,
            coin_name TEXT,
            coin_symbol TEXT,
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
            UNIQUE(start_date, public_date, coin_symbol)
            PRIMARY KEY(start_date, public_date, coin_symbol))
        ''')
        self.write()

    def write(self):
        self.db.commit()

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
                price_usd''' + str(time_of_day) + '''="'''+price_usd+'''",
                price_btc''' + str(time_of_day) + '''="'''+price_btc+'''",
                change_24h''' + str(time_of_day) + '''="'''+change_24h+'''",
                change_7d''' + str(time_of_day) + '''="'''+change_7d+'''"
                WHERE
                    start_date = "'''+str(start_date)+'''" AND
                    coin_name = "'''+str(token)+'''" AND 
                    coin_symbol = "'''+str(ticker)+'"')
        self.write()

    def check_or_insert(self, event):
        self.cursor.execute('''INSERT OR IGNORE INTO news_events
                (caption, proof, public_date, start_date, end_date, coin_name, coin_symbol,
                 price_usd, price_usd2, price_usd3, price_usd4, price_btc, price_btc2,
                 price_btc3, price_btc4, change_24h, change_24h2, change_24h3, change_24h4, 
                 change_7d,change_7d2,change_7d3,change_7d4)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                            (event.event, event.proof, event.public_date, event.start_date,
                             event.end_date, event.token, event.ticker, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    def get_events_for_today(self):
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            SELECT * FROM news_events 
            WHERE
                start_date = "'''+str(datetime.date.today())+'''"''')
        return self.cursor.fetchall()

    def close(self):
        self.db.close()

