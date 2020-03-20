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
        self.db[collection].update(
            {'category': event.category, 'event_date': event.event_date, 'source': event.source},
            {
                '$setOnInsert': vars(event),
            },
            upsert=True
        )

    def get_events_for_today(self, collection):
        return self.db[collection].find({'event_date': str(datetime.date.today())})

    def add_financial_event(self, collection, event_to_update, new_field, new_info):
        return self.db[collection].update_one(
            {'_id': event_to_update['_id']},
            {
                '$set':
                {
                    new_field: new_info
                },
                '$currentDate':
                {
                    'modified_date': True
                },
            },
            upsert=True
        )