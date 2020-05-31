"""
Used to import step/distance data from Apple Watch

Note the source data comes from an iPhone app named QS Access
     https://itunes.apple.com/gb/app/qs-access/id920297614?mt=8

or from apple_xml_parse.py.

Script assumes that QS Access is saved as csv.
Export should be done on a '1 Day' boundary rather than '1 Hour'

Note:
    * all non-zero values are added to the database
    * existing values are overwritten if the new value is larger
      don't write small values because they should never be smaller
    * cycling distance is not imported because it is reported incorrectly (garmin problem)
"""

# standard python includes
import pandas as pd
import csv
import datetime

# my includes
from fbcache import FitbitCache

from optparse import OptionParser


usage = "usage: %prog user-name filename"
parser = OptionParser(usage)

(options, args) = parser.parse_args()

if len(args) != 2:
    parser.print_help()
    exit(1)
else:
    user_name = args[0]
    filename = args[1]

cache = FitbitCache(user_name)
cache.read()


df = pd.read_csv(filename)
df['start'] = pd.to_datetime(df.Start)
df = df[['start', 'Distance (mi)', 'Steps (count)', 'Flights Climbed (count)']]
df.columns = ['start', 'distance', 'steps', 'flights']
df = df.head(len(df) - 1)  # need to drop last day because it's a partial day


for key, row in df.iterrows():
    date = row.start.date()  # convert from pandas timestamp to date
    if date in cache:

        # round values to the precision we want
        row.steps = int(round(row.steps, 0))
        row.distance = round(row.distance, 2)
        row.flights = int(round(row.flights, 0))
        # do basic validation before adding values in
        if row.steps > 1000:

            if cache[date].get('steps_aw', 0) > row.steps:
                print('warning:{}: steps_aw is {} but db has {}'.format(date, row.steps,
                                                                        cache[date]['steps_aw']))
            elif not cache[date].get('steps_aw'):
                cache.add_item(date, 'steps_aw', row.steps, 0)
                print('{}: steps_aw={}'.format(date, row.steps))
        if row.steps > 1.0:
            if cache[date].get('dist_aw', 0) > row.steps:
                print('warning:{}: dist_aw is {} but db has {}'.format(date, row.distance,
                                                                       cache[date]['dist_aw']))
            elif not cache[date].get('dist_aw'):
                cache.add_item(date, 'dist_aw', row.distance)
                print('{}: dist_aw={}'.format(date, row.distance))
        if row.flights > 1:
            if cache[date].get('floors_aw', 0) > row.steps:
                print('warning:{}: floors_aw is {} but db has {}'.format(date, row.flights,
                                                                         cache[date]['floors_aw']))
            elif not cache[date].get('floors_aw'):
                cache.add_item(date, 'floors_aw', row.flights)
                print('{}: floors_aw={}'.format(date, row.flights))

cache.write()
