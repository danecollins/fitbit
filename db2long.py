from __future__ import print_function
from __future__ import unicode_literals

import sys
from fbdb import FbData


def fb_data_to_long():
    if len(sys.argv) < 2:
        print('\nUsage: python db2long.py filename')
        exit(0)

    fn = sys.argv[1]

    fdb = FbData()
    fdb.read()

    with open(fn, 'w') as fp:
        for user in fdb.db.keys():
            for date_str, data in fdb.db[user].items():
                for k, v in data.items():
                    if k not in ['actcal', 'active1', 'active2', 'active3', 'margcal', 'sedentary', 'date', 'who']:
                        if not (k == 'weight' and v == 0):  # don't output weights of 0
                            print('{},{}_{},{}'.format(date_str, k, user, v), file=fp)

def weather_to_long():
    if len(sys.argv) < 2:
        print('\nUsage: python db2long.py filename')
        exit(0)

    fn = sys.argv[1]

    with open('weather.csv') as fin:
        lines = fin.readlines()

    with open(fn, 'w') as fp:
        line = lines[0].strip()
        fields = line.split(',')
        for line in lines[1:]:
            line = line.strip()
            data = line.split(',')
            for k, v in zip(fields[1:], data[1:]):
                print('{},{},{}'.format(data[0], k, v), file=fp)
if __name__ == '__main__':
    weather_to_long()
