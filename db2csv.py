"""
Convert the database for one user into a .csv file with the first column being the data and each attribute
in a separate column.

Writes data to standard out unless --outputfile is specified.
If --verbose is specified you should specify an output file or CSV data will include debugging lines.
"""

from __future__ import print_function
from __future__ import unicode_literals

import sys
from optparse import OptionParser

# my includes
from fbcache import FitbitCache


usage = "usage: %prog [options] user_name"
parser = OptionParser(usage)
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose",
                  help="print additional debugging information")
parser.add_option('-o', '--output',
                  action="store", dest='filename',
                  help="output file name, if missing writes to stdout")


def dump_data(fp, debug):
    stats = cache.write_as_csv(fp)
    if debug:
        print(stats, file=sys.stderr)


if __name__ == '__main__':
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
        else:
            cache.read()
        if options.verbose:
            debug = True
        else:
            debug = False

        if options.filename:
            fp = open(options.filename, 'w')
            if debug:
                print('Writing data to file: {}'.format(options.filename))
        else:
            fp = sys.stdout

    dump_data(fp, debug)
