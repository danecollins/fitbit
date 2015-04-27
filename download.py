from __future__ import print_function
from __future__ import unicode_literals

import fitbit
from datetime import datetime
from datetime import timedelta
from keys import fitbit_key
from fbdb import FbData
import sys
import time

#######################################################################
# Script downloads data from the fitbit website and caches it locally
#
# Keys for the users are defined in keys.py which uses environment
# variables to get the keys
#
# If you request more than 30 days the script will automatically
# throddle itself to prevent hiting the rate limits at fitbit.com
#
# Script collects both step data and weight data.  It does not collect
# any data on food or water intake.


def weight_on_day(c, d):
    body = c.body(d)
    try:
        return(body['body']['weight'])
    except:
        print('ERROR in getting weight')
        print(body)


def activity_on_day(c, d):
    act = c.activities(d)
    s = act['summary']
    summary = {'calories': s['caloriesOut'],
               'actcal': s['activityCalories'],
               'margcal': s['marginalCalories'],
               'distance': s['distances'][0]['distance'],
               'sedentary': s['sedentaryMinutes'],
               'active1': s['lightlyActiveMinutes'],
               'active2': s['fairlyActiveMinutes'],
               'active3': s['veryActiveMinutes'],
               'steps': s['steps']
               }
    return(summary)


def get_data():
    if len(sys.argv) != 4:
        print('Usage: python download.py user startdate enddate')
        exit(0)

    (consumer_key, consumer_secret, oakeys) = fitbit_key()
    if sys.argv[1] in oakeys:
        oa = oakeys[sys.argv[1]]
    else:
        print('\nUsage: python download.py [user] [startdate] [enddate]')
        print('     where user is one of {}'.format(oakeys.keys()))
        exit(1)

    authd_client = fitbit.Fitbit(consumer_key,
                                 consumer_secret,
                                 resource_owner_key=oa['oauth_token'],
                                 resource_owner_secret=oa['oauth_token_secret'])

    oneday = timedelta(1)
    d = datetime.strptime(sys.argv[2], '%Y-%m-%d')
    de = datetime.strptime(sys.argv[3], '%Y-%m-%d')

    # do we need to throttle back?
    throttle = (de - d).days > 30
    if throttle:
        print("Will throttle as there are more than 30 days (%d)" % (de - d).days)

    fdb = FbData()
    fdb.read()
    fdb.set_user(sys.argv[1])

    # get data one day at a time

    while d <= de:
        try:
            s = activity_on_day(authd_client, d)
        except:
            print("Error getting activity: {}".format(sys.exc_info()[0]))

        try:
            w = weight_on_day(authd_client, d)
        except:
            print("Error getting weight: {}".format(sys.exc_info()[0]))

        s['weight'] = w
        day = d.strftime('%Y-%m-%d')
        print('got data for {}'.format(day))
        fdb.add_day(day, s)
        d = d + oneday
        fdb.write()
        if throttle:
            time.sleep(60)

    authd_client.sleep()

if __name__ == '__main__':
    get_data()
