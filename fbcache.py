
from __future__ import print_function
from __future__ import unicode_literals

import json
import datetime
import os

# database is a dict of dates with the value being a fbday object
# Looks like:
#  {
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


class FitbitCache(dict):

    def __init__(self, user_name):
        filename = "./data/{}.json".format(user_name)
        self.user_name = user_name
        self.filename = filename

    def read(self):
        assert os.path.exists(self.filename)
        with open(self.filename) as f:
            db = json.loads(f.read())
        for k, v in db.items():
            day = datetime.datetime.strptime(k, '%Y-%m-%d').date()
            self[day] = v

    def get_user(self):
        return self.user_name

    def write(self):
        with open(self.filename, 'w') as f:
            # only want to write out dict, not attributes
            # convert time to a string to make json file more readable
            f.write(json.dumps({k.strftime('%Y-%m-%d'): v for k, v in self.items()}, indent=2))

    def add_item(self, day, name, value):
        if isinstance(day, datetime.datetime):
            date = datetime.date()
        elif isinstance(day, str):
            date = datetime.datetime.strptime(day, '%Y-%m-%d').date()
        elif isinstance(day, datetime.date):
            date = day
        else:
            print('Improper date passed to add_item: {}, type:{}', day, typeof(day))
            return False
        if date not in self:
            self[date] = {}

        self[date][name] = value
        return True

    def num_days(self):
        return len(self)

    def daylist(self):
        return(sorted(self.keys()))

    def find_missing_days(self):
        daylist = self.daylist()
        start = daylist[0]
        end = daylist[-1]
        one_day = datetime.timedelta(days=1)
        missing = []
        test_day = start
        while test_day <= end:
            if test_day not in self:
                missing.append(test_day)
            test_day = test_day + one_day
        return missing

    def create_derived_fields(self):
        for k, data in self.db.items():
            date = datetime.strptime('%Y-%m-%d', k)
            data['day'] = date  # .year, .month, .day .isocalendar()[1]

