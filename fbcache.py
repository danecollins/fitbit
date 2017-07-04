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
    """
    This is a cache of data from fitbit or other data providers.  The format of the data is:
        dict[date] = {name:value, name:value, name:value}

    It is limited to having one set of data per day.  The daily data set is a dict with as many
    items as desired.  For example in the case of fitbit data this will contains steps, distance,
    calories and may contain weight and other fitbit data.  It is meant to be flexible enough to
    allow you to import other data such as cycling or other exercise data to keep it all in one
    data structure.

    Usage:
        cache = FitbitCache(user_name)  # create the object for that user
        cache.read()  # read the data in the cache file
        cache.write()  # write the cache to disk
        cache.write_as_csv(filename)  # write the data to a csv, helper for dbdump

        cache.add_item(day, name, value)  # add or replace the value for item name on date day
        cache.num_days  # number of days in the data
        cache.daylist()  # return the list of days, in order, in the data
        cache.find_missing_days()  # return the days between the first and last day without data

    Notes:
        A separate command dumpdb is used to export the data for analysis.  This is not done in this
        file because I did not want the pandas dependency here.
    """
    def __init__(self, user_name):
        filename = './data/{}.json'.format(user_name)
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
        print('Read {} days for user {}'.format(len(self), self.user_name))
        return self  # allows read to be chained onto FitbitCache()

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
            print('Improper date passed to add_item: {}, type:{}', day, type(day))
            return False
        if date not in self:
            self[date] = {}

        self[date][name] = value
        return True

    def num_days(self):
        return len(self)

    def daylist(self):
        return sorted(self.keys())

    def remove_days_without_steps(self):
        x = []
        for k, v in self.items():
            # if the day has no steps, delete it
            if v.get('steps', 0) < 1:
                x.append(k)
        # can't remove in loop above since it would change the dict while iterating it
        for k in x:
            del self[k]
        return x

    def find_missing_days(self):
        daylist = self.daylist()
        start = min(daylist)
        end = max(daylist)
        one_day = datetime.timedelta(days=1)
        missing = []
        test_day = start
        while test_day <= end:
            if test_day not in self:
                missing.append(test_day)
            test_day = test_day + one_day
        return missing

    def write_as_csv(self, fp, delim=',', header=True):
        """
        Write out the database as CSV

        Will collect up all the attributes, order the dates and write out the data
        :param fp: output port
        :param delim: delimiter for csv file
        :param header: whether a header line should be written
        :return: dict of statistics on what was written
        """

        stats = dict(lines=0)  # stats we will collect and return

        # collect up all the attributes
        fields = set()
        for d in self.values():
            fields |= set(d.keys())

        fields = sorted(fields)
        if 'who' in fields:
            fields.remove('who')  # obsolete field

        stats['fields'] = ['date'] + fields
        if header:
            print(','.join(stats['fields']), file=fp)

        for day, data in sorted(self.items()):
            print('{}'.format(day.strftime('%Y-%m-%d')), end='', file=fp)
            for f in fields:
                print(delim, data.get(f, 'NA'), end='', file=fp)
            print(file=fp)
            stats['lines'] += 1

        stats['header'] = header

        return stats
