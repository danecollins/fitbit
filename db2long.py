""" This exports the database as a csv file in the following format

    | date    |  user  | activity   | attribute   | value  |

    where activity will be 'walking' for fitbit data and is extensible
    to other activities.

    Multiple users can be output to the same file.
"""

import sys
import fbcache


def fb_data_to_long():
    if len(sys.argv) < 2:

        print('\nUsage: python db2long.py filename user1 [user2 ...]')
        exit(0)

    # (name, ext) = os.path.splitext(sys.argv[1])
    filename = sys.argv[1]
    users = sys.argv[2:]

    with open(filename, 'w') as fp:
        # print header
        print('date,user, activity,attribute,value', file=fp)

        for user in users:
            db = fbcache.FitbitCache(user)
            db.read()
            for date_str, data in db.items():
                for k, v in data.items():
                    if k not in ['actcal', 'active1', 'active2', 'active3', 'margcal',
                                 'sedentary', 'date', 'who']:
                        if (k == 'weight') and (v == 0):
                                continue  # don't output weights of 0
                        else:
                            print('{},{},{},{},{}'.format(date_str, user, 'walking', k, v),
                                  file=fp)


if __name__ == '__main__':
    fb_data_to_long()
