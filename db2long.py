from __future__ import print_function
from __future__ import unicode_literals

import sys
from fbdb import FbData


def dump_data():
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
                        if not (k == 'weight' and v == 0):
                            print('{},{},{},{}'.format(date_str, user, k, v), file=fp)

if __name__ == '__main__':
    dump_data()
