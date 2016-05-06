"""
For a given users this prints out the range of dates for which
the database has data.

It is useful to run before doing a download to know where to
start.
"""

from __future__ import print_function
from __future__ import unicode_literals
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

if not cache.data_exists():
    print("ERROR: Could not open data for user '{}'\n".format(user_name))
    parser.print_help()
    exit(1)

cache.read()
days = cache.daylist()

print('Start    = {}'.format(days[0]))
print('End      = {}'.format(days[-1]))
print('Num Days = {}'.format(cache.num_days()))
