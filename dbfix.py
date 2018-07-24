from __future__ import print_function
from __future__ import unicode_literals

from optparse import OptionParser
from fbcache import FitbitCache

usage = "usage: %prog [options] user_name"
parser = OptionParser(usage)
parser.add_option("-c", "--commit",
                  action="store_true", dest="commit",
                  help="commit changes to database")


(options, args) = parser.parse_args()


if len(args) != 1:
    parser.print_help()
    exit(1)
else:
    user_name = args[0]


cache = FitbitCache(user_name)
if cache.data_exists():
    cache.read()
else:
    parser.print_help()
    print('\n   ERROR: user {} does not have any data'.format(user_name))
    exit(1)

print("-------------- User: {} ----------------------".format(user_name))
print("\nDatabase contains %d entries" % len(cache.daylist()))

empty_days = cache.remove_days_without_steps()
print("\nRemoving days with zero steps")
for x in empty_days:
    print("    %s" % x)


missing_days = cache.find_missing_days()
if len(missing_days) > 0:
    print("\nThese days are missing from the database")
    for x in missing_days:
        print("    %s" % x)
else:
    print("\nThere are no missing dates")

if options.commit:
    print("\nWriting out database")
    cache.write()
