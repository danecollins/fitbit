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

# my includes
from fbcache import FitbitCache

cache = FitbitCache()
cache.read()


with open('Health Data.csv', 'U') as csvfile:
    csvrecords = csv.DictReader(csvfile, dialect='excel')
    for record in csvrecords:
        day = record['Start'][0:-5]
        dist = record['Distance (mi)']
        steps = record['Steps (count)']
        cache.add_item(day, 'watch_steps', steps)
        cache.add_item(day, 'watch_dist', dist)

cache.write()
