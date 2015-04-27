
from __future__ import print_function
from __future__ import unicode_literals

import json
import datetime

# database is a dict of dates with the value being a fbday object
# Looks like:
# {
#   "dane": {
#     "2014-06-30": {
#       "distance": 8.44,
#       "margcal": 932,
#       "weight": 157.7,
#       "active1": 94,
#       "who": "dane",
#       "calories": 2771,
#       "active3": 96,
#       "active2": 113,
#       "steps": 17235,
#       "date": "2014-06-30",
#       "sedentary": 1137,
#       "actcal": 1487
#     }


class FbData:
    user = False

    def __init__(self, file='./db.json'):
        self.db = {}
        self.__filename__ = file

    def read(self):
        with open(self.__filename__) as f:
            self.db = json.loads(f.read())

    def get_user(self):
        assert self.user is not False, 'You forgot to set the user, call set_get_user(dane|cindy)'
        return self.user

    def get_user_list(self):
        return self.db.keys()

    def set_user(self, user):
        if user in self.db:
            self.user = user
        else:
            self.user = user
            self.db[user] = {}

    def write(self):
        with open(self.__filename__, 'w') as f:
            f.write(json.dumps(self.db, indent=2))

    def get_day(self, day):
        return self.db[self.get_user()][day]

    def add_day(self, day, data):
        # want to make sure we never set the data back to the wrong day so
        # store the day in the data and use set_day to make changes (which does
        # does not take a day but uses the stored day)

        # Day Format:
        # {'distance': 6.92, 'margcal': 0, 'steps': 14136, 'active3': 0,
        #  'weight': 183.9, 'active1': 670, 'sedentary': 770, 'calories': 2125,
        #  'actcal': 1225, 'active2': 0}
        data['date'] = day
        if day in self.db[self.get_user()]:
            print('ERROR: day {} is already in the data, use set_day'.format(day))
        else:
            self.db[self.get_user()][day] = data

    def set_day(self, data):
        day = data['date']
        if day not in self.db[self.get_user()]:
            print('ERROR: day {} not in data'.format(day))
        else:
            self.db[self.get_user()][day] = data

    def exists(self, date):
        return date in self.db[self.get_user()]

    def add_biking(self, date, dist):
        if self.exists(date):
            d = self.db[self.get_user()][date]
            d['biking'] = dist

    def num_days(self):
        return len(self.db[self.get_user()])

    def daylist(self):
        return(sorted(self.db[self.get_user()].keys()))

    def remove_days_without_steps(self):
        removed = list()
        for day in self.daylist():
            if self.db[self.get_user()][day]['steps'] == 0:
                del self.db[self.get_user()][day]
                removed.append(day)
        return removed

    def find_missing_days(self):
        day = datetime.datetime(2012, 11, 1)
        end = datetime.datetime.now()
        oneday = datetime.timedelta(days=1)
        db = self.db[self.get_user()]
        missing = list()
        while day <= end:
            key = day.strftime('%Y-%m-%d')
            if key not in db:
                missing.append(key)
            day = day + oneday
        return missing

    def create_derived_fields(self):
        for k, data in self.db.items():
            date = datetime.strptime('%Y-%m-%d', k)
            data['day'] = date  # .year, .month, .day .isocalendar()[1]

    def write_csv(self, fp, user=False, startdate=False, enddate=False):
        # Day Format:
        # {'distance': 6.92, 'margcal': 0, 'steps': 14136, 'active3': 0,
        #  'weight': 183.9, 'active1': 670, 'sedentary': 770, 'calories': 2125,
        #  'actcal': 1225, 'active2': 0}

        # standard field to output
        fields_out = ['distance', 'steps', 'weight', 'active1', 'active2', 'active3',
                      'sedentary', 'calories', 'actcal', 'biking']

        # additional field to write out that are computed
        xtra = ['date', 'month', 'year']

        if user:
            xtra.append('user')

        print(','.join(fields_out+xtra), file=fp)

        output_days = self.daylist()
        if (startdate and enddate):
            output_days = [x for x in output_days if x >= startdate and x <= enddate]

        for date in output_days:
            day = self.db[self.get_user()][date]
            for x in fields_out:
                val = day[x] if x in day else 0.0
                fp.write(str(val) + ",")
            fp.write(date + ",")
            sdate = datetime.datetime.strptime(date, '%Y-%m-%d')
            fp.write(str(sdate.month) + ",")
            fp.write(str(sdate.year))
            if user:
                fp.write(',' + user + '\n')
            else:
                fp.write('\n')
