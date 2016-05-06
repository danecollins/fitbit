"""
Used to import step/distance data from Apple Watch

Note the source data comes from an iPhone app named QS Access
     https://itunes.apple.com/gb/app/qs-access/id920297614?mt=8
This app is free and is a great way to get the step/distance data off the phone (way better than
exporting from Health app).

Script assumes that QS Access is saved as default name "Health Data.csv" and that only steps
and distance are exported.  Export should be done on a '1 Day' boundary rather than '1 Hour'
"""

# compatibility imports
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# standard python includes
import csv
import datetime

# my includes
from fbcache import FitbitCache

from optparse import OptionParser


usage = "usage: %prog user-name"
parser = OptionParser(usage)

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.print_help()
    exit(1)
else:
    user_name = args[0]

cache = FitbitCache(user_name)
cache.read()


with open('Health_Data.csv', 'U') as csvfile:
    csvrecords = csv.DictReader(csvfile, dialect='excel')
    next(csvrecords)  # skip header
    for record in csvrecords:
        day = record['Start'][0:-6]
        day_as_dt = datetime.datetime.strptime(day, '%d-%b-%Y')

        dist = record['Distance (mi)']
        steps = record['Steps (count)']
        cache.add_item(day_as_dt, 'steps_aw', float(steps))
        cache.add_item(day_as_dt, 'dist_aw', float(dist))

cache.write()
