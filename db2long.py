from __future__ import print_function
from __future__ import unicode_literals

import sys
import fbcache
import os


def fb_data_to_long():
    if len(sys.argv) < 2:
        print('\nUsage: python db2long.py base_filename.csv user1 [user2 ...]')
        print('   Will product base_filename_{user}.csv for each user')
        exit(0)

    (name, ext) = os.path.splitext(sys.argv[1])
    users = sys.argv[2:]

    for user in users:
        fn = '{}_{}{}'.format(name, user, ext)
        with open(fn, 'w') as fp:
            db = fbcache.FitbitCache(user)
            db.read()
            for date_str, data in db.items():
                for k, v in data.items():
                    if k not in ['actcal', 'active1', 'active2', 'active3', 'margcal', 'sedentary', 'date', 'who']:
                        if not (k == 'weight' and v == 0):  # don't output weights of 0
                            print('{},{},{}'.format(date_str, k, v), file=fp)


if __name__ == '__main__':
    fb_data_to_long()
