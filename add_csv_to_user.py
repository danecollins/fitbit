"""
This is used to add data in a .csv file to a user.  It is currently limited to
data that has only one value per day.  The first column in the .csv must be
a date in the YYYY-MM-DD format.

The first line in the csv should be the header names for the columns.  Ideally
these should not contain spaces and should not start with a number (you'll 
appreciate this when you get into R)

See cycling_data.csv as an example.

Usage is: python add_csv_to_user.py user_name file_name.csv
"""
from fbcache import FitbitCache
import datetime
import sys
import os


def add_csv_data(cache, fn):

    with open(fn, 'U') as fp:
        lines = [l.strip() for l in fp.readlines()]

    columns = lines[0].split(',')[1:]  # col 0 is the data, other columns are fields to add
    item_count = 0

    for line in lines[1:]:
        fields = line.split(',')
        cols = fields[1:]
        day = datetime.datetime.strptime(fields[0], '%Y-%m-%d').date()
        for name, value in zip(columns, cols):
            try:
                value = float(value)
            except:
                pass
            cache.add_item(day, name, value)
            item_count += 1

    return item_count


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python add_csv_to_user.py user_name csv_file.csv')
        exit(1)

    user_name = sys.argv[1]
    fbcache = FitbitCache(user_name)

    if fbcache.data_exists():
        fbcache.read()

    fn = sys.argv[2]
    if not os.path.exists(fn):
        print('Filename {} does not exist'.format(fn))
        print('Usage: python add_csv_to_user.py user_name csv_file.csv')
        exit(1)

    count = add_csv_data(fbcache, fn)
    fbcache.write()
    print('Items added = {}'.format(count))
