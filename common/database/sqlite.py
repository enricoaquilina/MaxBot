import sqlite3


class DB:
    def __init__(self):
        self.db = self.connect()

    def connect(self):
        self.db = sqlite3.connect('./database/events.db')
        self.create_table()
        return self.db

    def create_table(self):
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events(
            date      DATETIME,
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
            PRIMARY KEY(date, ticker))
        ''')
        self.write()

    def write(self):
        self.db.commit()

    def insert_entry(self, news_event):
        self.cursor.execute('''INSERT OR IGNORE INTO events
        (date, ticker, token, event, category, price_usd,price_usd2,price_usd3,price_usd4, 
        price_btc, price_btc2,price_btc3,price_btc4,change_24h,change_24h2,change_24h3,change_24h4, 
        change_7d,change_7d2,change_7d3,change_7d4)
         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (news_event.date, news_event.ticker, news_event.token,
             news_event.event, news_event.category, news_event.price_usd, 0, 0, 0,
             news_event.price_btc, 0, 0, 0, news_event.change_24h, 0, 0, 0, news_event.change_7d, 0, 0, 0))

    def update_entry(self, time_of_day, date, ticker, token, price_usd, price_btc, change_24h, change_7d):
        self.cursor.execute('''UPDATE events
              SET 
                price_usd''' + str(time_of_day) + '''="'''+price_usd+'''",
                price_btc''' + str(time_of_day) + '''="'''+price_btc+'''",
                change_24h''' + str(time_of_day) + '''="'''+change_24h+'''",
                change_7d''' + str(time_of_day) + '''="'''+change_7d+'''"
                WHERE
                    date = "'''+str(date)+'''" AND 
                    ticker = "'''+str(ticker)+'"')

    def close(self):
        self.db.close()

