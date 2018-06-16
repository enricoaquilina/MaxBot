import datetime
# from datetime import datetime
from dateutil.parser import parse


class Helper:

    def __init__(self):
        self.options = {'START': self.start,
                        'FINISH': self.finish}

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
                date = str(datetime.datetime.strptime(date, '%Y-%m-%d')).split(' ')[0]
            elif len(date.split('-')) == 2:
                return date
        return date

    def start(self):
        print('Starting news hunter job (' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ')')

    def finish(self, data):
        print('Finished news hunter job (' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ')')
        print('________________________________________________________________________')

        for datum in data:
            datum.clear()

