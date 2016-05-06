"""
Interface to reading and writing fitness (Fitbit) data cache although more than
fitbit data can be stored into it.

While the primary use is to cache fitbit data (using download.py) since there is
limited ability to get to the data through the throttled interface, additional
data can be aggregated into the cache and then exported to various formats.

Note: by design the cache only stores data that has one value per day such as
total distance walked or total steps.  It is not mean to handle items that have
intraday values such as heart rate measurements.

Getting Data
    1) cache = FitbitCache()  # get a cache object
    2) cache.read()  # read in the cache

Adding Data
    cache.add_item(date, item_name, item_value)

Write Changes
    cache.write()

Export Data
    cache.write_to_csv(filename)
    create_dataframe.py  # this is a separate script to eliminate the pandas requirement here

"""
from __future__ import print_function
from __future__ import unicode_literals

import json
import datetime
import os


def user_to_key_file(user):
    """
    Generates filename for key files.  Can be changed to relocate keys to another location.

    :param user: name of the user
    :returns: filename of the key file
    """
    return "keys/{}.key".format(user)


def key_file_exists(user):
    fn = user_to_key_file(user)
    return os.path.exists(fn)


def read_key(user):
    key_file = user_to_key_file(user)
    with open(key_file) as fp:
        data = json.load(fp)

    data.setdefault('client_id', os.environ['FITBIT_CLIENT_ID'])
    data.setdefault('client_secret', os.environ['FITBIT_CLIENT_SECRET'])
    return data


class FitbitCache(dict):

    def __init__(self, user_name):
        filename = "./data/{}.json".format(user_name)
        self.user_name = user_name
        self.filename = filename

    def data_exists(self):
        return os.path.exists(self.filename)

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
            date = day.date()
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

