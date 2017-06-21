"""
Script downloads data from the fitbit website and caches it locally

Keys for the users are defined in a keys/user.key file

If you request more than 30 days the script will automatically
time-limit itself to prevent hiting the rate limits at fitbit.com

Script collects both step data and weight data.  It does not collect
any data on food or water intake but could be modified to do so.
"""

from __future__ import print_function
from __future__ import unicode_literals

import fbcache
from fbcache import key_file_exists, user_to_key_file, read_key
import fitbit
from datetime import datetime
from datetime import timedelta
import sys
import time


def weight_on_day(c, d):
    body = c.body(d)
    try:
        return body['body']['weight']
    except KeyError:
        print('ERROR in getting weight')
        print(body)


def activity_on_day(c, d):
    """
    Gets the activities record and maps the values of interest to user-friendly names
    Names in returned dict can be changed without breaking anything

    :param c: auth_client object
    :param d: day
    :return: dict of the data for the specified day
    """
    act = c.activities(d)
    s = act['summary']
    summary = {'calories': s['caloriesOut'],
               'actcal': s['activityCalories'],
               'margcal': s['marginalCalories'],
               'floors': s['floors'],
               'elevation': s['elevation'],
               'distance': s['distances'][0]['distance'],
               'sedentary': s['sedentaryMinutes'],
               'active1': s['lightlyActiveMinutes'],
               'active2': s['fairlyActiveMinutes'],
               'active3': s['veryActiveMinutes'],
               'steps': s['steps']
               }
    return summary


def get_data():
    if len(sys.argv) != 4:
        print('Usage: python download.py user startdate enddate')
        print('       start and end dates are in the form 2016-03-01')
        exit(1)

    user = sys.argv[1]
    if key_file_exists(user):
        key_data = read_key(user)
    else:
        print('\nUsage: python download.py [user] [startdate] [enddate]')
        print('\n   ERROR: user {} does not have a key file ({}), run get_keys.py'.format(user,
              user_to_key_file(user)))
        exit(1)

    authd_client = fitbit.Fitbit(key_data['client_id'],
                                 key_data['client_secret'],
                                 access_token=key_data['access_token'],
                                 refresh_token=key_data['refresh_token'])

    one_day = timedelta(1)
    d = datetime.strptime(sys.argv[2], '%Y-%m-%d')
    de = datetime.strptime(sys.argv[3], '%Y-%m-%d')

    # do we need to throttle back?
    throttle = (de - d).days > 30
    if throttle:
        print("Will throttle as there are more than 30 days (%d)" % (de - d).days)

    cache = fbcache.FitbitCache(user)
    cache.read()

    # get data one day at a time
    token_age = 0
    while d <= de:
        if (token_age % 50) == 0:
            authd_client.client.refresh_token()  # make sure the token is fresh (only lasts 1 hour)
        try:
            s = activity_on_day(authd_client, d)
            # add the data to the cache
            for name, value in s.items():
                cache.add_item(d, name, value)
        except:
            print("Error getting activity: {}".format(sys.exc_info()[0]))

        try:
            w = weight_on_day(authd_client, d)
            cache.add_item(d, 'weight', w)
        except:
            print("Error getting weight: {}".format(sys.exc_info()[0]))

        print('got data for {}'.format(d.strftime('%Y-%m-%d')))
        d = d + one_day

        # in case something crashes, we don't want to lose anything so write cache
        cache.write()

        if throttle:
            time.sleep(55)
            token_age += 1

    authd_client.sleep()


if __name__ == '__main__':
    get_data()
