"""
Check for days with improper data
"""

from __future__ import print_function
from __future__ import unicode_literals
from fbcache import FitbitCache
import argparse
from datetime import timedelta
import pdb

dt_format = "%Y-%m-%d"

parser = argparse.ArgumentParser(description='Check database for suspicious data values')
parser.add_argument('-d', '--distance', help='check that distance and steps correlate', action='store_true')
parser.add_argument('-s', '--steps', nargs=1, help='minimum number of steps to check for',
                    default=5000)
parser.add_argument('-c', '--calories', nargs=1, help='minimum number of calories to check for')
parser.add_argument('user_name', help='name of user to check')
args = parser.parse_args()

steps_per_mile = 0
step_total = 0
dist_total = 0

if args.distance:
    print('will check distance values')
else:
    print('will NOT check distance values')

user_name = args.user_name

cache = FitbitCache(user_name)

if not cache.data_exists():
    print("ERROR: Could not open data for user '{}'\n".format(user_name))
    parser.print_help()
    exit(1)

cache.read()
days = cache.daylist()

current_date = days[0]
end_date = days[-1]

print('Start    = {}'.format(days[0]))
print('End      = {}'.format(days[-1]))
print('Num Days = {}'.format(cache.num_days()))

i = 0
while current_date <= end_date:
    s = False
    day_data = cache[current_date]
    if 'date' not in day_data:
        day_data['date'] = current_date.strftime(dt_format)

    valid = True

    if not (('steps' in day_data) and ('distance' in day_data) and ('calories' in day_data)):
        print('Illegal day data for {}'.format(current_date))
        print('    {}'.format(day_data))
    else:
        if day_data['steps'] < args.steps:
            valid = False

        if args.distance:
            step_total += day_data['steps']
            dist_total += day_data['distance']
            steps_per_mile = step_total / dist_total

        spm = day_data['steps'] / day_data['distance']
        if abs(spm - steps_per_mile) > 500:
            s = 'this={}, lta={}, distance should be={}'.format(spm, steps_per_mile,
                                                                day_data['steps'] / steps_per_mile)
            valid = False

        if not valid:
            print('{} steps={}, distance={} calories={}'.format(day_data['date'], day_data['steps'],
                                                                day_data['distance'], day_data['calories']))
            if s:
                print("    " + s)

    i += 1
    current_date += timedelta(days=1)
