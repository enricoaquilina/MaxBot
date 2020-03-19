import datetime as dt
# from datetime import datetime
from dateutil.parser import parse

import datetime as dt


class Helper:

    def __init__(self):
        self.options = {
            'START': self.start,
            'FINISH': self.finish,
            'GET_RUN': self.get_run
        }

    def process_date(self, event, date_type):
        date = event[date_type]
        if date:
            date = parse(date).strftime('%Y-%m-%d %H:%M:%f')

        if len(date.split('-')) > 2:
            day = date.split('-')[2]
            if len(day.split(' ')) == 2:
                date = event[date_type].split('-')[0] + '-' + event[date_type].split('-')[1] + '-' + day.split()[0]

        # this is to get padded month and days which are less than 10
        if date != '':
            if len(date.split('-')) > 2:
                date = str(dt.datetime.strptime(date, '%Y-%m-%d')).split(' ')[0]
            elif len(date.split('-')) == 2:
                return date
        return date

    def start(self):
        print('Starting news hunter job (' + dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ')')

    def finish(self, data):
        print('Finished news hunter job (' + dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ')')
        print('________________________________________________________________________')

        for datum in data:
            datum.clear()

    def get_run(self):
        timestamp = dt.datetime.now().time()

        second_run = dt.time(hour=6, minute=0)
        third_run = dt.time(hour=12, minute=0)
        fourth_run = dt.time(hour=18, minute=0)

        timestamp = dt.datetime.now().time()

        if timestamp < second_run:
            return 1
        elif timestamp >= second_run and timestamp < third_run:
            return 2
        elif timestamp >= third_run and timestamp < fourth_run:
            return 3
        elif timestamp > fourth_run:
            return 4