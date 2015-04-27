from __future__ import print_function
from __future__ import unicode_literals

import sys
from fbdb import FbData


def dump_data():
    if len(sys.argv) < 3:
        print('\nUsage: python db2csv.py user filename [startdate enddate] ')
        exit(0)

    user = sys.argv[1]

    fdb = FbData()
    fdb.read()
    fdb.set_user(user)

    with open(sys.argv[2], 'w') as fp:
        if len(sys.argv) == 5:
            fdb.write_csv(fp, user=user, startdate=sys.argv[3], enddate=sys.argv[4])
        else:
            fdb.write_csv(fp, user=user)

if __name__ == '__main__':
    dump_data()
