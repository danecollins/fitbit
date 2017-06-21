from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict, Counter
import sys

from fbcache import FitbitCache

if len(sys.argv) != 2:
    print('Usage: python dbfix.py [user]')
    exit(1)

user = sys.argv[1]

cache = FitbitCache(user)
if cache.data_exists():
    cache.read()
else:
    print('\nUsage: python dbfix.py [user]')
    print('\n   ERROR: user {} does not have any data'.format(user))
    exit(1)

print("-------------- User: {} ----------------------".format(user))
print("\nDatabase contains %d entries" % len(cache.daylist()))

# empty_days = fbd.remove_days_without_steps()
# print("\nRemoving days with zero steps")
# for x in empty_days:
#     print("    %s" % x)

### this needs to be changed to handle multiple users
missing_days = cache.find_missing_days()
if len(missing_days) > 0:
    print("\nThese days are missing from the database")
    for x in missing_days:
        print("    %s" % x)
else:
    print("\nThere are no missing dates")


# print("\nWriting out database")
# fbd.write()